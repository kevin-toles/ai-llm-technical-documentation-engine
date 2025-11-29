"""
Characterization tests for ui/desktop_app.py

TDD Iteration 1: Document current behavior before refactoring
Target: Reduce _execute_workflow() from CC 49 to <10
Target: Reduce get_files() from CC 21 to <10
Target: Reduce _execute_taxonomy_generation() from CC 16 to <10

Reference: BATCH1_CRITICAL_FILES_REMEDIATION_PLAN.md File #3
Architecture: Service Layer Pattern (Architecture Patterns Ch. 4)
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from ui.desktop_app import API, WORKFLOWS


class TestGetFilesCurrentBehavior:
    """
    Characterization tests for get_files() method.
    
    Current behavior (CC 21):
    - Looks up workflow config by tab_id
    - Scans input directory for files
    - Filters out cache/hidden files
    - Special handling for tab3 (taxonomy setup)
    - Special handling for tab4 (metadata enrichment)
    - Returns dict with files list
    """
    
    def test_returns_error_for_invalid_tab(self):
        """Test: Returns error dict for invalid tab_id"""
        api = API()
        
        result = api.get_files("invalid_tab")
        
        assert "error" in result
        assert result["error"] == "Invalid tab"
    
    def test_returns_empty_list_for_nonexistent_directory(self):
        """Test: Returns empty files list if directory doesn't exist"""
        api = API()
        
        # tab1 might not have input dir
        result = api.get_files("tab1")
        
        assert "files" in result
        assert isinstance(result["files"], list)
        assert "input_dir" in result
    
    def test_filters_hidden_and_cache_files(self):
        """Test: Filters out files starting with . or containing 'cache'"""
        api = API()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob') as mock_glob:
                # Mock files including hidden and cache
                mock_file1 = Mock()
                mock_file1.name = "book1.json"
                mock_file2 = Mock()
                mock_file2.name = ".hidden.json"
                mock_file3 = Mock()
                mock_file3.name = "cache_file.json"
                mock_file4 = Mock()
                mock_file4.name = "book2.json"
                
                mock_files = [mock_file1, mock_file2, mock_file3, mock_file4]
                mock_glob.return_value = mock_files
                
                result = api.get_files("tab2")
                
                assert len(result["files"]) == 2
                assert ".hidden.json" not in result["files"]
                assert "cache_file.json" not in result["files"]
    
    def test_tab3_includes_tier_support(self):
        """Test: tab3 returns supports_tiers flag and tier definitions"""
        api = API()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                result = api.get_files("tab3")
                
                assert result.get("supports_tiers") is True
                assert "tiers" in result
                assert len(result["tiers"]) > 0
    
    def test_tab4_includes_taxonomy_files(self):
        """Test: tab4 returns taxonomy_files from taxonomy_setup/output"""
        api = API()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                result = api.get_files("tab4")
                
                assert "taxonomy_files" in result


class TestRunWorkflowCurrentBehavior:
    """
    Characterization tests for run_workflow() method.
    
    Current behavior (CC 15):
    - Validates inputs
    - Generates workflow_id
    - Initializes workflow_status dict
    - Spawns thread for _execute_workflow()
    - Returns workflow_id
    """
    
    def test_returns_error_for_invalid_tab(self):
        """Test: Returns error dict for invalid tab_id"""
        api = API()
        
        result = api.run_workflow("invalid_tab", {})
        
        assert "error" in result
    
    def test_returns_error_for_missing_files(self):
        """Test: Returns error when files list is empty"""
        api = API()
        
        result = api.run_workflow("tab1", {"files": []})
        
        assert "error" in result
    
    def test_generates_workflow_id(self):
        """Test: Generates unique workflow ID"""
        api = API()
        
        with patch.object(api, '_execute_workflow'):
            result = api.run_workflow("tab1", {"files": ["test.pdf"]})
            
            assert "workflow_id" in result
            assert result["workflow_id"].startswith("tab1_")
    
    def test_initializes_workflow_status(self):
        """Test: Creates workflow_status entry"""
        api = API()
        
        with patch.object(api, '_execute_workflow'):
            result = api.run_workflow("tab1", {"files": ["test.pdf"]})
            workflow_id = result["workflow_id"]
            
            assert workflow_id in api.workflow_status
            assert "status" in api.workflow_status[workflow_id]
            assert "progress" in api.workflow_status[workflow_id]
    
    def test_spawns_background_thread(self):
        """Test: Executes workflow in background thread"""
        api = API()
        
        with patch.object(api, '_start_standard_workflow') as mock_start:
            mock_start.return_value = {"status": "started", "workflow_id": "test_id"}
            result = api.run_workflow("tab1", {"files": ["test.pdf"]})
            
            # Verify the helper method was called (which spawns the thread)
            mock_start.assert_called_once()
            assert result["status"] == "started"


