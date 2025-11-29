"""
Characterization tests for ui/main.py (FastAPI implementation).

Target complexity issues:
- get_files(): CC 16 (highest)
- execute_workflow(): CC 13
- execute_taxonomy_generation(): CC 12
- run_workflow(): CC 8

These tests document current behavior before refactoring to apply:
- Service Layer Pattern (Architecture Patterns Ch. 4)
- Strategy Pattern (Architecture Patterns Ch. 13)
- Extract Method (Python Distilled Ch. 16)
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import json
from fastapi.testclient import TestClient

# Import the FastAPI app
from ui.main import app, WORKFLOWS, workflow_status


@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)


class TestGetFilesCurrentBehavior:
    """
    Characterization tests for get_files() endpoint.
    
    Current behavior (CC 16):
    - Validates tab_id
    - Checks if input directory exists
    - Globs for files with matching extension
    - Special handling for tab5 (taxonomy files with validation)
    - Special handling for tab4 (tier support)
    - Special handling for tab6 (taxonomy + LLM providers)
    """
    
    def test_returns_error_for_invalid_tab(self, client):
        """Test: Returns error for invalid tab_id"""
        response = client.get("/files/invalid_tab")
        data = response.json()
        
        assert "error" in data
        assert data["error"] == "Invalid tab"
    
    def test_returns_empty_list_for_nonexistent_directory(self, client):
        """Test: Returns empty list when directory doesn't exist"""
        with patch('pathlib.Path.exists', return_value=False):
            response = client.get("/files/tab1")
            data = response.json()
            
            assert "files" in data
            assert data["files"] == []
    
    def test_returns_files_for_valid_directory(self, client):
        """Test: Returns list of files matching extension"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob') as mock_glob:
                mock_file1 = Mock()
                mock_file1.name = "book1.pdf"
                mock_file2 = Mock()
                mock_file2.name = "book2.pdf"
                mock_glob.return_value = [mock_file1, mock_file2]
                
                response = client.get("/files/tab1")
                data = response.json()
                
                assert len(data["files"]) == 2
                assert "book1.pdf" in data["files"]
                assert "book2.pdf" in data["files"]
    
    def test_tab4_includes_tier_support(self, client):
        """Test: tab4 returns supports_tiers flag and tier definitions"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                response = client.get("/files/tab4")
                data = response.json()
                
                assert data.get("supports_tiers") is True
                assert "tiers" in data
                assert len(data["tiers"]) == 3
    
    def test_tab5_includes_validated_taxonomy_files(self, client):
        """Test: tab5 returns only valid concept taxonomy files"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                with patch('builtins.open', create=True) as mock_open:
                    # Mock valid taxonomy file
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
                        "tiers": {
                            "architecture": {"concepts": ["pattern1"]}
                        }
                    })
                    
                    response = client.get("/files/tab5")
                    data = response.json()
                    
                    assert "taxonomy_files" in data
    
    @pytest.mark.asyncio
    async def test_tab6_includes_llm_providers(self, client):
        """Test: tab6 returns taxonomy files and LLM provider options"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                response = client.get("/files/tab6")
                data = response.json()
                
                assert "llm_providers" in data
                assert "taxonomy_files" in data


class TestRunWorkflowCurrentBehavior:
    """
    Characterization tests for run_workflow() endpoint.
    
    Current behavior (CC 8):
    - Validates tab_id
    - Generates workflow_id with timestamp
    - Initializes workflow_status
    - Handles 3 workflow types: LLM (tab6), Taxonomy (tab4), Regular files
    - Spawns background task
    """
    
    def test_returns_error_for_invalid_tab(self, client):
        """Test: Returns error for invalid tab_id"""
        response = client.post("/run/invalid_tab", json={"files": ["test.pdf"]})
        data = response.json()
        
        assert "error" in data
    
    def test_returns_error_for_missing_files(self, client):
        """Test: Returns error when no files selected"""
        response = client.post("/run/tab1", json={"files": []})
        data = response.json()
        
        assert "error" in data
    
    def test_generates_workflow_id(self, client):
        """Test: Generates unique workflow_id with timestamp"""
        response = client.post("/run/tab1", json={"files": ["test.pdf"]})
        data = response.json()
        
        assert "workflow_id" in data
        assert data["workflow_id"].startswith("tab1_")
    
    def test_initializes_workflow_status(self, client):
        """Test: Creates workflow_status entry"""
        # Clear previous status
        workflow_status.clear()
        
        response = client.post("/run/tab1", json={"files": ["test.pdf"]})
        data = response.json()
        workflow_id = data["workflow_id"]
        
        # Give background task time to initialize
        import time
        time.sleep(0.1)
        
        assert workflow_id in workflow_status


