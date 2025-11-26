"""
Async Service Layer for FastAPI workflow execution (main.py).

Applies Service Layer Pattern (Architecture Patterns Ch. 4) and
Strategy Pattern (Architecture Patterns Ch. 13) for async workflows.

This is the async equivalent of workflow_services.py for FastAPI.
"""
from pathlib import Path
from typing import List, Dict, Optional
import asyncio
import json

# Constants for file extensions (DRY principle)
JSON_EXT = ".json"
JSON_GLOB = "*.json"
MD_EXT = ".md"
PDF_EXT = ".pdf"


class AsyncWorkflowExecutionService:
    """
    Service for executing workflows asynchronously (FastAPI).
    
    Reduces execute_workflow() complexity from CC 13 to <5.
    Uses Strategy Pattern for command building.
    """
    
    def __init__(self, workflow_status: Dict, base_dir: Path, workflows_dir: Path):
        self.workflow_status = workflow_status
        self.base_dir = base_dir
        self.workflows_dir = workflows_dir
        self.command_builders = {
            "tab1": self._build_pdf_to_json_command,
            "tab2": self._build_metadata_extraction_command,
            "tab3": self._build_metadata_enrichment_command,
            "tab5": self._build_base_guideline_command
        }
    
    async def execute(self, workflow_id: str, tab_id: str, files: List[str], 
                     workflow: Dict, taxonomy_file: Optional[str] = None):
        """Execute workflow for all files (async)"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            script_path = workflow.get("script")
            
            if not self._validate_script(workflow_id, script_path):
                return
            
            input_dir = workflow["input_dir"]
            output_dir = workflow["output_dir"]
            output_dir.mkdir(parents=True, exist_ok=True)
            
            await self._process_files(workflow_id, tab_id, files, input_dir, 
                                     script_path, taxonomy_file)
            self._finalize(workflow_id)
            
        except Exception as e:
            self._handle_error(workflow_id, str(e))
    
    def _validate_script(self, workflow_id: str, script_path: Optional[Path]) -> bool:
        """Validate script exists"""
        if not script_path or not Path(script_path).exists():
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
            return False
        return True
    
    async def _process_files(self, workflow_id: str, tab_id: str, files: List[str],
                            input_dir: Path, script_path: Path, taxonomy_file: Optional[str]):
        """Process each file in the workflow"""
        successful = []
        failed = []
        
        for file in files:
            try:
                file_path = input_dir / file
                self._update_progress(workflow_id, f"Processing: {file}")
                
                cmd = self._build_command(tab_id, script_path, file_path, taxonomy_file)
                if cmd:
                    result = await self._run_subprocess(cmd)
                    if result["success"]:
                        successful.append(file)
                        self._update_progress(workflow_id, f"✓ Completed: {file}")
                    else:
                        failed.append(file)
                        error_msg = result["error"][:100]
                        self._update_progress(workflow_id, f"✗ Failed: {file} - {error_msg}")
                        
            except Exception as e:
                failed.append(file)
                self._update_progress(workflow_id, f"✗ Error: {file} - {str(e)}")
        
        self.workflow_status[workflow_id]["successful"] = successful
        self.workflow_status[workflow_id]["failed"] = failed
    
    def _build_command(self, tab_id: str, script_path: Path, 
                      file_path: Path, taxonomy_file: Optional[str]) -> Optional[List[str]]:
        """Build command using appropriate strategy"""
        builder = self.command_builders.get(tab_id)
        if builder:
            return builder(script_path, file_path, taxonomy_file)
        return None
    
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
        return ["python3", str(script_path), "--input", str(file_path)]
    
    def _build_base_guideline_command(self, script_path: Path, file_path: Path,
                                      taxonomy_file: Optional[str]) -> List[str]:
        """Build command for base guideline generation"""
        cmd = ["python3", str(script_path), str(file_path)]
        if taxonomy_file:
            taxonomy_path = self.workflows_dir / "taxonomy_setup" / "output" / taxonomy_file
            cmd.extend(["--taxonomy", str(taxonomy_path)])
            self._update_progress(
                list(self.workflow_status.keys())[-1],
                f"Using taxonomy: {taxonomy_file}"
            )
        return cmd
    
    async def _run_subprocess(self, cmd: List[str]) -> Dict:
        """Execute subprocess asynchronously"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.base_dir)
            )
            
            _, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "error": stderr.decode() if stderr else "Unknown error"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _update_progress(self, workflow_id: str, message: str):
        """Update workflow progress"""
        self.workflow_status[workflow_id]["progress"].append(message)
    
    def _finalize(self, workflow_id: str):
        """Finalize workflow execution"""
        from datetime import datetime
        
        successful = self.workflow_status[workflow_id].get("successful", [])
        failed = self.workflow_status[workflow_id].get("failed", [])
        
        self.workflow_status[workflow_id]["status"] = "completed"
        self.workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        self.workflow_status[workflow_id]["summary"] = (
            f"Completed: {len(successful)} successful, {len(failed)} failed"
        )
    
    def _handle_error(self, workflow_id: str, error: str):
        """Handle workflow error"""
        self.workflow_status[workflow_id]["status"] = "error"
        self.workflow_status[workflow_id]["error"] = error