class TestExecuteWorkflowCurrentBehavior:
    """
    Characterization tests for _execute_workflow() method.
    
    Current behavior (CC 49 - HIGHEST COMPLEXITY):
    - Processes each file individually
    - Builds subprocess command
    - Executes subprocess
    - Captures stdout/stderr
    - Updates progress status
    - Handles errors
    - Different logic per tab_id
    """
    
    def test_processes_multiple_files(self):
        """Test: Iterates through all provided files"""
        api = API()
        workflow_id = "test_wf_1"
        api.workflow_status[workflow_id] = {"status": "running", "progress": []}
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_popen.return_value = mock_process
            
            files = ["file1.pdf", "file2.pdf"]
            api._execute_workflow(workflow_id, "tab1", files, WORKFLOWS["tab1"])
            
            # Should call subprocess for each file
            assert mock_popen.call_count == len(files)
    
    def test_updates_progress_during_execution(self):
        """Test: Updates workflow_status progress list"""
        api = API()
        workflow_id = "test_wf_2"
        api.workflow_status[workflow_id] = {"status": "running", "progress": []}
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (b"success", b"")
            mock_process.returncode = 0
            mock_popen.return_value = mock_process
            
            api._execute_workflow(workflow_id, "tab1", ["test.pdf"], WORKFLOWS["tab1"])
            
            assert len(api.workflow_status[workflow_id]["progress"]) > 0
    
    def test_handles_subprocess_failure(self):
        """Test: Captures errors when subprocess fails"""
        api = API()
        workflow_id = "test_wf_3"
        api.workflow_status[workflow_id] = {"status": "running", "progress": []}
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (b"", b"Error occurred")
            mock_process.returncode = 1
            mock_popen.return_value = mock_process
            
            api._execute_workflow(workflow_id, "tab1", ["test.pdf"], WORKFLOWS["tab1"])
            
            assert api.workflow_status[workflow_id]["status"] == "completed"
            assert any("error" in str(p).lower() or "✗" in str(p) 
                      for p in api.workflow_status[workflow_id]["progress"])


class TestExecuteTaxonomyGenerationCurrentBehavior:
    """
    Characterization tests for _execute_taxonomy_generation() method.
    
    Current behavior (CC 16):
    - Processes taxonomy tiers sequentially
    - Builds concept hierarchy
    - Executes Python script
    - Updates progress
    """
    
    def test_processes_all_tiers(self):
        """Test: Processes all provided tiers (refactored to use subprocess.run)"""
        api = API()
        workflow_id = "test_tax_1"
        api.workflow_status[workflow_id] = {"status": "running", "progress": []}
        
        # Refactored implementation uses dict format: {"tier_name": [files...]}
        tiers = {
            "architecture": ["book1.json"],
            "implementation": ["book2.json"]
        }
        
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Taxonomy generated successfully"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            with patch('pathlib.Path.exists', return_value=True):
                api._execute_taxonomy_generation(workflow_id, tiers, WORKFLOWS["tab3"])
            
            # Should call subprocess.run once with all tiers
            mock_run.assert_called_once()
            assert api.workflow_status[workflow_id]["status"] == "completed"


class TestWorkflowConfigurationCurrentBehavior:
    """
    Tests for WORKFLOWS configuration dict.
    
    Current issues:
    - Magic strings duplicated (".json", "*.json")
    - No validation of required fields
    """
    
    def test_all_workflows_have_required_fields(self):
        """Test: Each workflow has name, input_dir, output_dir, script"""
        required_fields = ["name", "input_dir", "input_ext", "output_dir", "script"]
        
        for tab_id, workflow in WORKFLOWS.items():
            for field in required_fields:
                assert field in workflow, f"{tab_id} missing field: {field}"
    
    def test_workflow_paths_are_pathlib_objects(self):
        """Test: Paths are Path objects, not strings"""
        for tab_id, workflow in WORKFLOWS.items():
            assert isinstance(workflow["input_dir"], Path)
            assert isinstance(workflow["output_dir"], Path)
            assert isinstance(workflow["script"], Path)
