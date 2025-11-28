"""
Workflow execution services for desktop_app.py

Applies Service Layer Pattern (Architecture Patterns Ch. 4) and Strategy Pattern
to reduce _execute_workflow() complexity from CC 49 to <10.

Reference: BATCH1_CRITICAL_FILES_REMEDIATION_PLAN.md File #3
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Constants (DRY principle - no magic strings)
JSON_EXT = ".json"
JSON_GLOB = "*.json"
MD_EXT = ".md"


class WorkflowExecutionService:
    """
    Service Layer for workflow execution (Architecture Patterns Ch. 4).
    
    Orchestrates different workflow strategies and manages status updates.
    Reduces complexity by delegating to specialized command builders.
    """
    
    def __init__(self, workflow_status: Dict[str, Any]):
        self.workflow_status = workflow_status
        self.command_builders = {
            "tab1": self._build_pdf_to_json_command,
            "tab2": self._build_metadata_extraction_command,
            "tab4": self._build_metadata_enrichment_command,
            "tab5": self._build_base_guideline_command,
            "tab6": self._build_llm_enhancement_command
        }
    
    def execute(self, workflow_id: str, tab_id: str, files: List[str], 
                workflow: Dict, taxonomy_file: Optional[str] = None) -> None:
        """
        Execute workflow for given files (CC: 49 → 5).
        
        Delegates to command builders based on tab_id (Strategy Pattern).
        """
        try:
            self._update_status(workflow_id, "running")
            script_path = workflow.get("script")
            
            if not self._validate_script(workflow_id, script_path):
                return
            
            self._prepare_output_directory(workflow["output_dir"])
            
            # Execute using appropriate strategy
            if tab_id in self.command_builders:
                self._execute_file_workflow(
                    workflow_id, tab_id, files, workflow, 
                    script_path, taxonomy_file
                )
            
            self._finalize_workflow(workflow_id)
            
        except Exception as e:
            self._handle_error(workflow_id, str(e))
    
    def _validate_script(self, workflow_id: str, script_path: Path) -> bool:
        """Validate script exists"""
        if not script_path or not Path(script_path).exists():
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
            return False
        return True
    
    def _prepare_output_directory(self, output_dir: Path) -> None:
        """Ensure output directory exists"""
        output_dir.mkdir(parents=True, exist_ok=True)
    
    def _execute_file_workflow(self, workflow_id: str, tab_id: str, 
                                files: List[str], workflow: Dict, 
                                script_path: Path, taxonomy_file: Optional[str]) -> None:
        """Execute workflow for each file with post-execution validation"""
        input_dir = workflow["input_dir"]
        successful = []
        failed = []
        validation_warnings = []
        
        for idx, file in enumerate(files, 1):
            try:
                file_path = input_dir / file
                self._update_progress(workflow_id, f"[{idx}/{len(files)}] Processing: {file}")
                
                # Build command using strategy
                cmd = self._build_command(tab_id, script_path, file_path, taxonomy_file)
                
                if cmd:
                    result = self._run_subprocess(cmd)
                    if result["success"]:
                        # Run post-execution validation for ALL tabs
                        validation_result = self._validate_workflow_output(tab_id, file, workflow)
                        
                        if validation_result["errors"]:
                            failed.append(file)
                            self._update_progress(workflow_id, 
                                f"✗ Validation failed: {file} - {validation_result['errors'][0]}")
                        else:
                            successful.append(file)
                            if validation_result["warnings"]:
                                validation_warnings.extend(validation_result["warnings"])
                                self._update_progress(workflow_id, f"✓ {file} (with warnings)")
                            else:
                                self._update_progress(workflow_id, f"✓ {file}")
                    else:
                        failed.append(file)
                        self._update_progress(workflow_id, f"✗ {file}: {result['error']}")
                        
            except Exception as e:
                failed.append(file)
                self._update_progress(workflow_id, f"✗ {file}: {str(e)}")
        
        self.workflow_status[workflow_id]["successful"] = successful
        self.workflow_status[workflow_id]["failed"] = failed
        if validation_warnings:
            self.workflow_status[workflow_id]["validation_warnings"] = validation_warnings
    
    def _validate_workflow_output(self, tab_id: str, filename: str, 
                                   workflow: Dict) -> Dict[str, List[str]]:
        """
        Validate workflow output based on tab type.
        
        Returns dict with 'errors' and 'warnings' lists.
        """
        try:
            from scripts.workflow_validation_services import WorkflowValidationFacade
            
            # Get workflows_dir from workflow paths
            workflows_dir = workflow["output_dir"].parent.parent
            facade = WorkflowValidationFacade(workflows_dir)
            
            if tab_id == "tab1":
                # PDF to JSON conversion
                result = facade.validate_pdf_conversion(filename)
            elif tab_id == "tab2":
                # Metadata extraction
                result = facade.validate_metadata_extraction(filename)
            elif tab_id == "tab4":
                # Metadata enrichment
                result = facade.validate_metadata_enrichment(filename)
            elif tab_id == "tab5":
                # Base guideline generation
                result = facade.validate_base_guideline(filename)
            elif tab_id == "tab6":
                # LLM enhancement - validate output
                result = facade.validate_llm_output(filename)
            else:
                # Unknown tab - skip validation
                return {"errors": [], "warnings": []}
            
            return {
                "errors": result.get("errors", []),
                "warnings": result.get("warnings", [])
            }
            
        except ImportError as e:
            return {"errors": [], "warnings": [f"Validation skipped: {e}"]}
        except Exception as e:
            return {"errors": [], "warnings": [f"Validation error: {str(e)}"]}
    
    def _build_command(self, tab_id: str, script_path: Path, 
                      file_path: Path, taxonomy_file: Optional[str]) -> Optional[List[str]]:
        """Build command using appropriate strategy"""
        builder = self.command_builders.get(tab_id)
        if builder:
            return builder(script_path, file_path, taxonomy_file)
        return None
    
    # Command builders (Strategy Pattern implementations)
    
    def _build_pdf_to_json_command(self, script_path: Path, file_path: Path, 
                                    taxonomy_file: Optional[str]) -> List[str]:
        """Build command for PDF to JSON conversion"""
        return ["python3", str(script_path), str(file_path)]
    
    def _build_metadata_extraction_command(self, script_path: Path, file_path: Path, 
                                           taxonomy_file: Optional[str]) -> List[str]:
        """Build command for metadata extraction"""
        return ["python3", str(script_path), "--input", str(file_path), "--auto-detect"]
    
    def _build_metadata_enrichment_command(self, script_path: Path, file_path: Path, 
                                           taxonomy_file: Optional[str]) -> List[str]:
        """Build command for metadata enrichment"""
        if not taxonomy_file:
            raise ValueError("Taxonomy file required for metadata enrichment")
        
        return [
            "python3", str(script_path),
            "--metadata-file", str(file_path),
            "--taxonomy-file", str(taxonomy_file)
        ]
    
    def _build_base_guideline_command(self, script_path: Path, file_path: Path, 
                                      taxonomy_file: Optional[str]) -> List[str]:
        """Build command for base guideline generation"""
        return ["python3", str(script_path), "--input", str(file_path)]
    
    def _build_llm_enhancement_command(self, script_path: Path, file_path: Path, 
                                       taxonomy_file: Optional[str]) -> List[str]:
        """Build command for LLM enhancement"""
        return ["python3", str(script_path), "--input", str(file_path)]
    
    def _run_subprocess(self, cmd: List[str]) -> Dict[str, Any]:
        """Execute subprocess and return result"""
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=3600)
            
            return {
                "success": process.returncode == 0,
                "stdout": stdout,
                "stderr": stderr,
                "error": stderr if process.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Process timeout (>1 hour)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _update_status(self, workflow_id: str, status: str) -> None:
        """Update workflow status"""
        self.workflow_status[workflow_id]["status"] = status
    
    def _update_progress(self, workflow_id: str, message: str) -> None:
        """Add progress message"""
        self.workflow_status[workflow_id]["progress"].append(message)
    
    def _finalize_workflow(self, workflow_id: str) -> None:
        """Mark workflow as completed"""
        self.workflow_status[workflow_id]["status"] = "completed"
        self.workflow_status[workflow_id]["progress"].append("✓ All files processed")
    
    def _handle_error(self, workflow_id: str, error: str) -> None:
        """Handle workflow error"""
        self.workflow_status[workflow_id]["status"] = "error"
        self.workflow_status[workflow_id]["error"] = error
        self.workflow_status[workflow_id]["progress"].append(f"✗ Error: {error}")


class FileListService:
    """
    Service for retrieving file lists (reduces get_files() complexity from CC 21 to <5).
    
    Separates file filtering logic from API layer.
    """
    
    @staticmethod
    def get_files_for_workflow(input_dir: Path, extension: str) -> List[str]:
        """Get filtered list of files from directory"""
        if not input_dir.exists():
            print(f"[FileListService] Input dir doesn't exist: {input_dir}")
            return []
        
        all_files = [f.name for f in input_dir.glob(f"*{extension}")]
        files = FileListService._filter_files(all_files)
        print(f"[FileListService] Found {len(files)} files in {input_dir} (filtered from {len(all_files)})")
        return sorted(files)
    
    @staticmethod
    def _filter_files(files: List[str]) -> List[str]:
        """Filter out hidden and cache files"""
        return [
            f for f in files 
            if not f.startswith('.') and 'cache' not in f.lower()
        ]
    
    @staticmethod
    def get_taxonomy_files() -> List[str]:
        """Get list of valid taxonomy files with tier concepts"""
        import json
        taxonomy_dir = Path(__file__).parent.parent / "workflows" / "taxonomy_setup" / "output"
        
        if not taxonomy_dir.exists():
            return []
        
        taxonomy_files = []
        for f in taxonomy_dir.glob(JSON_GLOB):
            try:
                with open(f, 'r') as tf:
                    tax_data = json.load(tf)
                    if 'tiers' in tax_data:
                        has_concepts = any(
                            isinstance(tier, dict) and 'concepts' in tier 
                            for tier in tax_data['tiers'].values()
                        )
                        if has_concepts:
                            taxonomy_files.append(f.name)
            except Exception:
                pass
        
        return sorted(taxonomy_files)
    
    @staticmethod
    def get_enriched_metadata_files() -> List[str]:
        """Get list of enriched metadata files from Tab 4 output"""
        enriched_dir = Path(__file__).parent.parent / "workflows" / "metadata_enrichment" / "output"
        
        if not enriched_dir.exists():
            return []
        
        files = [f.name for f in enriched_dir.glob("*_enr_metadata_*" + JSON_EXT)]
        return sorted(files)

