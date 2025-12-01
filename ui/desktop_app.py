"""
Desktop application for LLM Document Enhancer
Uses PyWebView to provide native window with web UI

Refactored using Service Layer Pattern (Architecture Patterns Ch. 4)
to reduce complexity from CC 49 to <10.
"""
import webview
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from threading import Thread
from jinja2 import Template
from ui.workflow_services import (
    WorkflowExecutionService,
    FileListService,
    JSON_EXT,
    JSON_GLOB,
    MD_EXT
)


# Base paths
UI_DIR = Path(__file__).parent
BASE_DIR = UI_DIR.parent
WORKFLOWS_DIR = BASE_DIR / "workflows"

# Workflow configurations
WORKFLOWS = {
    "tab1": {
        "name": "PDF to JSON",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "input",
        "input_ext": ".pdf",
        "output_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "script": WORKFLOWS_DIR / "pdf_to_json" / "scripts" / "convert_pdf_to_json.py"
    },
    "tab2": {
        "name": "Metadata Extraction",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "script": WORKFLOWS_DIR / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"
    },
    "tab3": {
        "name": "Taxonomy Setup",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "taxonomy_setup" / "output",
        "script": WORKFLOWS_DIR / "taxonomy_setup" / "scripts" / "generate_concept_taxonomy.py"
    },
    "tab4": {
        "name": "Metadata Enrichment",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "metadata_enrichment" / "output",
        "script": WORKFLOWS_DIR / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"
    },
    "tab5": {
        "name": "Base Guideline",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "script": WORKFLOWS_DIR / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py"
    },
    "tab6": {
        "name": "LLM Enhancement",
        "input_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "input_ext": JSON_EXT,
        "exclude_dirs": ["chapter_summaries"],
        "output_dir": WORKFLOWS_DIR / "llm_enhancement" / "output",
        "script": WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "integrate_llm_enhancements.py"
    }
}