class AsyncFileListService:
    """
    Service for retrieving file lists (async version).
    
    Reduces get_files() complexity from CC 16 to <5.
    """
    
    @staticmethod
    def get_files_for_workflow(input_dir: Path, extension: str) -> List[str]:
        """Get filtered list of files from directory"""
        if not input_dir.exists():
            return []
        
        files = [f.name for f in input_dir.glob(f"*{extension}")]
        return sorted(files)
    
    @staticmethod
    def get_taxonomy_files_with_validation(taxonomy_dir: Path) -> List[str]:
        """Get list of valid concept taxonomy files"""
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
    def get_taxonomy_files(taxonomy_dir: Path) -> List[str]:
        """Get all taxonomy JSON files"""
        if not taxonomy_dir.exists():
            return []
        
        files = [f.name for f in taxonomy_dir.glob(JSON_GLOB)]
        return sorted(files)


class AsyncTaxonomyGenerationService:
    """
    Service for taxonomy generation (async version).
    
    Reduces execute_taxonomy_generation() complexity from CC 12 to <5.
    """
    
    def __init__(self, workflow_status: Dict, base_dir: Path, workflows_dir: Path):
        self.workflow_status = workflow_status
        self.base_dir = base_dir
        self.workflows_dir = workflows_dir
    
    async def execute(self, workflow_id: str, tiers: Dict, workflow: Dict):
        """Execute taxonomy generation"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            self._update_progress(workflow_id, "Analyzing books for concept extraction...")
            
            if not self._validate_tiers(workflow_id, tiers):
                return
            
            tier_books = self._resolve_tier_files(workflow_id, tiers)
            script_path = workflow.get("script")
            
            if not self._validate_script(workflow_id, script_path):
                return
            
            await self._execute_script(workflow_id, script_path, tier_books)
            
        except Exception as e:
            self._handle_error(workflow_id, str(e))
    
    def _validate_tiers(self, workflow_id: str, tiers: Dict) -> bool:
        """Validate required tiers are present"""
        if not tiers.get("architecture") or not tiers.get("implementation"):
            self.workflow_status[workflow_id]["status"] = "failed"
            self._update_progress(
                workflow_id,
                "✗ Error: Architecture and Implementation tiers are required"
            )
            return False
        return True
    
    def _resolve_tier_files(self, workflow_id: str, tiers: Dict) -> Dict:
        """Resolve tier JSON files to metadata paths"""
        tier_books = {}
        for tier_name in ["architecture", "implementation", "practices"]:
            if tiers.get(tier_name):
                resolved_files = []
                for json_file in tiers[tier_name]:
                    resolved_path = self._resolve_to_metadata(workflow_id, json_file)
                    if resolved_path:
                        resolved_files.append(str(resolved_path))
                if resolved_files:
                    tier_books[tier_name] = resolved_files
        return tier_books
    
    def _resolve_to_metadata(self, workflow_id: str, json_filename: str) -> Optional[Path]:
        """Resolve JSON filename to metadata path or fallback"""
        base_name = json_filename.replace(JSON_EXT, "")
        
        # Try metadata first
        metadata_path = (self.workflows_dir / "metadata_extraction" / "output" / 
                        f"{base_name}_metadata{JSON_EXT}")
        if metadata_path.exists():
            self._update_progress(workflow_id, f"  Using metadata: {metadata_path.name}")
            return metadata_path
        
        # Fallback to raw JSON
        json_path = (self.workflows_dir / "pdf_to_json" / "output" / 
                    "textbooks_json" / json_filename)
        if json_path.exists():
            self._update_progress(workflow_id, f"  Using raw JSON: {json_filename}")
            return json_path
        
        self._update_progress(
            workflow_id,
            f"  ✗ Warning: Neither metadata nor JSON found for {json_filename}"
        )
        return None
    
    def _validate_script(self, workflow_id: str, script_path: Optional[Path]) -> bool:
        """Validate script exists"""
        if not script_path or not Path(script_path).exists():
            self.workflow_status[workflow_id]["status"] = "failed"
            self._update_progress(workflow_id, f"✗ Error: Script not found: {script_path}")
            return False
        return True
    
    async def _execute_script(self, workflow_id: str, script_path: Path, tier_books: Dict):
        """Execute taxonomy generation script"""
        from datetime import datetime
        
        # Build command
        tier_json = json.dumps(tier_books)
        timestamp = datetime.now().strftime('%Y%m%d')
        output_filename = f"taxonomy_{timestamp}{JSON_EXT}"
        
        cmd = [
            "python3", 
            str(script_path),
            "--tiers", tier_json,
            "--output", output_filename
        ]
        
        total_files = sum(len(books) for books in tier_books.values())
        self._update_progress(
            workflow_id,
            f"Extracting concepts from {total_files} metadata files..."
        )
        
        # Execute
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.base_dir)
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            self._update_progress(workflow_id, "✓ Concept extraction complete")
            self.workflow_status[workflow_id]["status"] = "completed"
            self.workflow_status[workflow_id]["output_file"] = output_filename
            self._update_progress(workflow_id, f"✓ Taxonomy saved: {output_filename}")
            self.workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        else:
            error_text = stderr.decode() if stderr else "Unknown error"
            self.workflow_status[workflow_id]["status"] = "failed"
            self._update_progress(workflow_id, f"✗ Error: {error_text}")
    
    def _update_progress(self, workflow_id: str, message: str):
        """Update workflow progress"""
        self.workflow_status[workflow_id]["progress"].append(message)
    
    def _handle_error(self, workflow_id: str, error: str):
        """Handle workflow error"""
        self.workflow_status[workflow_id]["status"] = "error"
        self.workflow_status[workflow_id]["error"] = error