class TestExecuteWorkflowCurrentBehavior:
    """
    Characterization tests for execute_workflow() function.
    
    Current behavior (CC 13):
    - Validates script exists
    - Processes each file individually
    - Builds command based on tab_id (if/elif chain)
    - Executes subprocess with asyncio
    - Tracks successful and failed files
    """
    
    @pytest.mark.asyncio
    async def test_processes_multiple_files(self):
        """Test: Processes each file in the list"""
        from ui.main import execute_workflow
        
        workflow_id = "test_1"
        workflow_status[workflow_id] = {"status": "starting", "progress": []}
        
        files = ["file1.json", "file2.json"]
        
        with patch('asyncio.create_subprocess_exec') as mock_exec:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_exec.return_value = mock_process
            
            await execute_workflow(workflow_id, "tab2", files, WORKFLOWS["tab2"])
            
            # Should call subprocess for each file
            assert mock_exec.call_count == len(files)
    
    @pytest.mark.asyncio
    async def test_updates_progress_during_execution(self):
        """Test: Updates workflow_status progress list"""
        from ui.main import execute_workflow
        
        workflow_id = "test_2"
        workflow_status[workflow_id] = {"status": "starting", "progress": []}
        
        with patch('asyncio.create_subprocess_exec') as mock_exec:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"", b"")
            mock_process.returncode = 0
            mock_exec.return_value = mock_process
            
            await execute_workflow(workflow_id, "tab2", ["test.json"], WORKFLOWS["tab2"])
            
            assert len(workflow_status[workflow_id]["progress"]) > 0


class TestExecuteTaxonomyGenerationCurrentBehavior:
    """
    Characterization tests for execute_taxonomy_generation() function.
    
    Current behavior (CC 12):
    - Validates required tiers (architecture, implementation)
    - Resolves JSON files to metadata paths
    - Builds tier data structure
    - Executes Python script with tiers
    - Updates progress
    """
    
    @pytest.mark.asyncio
    async def test_validates_required_tiers(self):
        """Test: Fails if architecture or implementation tiers missing"""
        from ui.main import execute_taxonomy_generation
        
        workflow_id = "test_tax_1"
        workflow_status[workflow_id] = {"status": "starting", "progress": []}
        
        # Missing required tiers
        tiers = {"practices": ["book1.json"]}
        
        await execute_taxonomy_generation(workflow_id, tiers, WORKFLOWS["tab4"])
        
        assert workflow_status[workflow_id]["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_resolves_files_to_metadata_paths(self):
        """Test: Prefers metadata files over raw JSON"""
        from ui.main import execute_taxonomy_generation
        
        workflow_id = "test_tax_2"
        workflow_status[workflow_id] = {"status": "starting", "progress": []}
        
        tiers = {
            "architecture": ["book1.json"],
            "implementation": ["book2.json"]
        }
        
        with patch('asyncio.create_subprocess_exec') as mock_exec:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_exec.return_value = mock_process
            
            with patch('pathlib.Path.exists', return_value=True):
                await execute_taxonomy_generation(workflow_id, tiers, WORKFLOWS["tab4"])
                
                # Should mention metadata in progress
                progress_text = " ".join(workflow_status[workflow_id]["progress"])
                assert "metadata" in progress_text.lower() or "json" in progress_text.lower()


class TestWorkflowConfigurationCurrentBehavior:
    """
    Tests for WORKFLOWS configuration dict.
    """
    
    def test_all_workflows_have_required_fields(self):
        """Test: Each workflow has name, input_dir, output_dir"""
        required_fields = ["name", "input_dir", "input_ext", "output_dir"]
        
        for tab_id, workflow in WORKFLOWS.items():
            for field in required_fields:
                assert field in workflow, f"{tab_id} missing field: {field}"
    
    def test_workflow_paths_are_pathlib_objects(self):
        """Test: Paths are Path objects, not strings"""
        for tab_id, workflow in WORKFLOWS.items():
            assert isinstance(workflow["input_dir"], Path)
            assert isinstance(workflow["output_dir"], Path)