class API:
    """API class exposed to JavaScript via pywebview"""
    
    def __init__(self):
        self.workflow_status = {}
    
    def get_files(self, tab_id):
        """Get list of files for the specified workflow (refactored: CC 21 → 3)"""
        print(f"[API] get_files called with tab_id: {tab_id}")
        if tab_id not in WORKFLOWS:
            print(f"[API] Invalid tab: {tab_id}")
            return {"error": "Invalid tab"}
        
        workflow = WORKFLOWS[tab_id]
        exclude_dirs = workflow.get("exclude_dirs", [])
        files = FileListService.get_files_for_workflow(
            workflow["input_dir"], 
            workflow["input_ext"],
            exclude_dirs=exclude_dirs
        )
        
        response = {
            "files": files,
            "input_dir": str(workflow["input_dir"])
        }
        
        # Add tab-specific metadata
        if tab_id == "tab3":
            response.update(self._get_tab3_metadata())
        
        elif tab_id == "tab4":
            response["taxonomy_files"] = FileListService.get_taxonomy_files()
        
        elif tab_id == "tab6":
            response.update(self._get_tab6_metadata())
        else:
            response["output_dir"] = str(workflow["output_dir"])
        
        return response
    
    def _get_tab3_metadata(self):
        """Get Taxonomy Setup tab metadata"""
        return {
            "supports_tiers": True,
            "tiers": [
                {"id": "architecture", "name": "Architecture Spine", "priority": 1},
                {"id": "implementation", "name": "Implementation", "priority": 2},
                {"id": "practices", "name": "Engineering Practices", "priority": 3}
            ]
        }
    
    def _get_tab6_metadata(self):
        """Get LLM Enhancement tab metadata - enriched metadata auto-discovered by backend"""
        return {
            "taxonomy_files": FileListService.get_taxonomy_files(),
            "llm_providers": self.get_llm_providers()
        }
    
    def get_taxonomy_files(self):
        """Get list of available taxonomy files"""
        taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
        
        if not taxonomy_dir.exists():
            return {"files": []}
        
        files = [f.name for f in taxonomy_dir.glob("*.json")]
        return {"files": sorted(files)}
    
    def get_llm_providers(self):
        """Get available LLM providers and their models (matching llm_evaluation.py configs)"""
        return {
            "anthropic": {
                "name": "Anthropic (Primary)",
                "models": [
                    {"id": "claude-opus-4-5-20251101", "name": "Claude Opus 4.5", "recommended": True},
                    {"id": "claude-sonnet-4-5-20250929", "name": "Claude Sonnet 4.5"},
                ]
            },
            "openai": {
                "name": "OpenAI (Primary)",
                "models": [
                    {"id": "gpt-5.1", "name": "GPT-5.1", "recommended": True},
                    {"id": "gpt-5", "name": "GPT-5"},
                    {"id": "gpt-5.1-mini", "name": "GPT-5.1 Mini"},
                    {"id": "gpt-5.1-nano", "name": "GPT-5.1 Nano"},
                ]
            },
            "google": {
                "name": "Google",
                "models": [
                    {"id": "gemini-3-pro-preview", "name": "Gemini 3 Pro"},
                    {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash"},
                ]
            },
            "deepseek": {
                "name": "DeepSeek",
                "models": [
                    {"id": "deepseek-chat", "name": "DeepSeek V3"},
                    {"id": "deepseek-reasoner", "name": "DeepSeek R1"},
                ]
            }
        }
    
    def run_workflow(self, tab_id, data):
        """Execute workflow with selected files (refactored: CC 15 → 5)"""
        self._log_workflow_request(tab_id, data)
        
        if tab_id not in WORKFLOWS:
            return {"error": "Invalid tab"}
        
        workflow = WORKFLOWS[tab_id]
        workflow_id = self._generate_workflow_id(tab_id, data)
        print(f"[API] Starting workflow {workflow_id}")
        
        # Initialize status
        self._initialize_workflow_status(workflow_id, workflow["name"])
        
        # Delegate to appropriate handler
        if tab_id == "tab6" and "llm_config" in data:
            return self._start_llm_enhancement(workflow_id, data, workflow)
        elif tab_id == "tab3" and "tiers" in data:
            return self._start_taxonomy_generation(workflow_id, data, workflow)
        else:
            return self._start_standard_workflow(workflow_id, tab_id, data, workflow)
    
    def _log_workflow_request(self, tab_id, data):
        """Log workflow request details"""
        print(f"\n{'='*80}")
        print("[API] run_workflow called")
        print(f"[API] tab_id: {tab_id}")
        print(f"[API] data type: {type(data)}")
        print(f"[API] data keys: {data.keys() if isinstance(data, dict) else 'N/A'}")
        print(f"[API] full data: {json.dumps(data, indent=2)}")
        print(f"{'='*80}\n")
        
        # Extra diagnostics for taxonomy tab
        if tab_id == 'tab3':
            try:
                tiers = data.get('tiers', {}) if isinstance(data, dict) else {}
                arch = tiers.get('architecture', [])
                impl = tiers.get('implementation', [])
                pract = tiers.get('practices', [])
                print(f"[API][DIAG] Taxonomy request: taxonomy_name={data.get('taxonomy_name')} "
                      f"arch_count={len(arch)} impl_count={len(impl)} pract_count={len(pract)}")
            except Exception as e:
                print(f"[API][DIAG] Failed to log taxonomy diagnostics: {e}")
    
    def _generate_workflow_id(self, tab_id, data):
        """Generate appropriate workflow ID"""
        if tab_id == "tab3" and "taxonomy_name" in data:
            taxonomy_name = data.get("taxonomy_name", "taxonomy")
            return f"{taxonomy_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return f"{tab_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _initialize_workflow_status(self, workflow_id, workflow_name):
        """Initialize workflow status tracking"""
        self.workflow_status[workflow_id] = {
            "status": "starting",
            "workflow": workflow_name,
            "started_at": datetime.now().isoformat(),
            "progress": []
        }
    
    def _start_llm_enhancement(self, workflow_id, data, workflow):
        """Start LLM enhancement workflow"""
        thread = Thread(target=self._execute_llm_enhancement, 
                       args=(workflow_id, data["llm_config"], workflow))
        thread.daemon = True
        thread.start()
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started LLM enhancement with {data['llm_config']['provider']}/{data['llm_config']['model']}"
        }
    
    def _start_taxonomy_generation(self, workflow_id, data, workflow):
        """Start taxonomy generation workflow"""
        thread = Thread(target=self._execute_taxonomy_generation, 
                       args=(workflow_id, data["tiers"], workflow))
        thread.daemon = True
        thread.start()
        total_files = sum(len(files) for files in data["tiers"].values())
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started taxonomy generation with {total_files} file(s)"
        }
    
    def _start_standard_workflow(self, workflow_id, tab_id, data, workflow):
        """Start standard file processing workflow"""
        selected_files = data.get("files", [])
        if not selected_files:
            return {"error": "No files selected"}
        
        taxonomy_file = data.get("taxonomy")
        
        # Validate Tab 4 requires taxonomy
        if tab_id == "tab4" and not taxonomy_file:
            return {"error": "Taxonomy file is required for metadata enrichment. Please select a taxonomy."}
        
        # Execute in background thread
        thread = Thread(target=self._execute_workflow, 
                       args=(workflow_id, tab_id, selected_files, workflow, taxonomy_file))
        thread.daemon = True
        thread.start()
        
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started processing {len(selected_files)} file(s)"
        }
    
    def get_status(self, workflow_id):
        """Get status of a running workflow"""
        if workflow_id not in self.workflow_status:
            return {"error": "Workflow not found"}
        
        return self.workflow_status[workflow_id]
    
    def _execute_workflow(self, workflow_id, tab_id, files, workflow, taxonomy_file=None):
        """Execute a workflow with selected files (refactored: CC 134 → 5)"""
        print(f"[API] _execute_workflow started for {workflow_id}, files: {files}")
        try:
            # Delegate to WorkflowExecutionService
            service = WorkflowExecutionService(self.workflow_status)
            service.execute(workflow_id, tab_id, files, workflow, taxonomy_file)
            
        except Exception as e:
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = str(e)
    
    def _execute_taxonomy_generation(self, workflow_id, tiers, workflow):
        """Generate concept taxonomy (refactored: CC 29 → 5)"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            self.workflow_status[workflow_id]["progress"].append("Analyzing books for concept extraction...")
            
            # Validate tiers
            if not self._validate_tiers(workflow_id, tiers):
                return
            
            # Resolve files to metadata paths
            tier_books = self._resolve_tier_files(workflow_id, tiers)
            
            # Build and execute command
            script_path = workflow.get("script")
            if not self._validate_script(workflow_id, script_path):
                return
            
            output_filename = self._generate_taxonomy_filename(workflow_id)
            cmd = self._build_taxonomy_command(script_path, tier_books, output_filename)
            
            self._execute_taxonomy_script(workflow_id, cmd, tier_books, output_filename)
            
        except Exception as e:
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = str(e)
    
    def _validate_tiers(self, workflow_id, tiers):
        """Validate required tiers are present"""
        if not tiers.get("architecture") or not tiers.get("implementation"):
            self.workflow_status[workflow_id]["status"] = "failed"
            self.workflow_status[workflow_id]["progress"].append(
                "✗ Error: Architecture and Implementation tiers are required"
            )
            return False
        return True
    
    def _resolve_tier_files(self, workflow_id, tiers):
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
    
    def _resolve_to_metadata(self, workflow_id, json_filename):
        """Resolve JSON filename to metadata path or fallback to raw JSON"""
        base_name = json_filename.replace(JSON_EXT, "")
        
        # Try metadata first
        metadata_path = WORKFLOWS_DIR / "metadata_extraction" / "output" / f"{base_name}_metadata{JSON_EXT}"
        if metadata_path.exists():
            self.workflow_status[workflow_id]["progress"].append(f"  Using metadata: {metadata_path.name}")
            return metadata_path
        
        # Fallback to raw JSON
        json_path = WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json" / json_filename
        if json_path.exists():
            self.workflow_status[workflow_id]["progress"].append(f"  Using raw JSON: {json_filename}")
            return json_path
        
        # File not found
        self.workflow_status[workflow_id]["progress"].append(
            f"  ✗ Warning: Neither metadata nor JSON found for {json_filename}"
        )
        return None
    
    def _validate_script(self, workflow_id, script_path):
        """Validate script exists"""
        if not script_path or not Path(script_path).exists():
            self.workflow_status[workflow_id]["status"] = "failed"
            self.workflow_status[workflow_id]["progress"].append(f"✗ Error: Script not found: {script_path}")
            return False
        return True
    
    def _generate_taxonomy_filename(self, workflow_id):
        """Generate output filename for taxonomy"""
        taxonomy_name = workflow_id.split('_')[0] if '_' in workflow_id else 'taxonomy'
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"{taxonomy_name}_taxonomy_{timestamp}{JSON_EXT}"
    
    def _build_taxonomy_command(self, script_path, tier_books, output_filename):
        """Build taxonomy generation command"""
        tier_json = json.dumps(tier_books)
        return [
            "python3", 
            str(script_path),
            "--tiers", tier_json,
            "--output", output_filename
        ]
    
    def _execute_taxonomy_script(self, workflow_id, cmd, tier_books, output_filename):
        """Execute taxonomy generation script"""
        total_files = sum(len(books) for books in tier_books.values())
        self.workflow_status[workflow_id]["progress"].append(
            f"Extracting concepts from {total_files} metadata files..."
        )
        
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
        
        if result.returncode == 0:
            output_text = result.stdout if result.stdout else ""
            self.workflow_status[workflow_id]["progress"].append("✓ Concept extraction complete")
            self.workflow_status[workflow_id]["progress"].extend(output_text.strip().split('\n')[-5:])
            
            self.workflow_status[workflow_id]["status"] = "completed"
            self.workflow_status[workflow_id]["output_file"] = output_filename
            self.workflow_status[workflow_id]["progress"].append(f"✓ Taxonomy saved: {output_filename}")
            self.workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        else:
            error_text = result.stderr if result.stderr else "Unknown error"
            self.workflow_status[workflow_id]["status"] = "failed"
            self.workflow_status[workflow_id]["progress"].append(f"✗ Error: {error_text}")
    
    def _execute_llm_enhancement(self, workflow_id, llm_config, workflow):
        """Execute LLM enhancement (runs in background thread)"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            
            # Extract source book name from guideline (e.g. "AI Engineering Building Applications_guideline.json" -> "AI Engineering Building Applications")
            guideline_name = llm_config.get('guideline', '')
            source_book = guideline_name.replace("_guideline.json", "").replace(".json", "")
            
            # Log all selections for debugging
            print(f"\n{'='*60}")
            print(f"[LLM Enhancement] Starting workflow: {workflow_id}")
            print(f"[LLM Enhancement] Source Book: {source_book}")
            print(f"[LLM Enhancement] Guideline: {llm_config.get('guideline', 'N/A')}")
            print(f"[LLM Enhancement] Taxonomy: {llm_config.get('taxonomy', 'N/A')}")
            print(f"[LLM Enhancement] Provider: {llm_config.get('provider')}")
            print(f"[LLM Enhancement] Model: {llm_config.get('model')}")
            print(f"{'='*60}\n")
            
            # Validate required fields
            if not llm_config.get('guideline'):
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = "Guideline is required"
                return
            
            if not llm_config.get('taxonomy'):
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = "Taxonomy is required for aggregate package creation"
                self.workflow_status[workflow_id]["progress"].append("✗ Error: Taxonomy selection is required")
                return
            
            # Step 1: Prepare files for aggregate package creation
            # Following production flow from run_extraction_tests.py
            aggregate_script = WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "create_aggregate_package.py"
            if not aggregate_script.exists():
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = f"Aggregate package script not found: {aggregate_script}"
                return
            
            # Source directories
            base_taxonomy_path = WORKFLOWS_DIR / "taxonomy_setup" / "output" / llm_config["taxonomy"]
            metadata_dir = WORKFLOWS_DIR / "metadata_extraction" / "output"
            enriched_dir = WORKFLOWS_DIR / "metadata_enrichment" / "output"
            guideline_dir = WORKFLOWS_DIR / "base_guideline_generation" / "output"
            tmp_dir = WORKFLOWS_DIR / "llm_enhancement" / "tmp"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            
            self.workflow_status[workflow_id]["progress"].append(f"Source Book: {source_book}")
            self.workflow_status[workflow_id]["progress"].append(f"Guideline: {llm_config['guideline']}")
            self.workflow_status[workflow_id]["progress"].append(f"Taxonomy: {llm_config['taxonomy']}")
            self.workflow_status[workflow_id]["progress"].append(f"Provider: {llm_config['provider']}")
            self.workflow_status[workflow_id]["progress"].append(f"Model: {llm_config['model']}")
            
            # Step 2: Create profile-specific taxonomy with proper naming
            # Production script extracts source_book from: "{source_book}_taxonomy.json"
            taxonomy_for_aggregate = tmp_dir / f"{source_book}_taxonomy.json"
            
            # Copy and transform base taxonomy
            import json as json_module
            import shutil
            
            self.workflow_status[workflow_id]["progress"].append("Preparing taxonomy...")
            shutil.copy(base_taxonomy_path, taxonomy_for_aggregate)
            
            # Transform taxonomy books from dicts to strings if needed
            with open(taxonomy_for_aggregate) as f:
                taxonomy_data = json_module.load(f)
            
            tiers = taxonomy_data.get("tiers", {})
            transformed = False
            for tier_name, tier_data in tiers.items():
                books = tier_data.get("books", [])
                if books and isinstance(books[0], dict):
                    tier_data["books"] = [book["name"] for book in books if isinstance(book, dict) and "name" in book]
                    transformed = True
            
            if transformed:
                with open(taxonomy_for_aggregate, "w") as f:
                    json_module.dump(taxonomy_data, f, indent=2)
                self.workflow_status[workflow_id]["progress"].append("✓ Transformed taxonomy to production format")
            
            # Step 3: Prepare metadata directory with source book metadata
            profile_metadata_dir = tmp_dir / "metadata"
            profile_metadata_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all companion book metadata
            for meta_file in metadata_dir.glob("*_metadata.json"):
                shutil.copy(meta_file, profile_metadata_dir / meta_file.name)
            
            # Ensure source book metadata exists with expected name
            source_metadata = profile_metadata_dir / f"{source_book}_metadata.json"
            if not source_metadata.exists():
                # Try to find a matching metadata file
                possible_source = metadata_dir / f"{source_book}_metadata.json"
                if possible_source.exists():
                    shutil.copy(possible_source, source_metadata)
            
            self.workflow_status[workflow_id]["progress"].append(f"✓ Prepared metadata directory ({len(list(profile_metadata_dir.glob('*.json')))} files)")
            
            # Step 4: Find enriched metadata for source book
            enriched_file = enriched_dir / f"{source_book}_enriched.json"
            enriched_for_aggregate = None
            
            if enriched_file.exists():
                # Copy with production naming pattern
                from datetime import datetime as dt
                timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
                enriched_for_aggregate = tmp_dir / f"{source_book}_enr_metadata_{timestamp}.json"
                shutil.copy(enriched_file, enriched_for_aggregate)
                self.workflow_status[workflow_id]["progress"].append(f"✓ Found enriched metadata: {enriched_file.name}")
                print(f"[LLM Enhancement] Using enriched metadata: {enriched_file}")
            else:
                self.workflow_status[workflow_id]["progress"].append("ℹ No enriched metadata found, using basic metadata")
                print(f"[LLM Enhancement] No enriched metadata found for {source_book}")
            
            # Step 5: Build aggregate package command
            aggregate_cmd = [
                "python3", str(aggregate_script),
                "--taxonomy", str(taxonomy_for_aggregate),
                "--metadata-dir", str(profile_metadata_dir),
                "--guideline-dir", str(guideline_dir),
                "--output-dir", str(tmp_dir)
            ]
            
            if enriched_for_aggregate:
                aggregate_cmd.extend(["--enriched-metadata", str(enriched_for_aggregate)])
            
            self.workflow_status[workflow_id]["progress"].append("Creating aggregate package...")
            
            # Execute aggregate package creation
            aggregate_result = subprocess.run(
                aggregate_cmd,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )
            
            if aggregate_result.returncode != 0:
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = f"Aggregate package creation failed: {aggregate_result.stderr}"
                self.workflow_status[workflow_id]["progress"].append("✗ Aggregate package creation failed")
                return
            
            self.workflow_status[workflow_id]["progress"].append("✓ Aggregate package created")
            
            # Step 2: Run LLM enhancement with the guideline and taxonomy
            script_path = workflow.get("script")
            if not script_path or not Path(script_path).exists():
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = f"Enhancement script not found: {script_path}"
                return
            
            # Set environment variables for LLM provider/model
            env = os.environ.copy()
            env["LLM_PROVIDER"] = llm_config["provider"]
            if llm_config["provider"] == "anthropic":
                env["ANTHROPIC_MODEL"] = llm_config["model"]
            else:
                env["OPENAI_MODEL"] = llm_config["model"]
            
            # Find the created aggregate package
            package_pattern = f"{source_book}_llm_package_*.json"
            package_files = sorted(tmp_dir.glob(package_pattern), reverse=True)
            if not package_files:
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = "Aggregate package not found"
                return
            aggregate_path = package_files[0]
            
            # Build command with --aggregate and --guideline
            # The guideline should be the markdown file, not JSON
            guideline_json = llm_config["guideline"]
            guideline_md = guideline_json.replace("_guideline.json", "_guideline.md")
            guideline_path = guideline_dir / guideline_md
            
            # Fall back to JSON if markdown doesn't exist
            if not guideline_path.exists():
                guideline_path = guideline_dir / guideline_json
            
            cmd = [
                "python3", str(script_path),
                "--aggregate", str(aggregate_path),
                "--guideline", str(guideline_path)
            ]
            
            self.workflow_status[workflow_id]["progress"].append("Starting LLM enhancement...")
            
            # Use Popen for streaming output instead of subprocess.run
            process = subprocess.Popen(
                cmd,
                cwd=str(BASE_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                bufsize=1  # Line buffered
            )
            
            # Stream stdout line by line for real-time progress
            output_lines = []
            for line in iter(process.stdout.readline, ''):
                line = line.rstrip()
                if line:
                    output_lines.append(line)
                    # Show chapter progress in UI
                    if "Chapter " in line or line.startswith("✓") or line.startswith("✅") or line.startswith("�"):
                        self.workflow_status[workflow_id]["progress"].append(line)
            
            process.stdout.close()
            stderr_output = process.stderr.read()
            process.stderr.close()
            return_code = process.wait()
            
            if return_code == 0:
                # Find the output file for validation
                output_dir = WORKFLOWS_DIR / "llm_enhancement" / "output"
                enhanced_files = sorted(output_dir.glob("*_guideline_enhanced.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                
                self.workflow_status[workflow_id]["progress"].append("✓ LLM enhancement completed")
                
                # Step 3: Run compliance validation
                if enhanced_files:
                    enhanced_file = enhanced_files[0]
                    self.workflow_status[workflow_id]["progress"].append(f"Running compliance validation on {enhanced_file.name}...")
                    
                    validator_script = WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "compliance_validator_v3.py"
                    if validator_script.exists():
                        val_cmd = [
                            "python3", str(validator_script),
                            "--md", str(enhanced_file),
                            "--output-format", "text",
                            "--verbose"
                        ]
                        val_result = subprocess.run(val_cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
                        
                        # Parse validation output
                        if val_result.returncode == 0:
                            self.workflow_status[workflow_id]["progress"].append("✓ Compliance validation passed")
                        else:
                            self.workflow_status[workflow_id]["progress"].append("⚠ Compliance validation found issues:")
                        
                        # Show last few lines of validation output
                        val_lines = val_result.stdout.strip().split('\n') if val_result.stdout else []
                        for vline in val_lines[-5:]:
                            if vline.strip():
                                self.workflow_status[workflow_id]["progress"].append(f"  {vline}")
                
                self.workflow_status[workflow_id]["status"] = "completed"
                self.workflow_status[workflow_id]["output"] = '\n'.join(output_lines[-20:])
            else:
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = stderr_output
                self.workflow_status[workflow_id]["progress"].append("✗ Enhancement failed")
            
            self.workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = str(e)


def main():
    """Launch the desktop application"""
    api = API()
    
    # Get HTML template path
    template_path = UI_DIR / "templates" / "index.html"
    
    if not template_path.exists():
        print(f"Error: Template not found at {template_path}")
        return
    
    # Read and render Jinja2 template
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Render template with workflows data
    template = Template(template_content)
    html_content = template.render(workflows=WORKFLOWS)
    
    # Inject pywebview API adapter script
    api_adapter = '''
    <script>
    // Safe PyWebView detection
    function hasPyWebView() {
        return (
            typeof window !== 'undefined' &&
            typeof window.pywebview !== 'undefined' &&
            window.pywebview !== null &&
            typeof window.pywebview.api !== 'undefined'
        );
    }
    
    // Store original fetch before overriding
    const originalFetch = window.fetch;
    
    // Wait for pywebview to be ready
    window.addEventListener('pywebviewready', function() {
        if (hasPyWebView()) {
            console.log('PyWebView API ready!');
            console.log('Available methods:', Object.keys(window.pywebview.api));
        } else {
            console.log('pywebviewready fired but window.pywebview missing');
        }
    });
    
    // PyWebView API Adapter
    window.apiAdapter = {
        async getFiles(tabId) {
            console.log('apiAdapter.getFiles called with:', tabId);
            
            if (hasPyWebView()) {
                try {
                    const result = await window.pywebview.api.get_files(tabId);
                    console.log('getFiles result:', result);
                    return result;
                } catch (error) {
                    console.error('PyWebView getFiles error:', error);
                    throw error;
                }
            } else {
                // Browser fallback - use original fetch
                try {
                    const resp = await originalFetch(`/files/${tabId}`);
                    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                    return await resp.json();
                } catch (error) {
                    console.error('fetch getFiles error:', error);
                    throw error;
                }
            }
        },
        async runWorkflow(tabId, data) {
            console.log('apiAdapter.runWorkflow called with:', tabId, data);
            
            if (hasPyWebView()) {
                try {
                    const result = await window.pywebview.api.run_workflow(tabId, data);
                    console.log('runWorkflow result:', result);
                    return result;
                } catch (error) {
                    console.error('PyWebView runWorkflow error:', error);
                    throw error;
                }
            } else {
                // Browser fallback - use original fetch
                try {
                    const resp = await originalFetch(`/run/${tabId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                    return await resp.json();
                } catch (error) {
                    console.error('fetch runWorkflow error:', error);
                    throw error;
                }
            }
        },
        async getStatus(workflowId) {
            console.log('apiAdapter.getStatus called with:', workflowId);
            
            if (hasPyWebView()) {
                try {
                    const result = await window.pywebview.api.get_status(workflowId);
                    console.log('getStatus result:', result);
                    return result;
                } catch (error) {
                    console.error('PyWebView getStatus error:', error);
                    throw error;
                }
            } else {
                // Browser fallback - use original fetch
                try {
                    const resp = await originalFetch(`/status/${workflowId}`);
                    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                    return await resp.json();
                } catch (error) {
                    console.error('fetch getStatus error:', error);
                    throw error;
                }
            }
        }
    };
    
    // Override fetch for API endpoints
    window.fetch = async function(url, options) {
        console.log('fetch intercepted:', url);
        // Check if it's an API endpoint
        if (typeof url === 'string') {
            if (url.startsWith('/files/')) {
                const tabId = url.split('/')[2];
                return {
                    status: 200,
                    ok: true,
                    json: async () => await window.apiAdapter.getFiles(tabId)
                };
            } else if (url.startsWith('/run/')) {
                const tabId = url.split('/')[2];
                const data = JSON.parse(options.body);
                return {
                    status: 200,
                    ok: true,
                    json: async () => await window.apiAdapter.runWorkflow(tabId, data)
                };
            } else if (url.startsWith('/status/')) {
                const workflowId = url.split('/')[2];
                return {
                    status: 200,
                    ok: true,
                    json: async () => await window.apiAdapter.getStatus(workflowId)
                };
            }
        }
        // Fall back to original fetch for non-API calls
        return originalFetch(url, options);
    };
    </script>
    '''
    
    # Inject before closing </head> tag
    html_content = html_content.replace('</head>', f'{api_adapter}</head>')
    
    # Read CSS file and inject inline
    css_path = UI_DIR / 'static' / 'css' / 'style.css'
    if css_path.exists():
        with open(css_path, 'r') as f:
            css_content = f.read()
        # Inject CSS inline
        html_content = html_content.replace(
            '<link rel="stylesheet" href="/static/css/style.css">',
            f'<style>{css_content}</style>'
        )
    
    # Create window
    webview.create_window(
        title='LLM Document Enhancer',
        html=html_content,
        js_api=api,
        width=1400,
        height=900,
        resizable=True
    )
    
    # Start webview
    webview.start(debug=True)


if __name__ == "__main__":
    main()
