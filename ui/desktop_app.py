"""
Desktop application for LLM Document Enhancer
Uses PyWebView to provide native window with web UI
"""
import webview
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from threading import Thread
from jinja2 import Template


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
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "script": WORKFLOWS_DIR / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"
    },
    "tab3": {
        "name": "Taxonomy Setup",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "taxonomy_setup" / "output",
        "script": WORKFLOWS_DIR / "taxonomy_setup" / "scripts" / "generate_concept_taxonomy.py"
    },
    "tab4": {
        "name": "Metadata Enrichment",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "metadata_enrichment" / "output",
        "script": WORKFLOWS_DIR / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"
    },
    "tab5": {
        "name": "Base Guideline",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "script": WORKFLOWS_DIR / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py"
    },
    "tab6": {
        "name": "LLM Enhancement",
        "input_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output" / "chapter_summaries",
        "input_ext": ".md",
        "output_dir": WORKFLOWS_DIR / "llm_enhancement" / "output",
        "script": WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "integrate_llm_enhancements.py"
    }
}


class API:
    """API class exposed to JavaScript via pywebview"""
    
    def __init__(self):
        self.workflow_status = {}
    
    def get_files(self, tab_id):
        """Get list of files available for the workflow"""
        print(f"[API] get_files called with tab_id: {tab_id}")
        if tab_id not in WORKFLOWS:
            print(f"[API] Invalid tab: {tab_id}")
            return {"error": "Invalid tab"}
        
        workflow = WORKFLOWS[tab_id]
        input_dir = workflow["input_dir"]
        
        if not input_dir.exists():
            print(f"[API] Input dir doesn't exist: {input_dir}")
            return {"files": [], "input_dir": str(input_dir)}
        
        # Get all files with matching extension (excluding cache/system files)
        all_files = [f.name for f in input_dir.glob(f"*{workflow['input_ext']}")]
        # Filter out cache files and hidden files
        files = [f for f in all_files if not f.startswith('.') and 'cache' not in f.lower()]
        print(f"[API] Found {len(files)} files in {input_dir} (filtered from {len(all_files)})")
        
        # Special handling for Taxonomy Setup tab - show tier builder
        if tab_id == "tab3":
            return {
                "files": sorted(files),
                "input_dir": str(input_dir),
                "supports_tiers": True,
                "tiers": [
                    {"id": "architecture", "name": "Architecture Spine", "priority": 1},
                    {"id": "implementation", "name": "Implementation", "priority": 2},
                    {"id": "practices", "name": "Engineering Practices", "priority": 3}
                ]
            }
        
        # Special handling for Metadata Enrichment tab - include taxonomy files
        if tab_id == "tab4":
            taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
            taxonomy_files = []
            if taxonomy_dir.exists():
                for f in taxonomy_dir.glob("*.json"):
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
                    except:
                        pass
            return {
                "files": sorted(files),
                "input_dir": str(input_dir),
                "taxonomy_files": sorted(taxonomy_files)
            }
        
        # Special handling for LLM tab
        if tab_id == "tab6":
            taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
            taxonomy_files = []
            if taxonomy_dir.exists():
                taxonomy_files = [f.name for f in taxonomy_dir.glob("*.json")]
            
            providers_data = self.get_llm_providers()
            
            return {
                "files": sorted(files),
                "input_dir": str(input_dir),
                "taxonomy_files": sorted(taxonomy_files),
                "llm_providers": providers_data
            }
        
        return {
            "files": sorted(files),
            "input_dir": str(input_dir),
            "output_dir": str(workflow["output_dir"])
        }
    
    def get_taxonomy_files(self):
        """Get list of available taxonomy files"""
        taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
        
        if not taxonomy_dir.exists():
            return {"files": []}
        
        files = [f.name for f in taxonomy_dir.glob("*.json")]
        return {"files": sorted(files)}
    
    def get_llm_providers(self):
        """Get available LLM providers and their models"""
        return {
            "openai": {
                "name": "OpenAI",
                "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
            },
            "anthropic": {
                "name": "Anthropic",
                "models": [
                    "claude-sonnet-4-5-20250929",
                    "claude-haiku-4-5-20251001",
                    "claude-opus-4-1-20250805",
                    "claude-sonnet-4-20250514",
                    "claude-opus-4-20250514", 
                    "claude-3-7-sonnet-20250219",
                    "claude-3-5-haiku-20241022",
                    "claude-3-haiku-20240307"
                ]
            }
        }
    
    def run_workflow(self, tab_id, data):
        """Execute workflow with selected files"""
        print(f"\n{'='*80}")
        print(f"[API] run_workflow called")
        print(f"[API] tab_id: {tab_id}")
        print(f"[API] data type: {type(data)}")
        print(f"[API] data keys: {data.keys() if isinstance(data, dict) else 'N/A'}")
        print(f"[API] full data: {json.dumps(data, indent=2)}")
        print(f"{'='*80}\n")

        # Extra diagnostics specifically for taxonomy tab
        if tab_id == 'tab3':
            try:
                tiers = data.get('tiers', {}) if isinstance(data, dict) else {}
                arch = tiers.get('architecture', [])
                impl = tiers.get('implementation', [])
                pract = tiers.get('practices', [])
                print(f"[API][DIAG] Taxonomy request received: taxonomy_name={data.get('taxonomy_name')} arch_count={len(arch)} impl_count={len(impl)} pract_count={len(pract)}")
                print(f"[API][DIAG] Architecture files: {arch}")
                print(f"[API][DIAG] Implementation files: {impl}")
                print(f"[API][DIAG] Practices files: {pract}")
            except Exception as e:
                print(f"[API][DIAG] Failed to log taxonomy diagnostics: {e}")
        
        if tab_id not in WORKFLOWS:
            return {"error": "Invalid tab"}
        
        workflow = WORKFLOWS[tab_id]
        workflow_id = f"{tab_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"[API] Starting workflow {workflow_id}")
        
        # Initialize status
        self.workflow_status[workflow_id] = {
            "status": "starting",
            "workflow": workflow["name"],
            "started_at": datetime.now().isoformat(),
            "progress": []
        }
        
        # Handle different workflow types
        if tab_id == "tab6" and "llm_config" in data:
            # LLM Enhancement
            thread = Thread(target=self._execute_llm_enhancement, args=(workflow_id, data["llm_config"], workflow))
            thread.daemon = True
            thread.start()
            return {
                "status": "started",
                "workflow_id": workflow_id,
                "workflow": workflow["name"],
                "message": f"Started LLM enhancement with {data['llm_config']['provider']}/{data['llm_config']['model']}"
            }
        elif tab_id == "tab3" and "tiers" in data:
            # Taxonomy Generation
            # Use custom taxonomy name if provided
            taxonomy_name = data.get("taxonomy_name", "taxonomy")
            custom_workflow_id = f"{taxonomy_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            print(f"[API][DIAG] Starting taxonomy workflow id={custom_workflow_id} with taxonomy_name={taxonomy_name}")
            for tier_label, tier_files in data.get('tiers', {}).items():
                print(f"[API][DIAG] Tier '{tier_label}' file count={len(tier_files)}: {tier_files}")
            
            self.workflow_status[custom_workflow_id] = {
                "status": "starting",
                "workflow": workflow["name"],
                "started_at": datetime.now().isoformat(),
                "progress": []
            }
            
            thread = Thread(target=self._execute_taxonomy_generation, args=(custom_workflow_id, data["tiers"], workflow))
            thread.daemon = True
            thread.start()
            total_files = sum(len(files) for files in data["tiers"].values())
            return {
                "status": "started",
                "workflow_id": custom_workflow_id,
                "workflow": workflow["name"],
                "message": f"Started taxonomy generation with {total_files} file(s)"
            }
        else:
            # Regular file selection
            selected_files = data.get("files", [])
            if not selected_files:
                return {"error": "No files selected"}
            
            taxonomy_file = data.get("taxonomy")
            
            # Validate Tab 4 requires taxonomy selection
            if tab_id == "tab4" and not taxonomy_file:
                return {"error": "Taxonomy file is required for metadata enrichment. Please select a taxonomy."}
            
            # Execute in background thread
            thread = Thread(target=self._execute_workflow, args=(workflow_id, tab_id, selected_files, workflow, taxonomy_file))
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
        """Execute a workflow with selected files (runs in background thread)"""
        print(f"[API] _execute_workflow started for {workflow_id}, files: {files}")
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            script_path = workflow.get("script")
            print(f"[API] Script path: {script_path}")
            
            if not script_path or not Path(script_path).exists():
                print(f"[API] Script not found: {script_path}")
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
                return
            
            input_dir = workflow["input_dir"]
            output_dir = workflow["output_dir"]
            output_dir.mkdir(parents=True, exist_ok=True)
            
            successful = []
            failed = []
            
            # Process each file
            for file in files:
                try:
                    file_path = input_dir / file
                    self.workflow_status[workflow_id]["progress"].append(f"Processing: {file}")
                    
                    # Build command based on tab
                    if tab_id == "tab1":  # PDF to JSON
                        cmd = ["python3", str(script_path), str(file_path)]
                    elif tab_id == "tab2":  # Metadata Extraction
                        cmd = ["python3", str(script_path), "--input", str(file_path), "--auto-detect"]
                    elif tab_id == "tab3":  # Taxonomy Setup (handled separately via tiers)
                        continue
                    elif tab_id == "tab4":  # Metadata Enrichment
                        # Requires taxonomy file for scoped cross-book enrichment
                        if not taxonomy_file:
                            self.workflow_status[workflow_id]["status"] = "error"
                            self.workflow_status[workflow_id]["error"] = "Taxonomy file is required for metadata enrichment"
                            return
                        
                        taxonomy_path = WORKFLOWS_DIR / "taxonomy_setup" / "output" / taxonomy_file
                        
                        # Generate output path: input_metadata.json -> input_enriched_metadata.json
                        base_name = file.replace("_metadata.json", "")
                        output_path = output_dir / f"{base_name}_enriched_metadata.json"
                        
                        cmd = ["python3", str(script_path), "--input", str(file_path), "--taxonomy", str(taxonomy_path), "--output", str(output_path)]
                    elif tab_id == "tab5":  # Base Guideline
                        # Resolve to enriched metadata, fallback to metadata, then JSON
                        base_name = file.replace(".json", "")
                        
                        # Try enriched metadata first
                        enriched_path = WORKFLOWS_DIR / "metadata_enrichment" / "output" / f"{base_name}_enriched_metadata.json"
                        if enriched_path.exists():
                            resolved_path = enriched_path
                            self.workflow_status[workflow_id]["progress"].append(f"Using enriched metadata: {enriched_path.name}")
                        else:
                            # Try regular metadata
                            metadata_path = WORKFLOWS_DIR / "metadata_extraction" / "output" / f"{base_name}_metadata.json"
                            if metadata_path.exists():
                                resolved_path = metadata_path
                                self.workflow_status[workflow_id]["progress"].append(f"Using metadata: {metadata_path.name}")
                            else:
                                # Fallback to raw JSON
                                resolved_path = file_path
                                self.workflow_status[workflow_id]["progress"].append(f"Using raw JSON: {file}")
                        
                        cmd = ["python3", str(script_path), str(resolved_path)]
                        if taxonomy_file:
                            taxonomy_path = WORKFLOWS_DIR / "taxonomy_setup" / "output" / taxonomy_file
                            cmd.extend(["--taxonomy", str(taxonomy_path)])
                            self.workflow_status[workflow_id]["progress"].append(f"Using taxonomy: {taxonomy_file}")
                    else:
                        continue
                    
                    # Execute command with real-time output streaming
                    print(f"[API] Executing command: {' '.join(cmd)}")
                    
                    # Use stdbuf to force line buffering for real-time output
                    # Alternative: use -u flag for Python unbuffered mode
                    cmd_unbuffered = ["python3", "-u"] + cmd[1:]
                    
                    process = subprocess.Popen(
                        cmd_unbuffered,
                        cwd=str(BASE_DIR),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=0  # Unbuffered
                    )
                    
                    # Stream stdout in real-time with character-by-character reading
                    import select
                    current_line = ""
                    
                    while True:
                        # Check if process has finished
                        if process.poll() is not None:
                            # Read any remaining output
                            remaining = process.stdout.read()
                            if remaining:
                                current_line += remaining
                            break
                        
                        # Read available output (non-blocking)
                        ready, _, _ = select.select([process.stdout], [], [], 0.1)
                        if ready:
                            char = process.stdout.read(1)
                            if char:
                                if char == '\n':
                                    # Process complete line
                                    line = current_line.strip()
                                    if line:
                                        # Update progress for page processing lines (Tab 1: PDF to JSON)
                                        if "Processed" in line and "/" in line:
                                            # Update or add progress line
                                            if self.workflow_status[workflow_id]["progress"]:
                                                last_msg = self.workflow_status[workflow_id]["progress"][-1]
                                                if last_msg.startswith("  Processed"):
                                                    # Replace previous progress line
                                                    self.workflow_status[workflow_id]["progress"][-1] = f"  {line}"
                                                else:
                                                    self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                            else:
                                                self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                        # Tab 2: Metadata Extraction progress
                                        elif line.startswith("[") and "%" in line and "Processing Chapter" in line:
                                            # Chapter progress: [45.2%] Processing Chapter 5: Advanced Topics
                                            self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                        elif line.startswith("  Collected") and "characters" in line:
                                            # Text collection: "  Collected 45,231 characters from 23 pages"
                                            self.workflow_status[workflow_id]["progress"].append(f"    {line.strip()}")
                                        elif line.startswith("  Keywords:") or line.startswith("  Concepts:"):
                                            # Extraction results: "  Keywords: async, await, coroutine..."
                                            self.workflow_status[workflow_id]["progress"].append(f"    {line.strip()}")
                                        elif "Using" in line and "pre-defined chapters" in line:
                                            # Chapter detection: "   Using 42 pre-defined chapters from JSON"
                                            self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                        elif "Scanning pages for chapter markers" in line:
                                            # Fallback chapter detection
                                            self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                        # Show other important messages (Tab 1 and general)
                                        elif any(keyword in line for keyword in ["Detecting chapters", "Extracting chapter content", "Successfully converted", "Converting:", "Output to:", "Saved metadata", "Generating metadata"]):
                                            self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                    current_line = ""
                                elif char == '\r':
                                    # Carriage return - process current line as progress update
                                    line = current_line.strip()
                                    if line and "Processed" in line:
                                        if self.workflow_status[workflow_id]["progress"]:
                                            last_msg = self.workflow_status[workflow_id]["progress"][-1]
                                            if last_msg.startswith("  Processed"):
                                                self.workflow_status[workflow_id]["progress"][-1] = f"  {line}"
                                            else:
                                                self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                        else:
                                            self.workflow_status[workflow_id]["progress"].append(f"  {line}")
                                    current_line = ""
                                else:
                                    current_line += char
                    
                    # Get stderr
                    stderr_output = process.stderr.read()
                    returncode = process.returncode
                    
                    print(f"[API] Command completed with return code: {returncode}")
                    
                    if returncode == 0:
                        successful.append(file)
                        self.workflow_status[workflow_id]["progress"].append(f"✓ Completed: {file}")
                    else:
                        failed.append(file)
                        error_msg = stderr_output[:100] if stderr_output else "Unknown error"
                        self.workflow_status[workflow_id]["progress"].append(f"✗ Failed: {file} - {error_msg}")
                        
                except Exception as e:
                    failed.append(file)
                    self.workflow_status[workflow_id]["progress"].append(f"✗ Error: {file} - {str(e)}")
            
            # Update final status
            self.workflow_status[workflow_id]["status"] = "completed"
            self.workflow_status[workflow_id]["successful"] = successful
            self.workflow_status[workflow_id]["failed"] = failed
            self.workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
            self.workflow_status[workflow_id]["summary"] = f"Completed: {len(successful)} successful, {len(failed)} failed"
            
        except Exception as e:
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = str(e)
    
    def _execute_taxonomy_generation(self, workflow_id, tiers, workflow):
        """Generate concept taxonomy (runs in background thread)"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            self.workflow_status[workflow_id]["progress"].append("Analyzing books for concept extraction...")
            
            # Validate tiers
            if not tiers.get("architecture") or not tiers.get("implementation"):
                self.workflow_status[workflow_id]["status"] = "failed"
                self.workflow_status[workflow_id]["progress"].append("✗ Error: Architecture and Implementation tiers are required")
                return
            
            # Resolve files: prefer metadata, fallback to JSON
            # User selects "Book.json" but we want to use "Book_metadata.json" if it exists
            def resolve_to_metadata(json_filename):
                """Given 'Book.json', return path to 'Book_metadata.json' if exists, else 'Book.json'"""
                base_name = json_filename.replace(".json", "")
                
                # Try metadata first
                metadata_path = WORKFLOWS_DIR / "metadata_extraction" / "output" / f"{base_name}_metadata.json"
                if metadata_path.exists():
                    self.workflow_status[workflow_id]["progress"].append(f"  Using metadata: {metadata_path.name}")
                    return metadata_path
                
                # Fallback to raw JSON
                json_path = WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json" / json_filename
                if json_path.exists():
                    self.workflow_status[workflow_id]["progress"].append(f"  Using raw JSON: {json_filename}")
                    return json_path
                
                # File not found
                self.workflow_status[workflow_id]["progress"].append(f"  ✗ Warning: Neither metadata nor JSON found for {json_filename}")
                return None
            
            # Build tier data with resolved paths
            tier_books = {}
            for tier_name in ["architecture", "implementation", "practices"]:
                if tiers.get(tier_name):
                    resolved_files = []
                    for json_file in tiers[tier_name]:
                        resolved_path = resolve_to_metadata(json_file)
                        if resolved_path:
                            resolved_files.append(str(resolved_path))
                    if resolved_files:
                        tier_books[tier_name] = resolved_files
            
            # Generate output filename with custom name
            taxonomy_name = workflow_id.split('_')[0] if '_' in workflow_id else 'taxonomy'
            timestamp = datetime.now().strftime('%Y%m%d')
            output_filename = f"{taxonomy_name}_taxonomy_{timestamp}.json"
            
            script_path = workflow.get("script")
            if not script_path or not Path(script_path).exists():
                self.workflow_status[workflow_id]["status"] = "failed"
                self.workflow_status[workflow_id]["progress"].append(f"✗ Error: Script not found: {script_path}")
                return
            
            # Build command
            tier_json = json.dumps(tier_books)
            cmd = [
                "python3", 
                str(script_path),
                "--tiers", tier_json,
                "--output", output_filename
            ]
            
            self.workflow_status[workflow_id]["progress"].append(f"Extracting concepts from {sum(len(b) for b in tier_books.values())} metadata files...")
            
            # Execute script
            result = subprocess.run(
                cmd,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )
            
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
            
        except Exception as e:
            self.workflow_status[workflow_id]["status"] = "error"
            self.workflow_status[workflow_id]["error"] = str(e)
    
    def _execute_llm_enhancement(self, workflow_id, llm_config, workflow):
        """Execute LLM enhancement (runs in background thread)"""
        try:
            self.workflow_status[workflow_id]["status"] = "running"
            script_path = workflow.get("script")
            
            if not script_path or not Path(script_path).exists():
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
                return
            
            # Build command with LLM config
            guideline_path = workflow["input_dir"] / llm_config["guideline"]
            taxonomy_path = WORKFLOWS_DIR / "taxonomy_setup" / "output" / llm_config["taxonomy"]
            
            self.workflow_status[workflow_id]["progress"].append(f"Guideline: {llm_config['guideline']}")
            self.workflow_status[workflow_id]["progress"].append(f"Taxonomy: {llm_config['taxonomy']}")
            self.workflow_status[workflow_id]["progress"].append(f"Provider: {llm_config['provider']}")
            self.workflow_status[workflow_id]["progress"].append(f"Model: {llm_config['model']}")
            
            # Set environment variables for LLM
            env = os.environ.copy()
            env["LLM_PROVIDER"] = llm_config["provider"]
            env["LLM_MODEL"] = llm_config["model"]
            
            cmd = [
                "python3", str(script_path),
                "--guideline", str(guideline_path),
                "--taxonomy", str(taxonomy_path)
            ]
            
            self.workflow_status[workflow_id]["progress"].append("Starting LLM enhancement...")
            
            # Execute command
            result = subprocess.run(
                cmd,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                env=env
            )
            
            if result.returncode == 0:
                self.workflow_status[workflow_id]["status"] = "completed"
                self.workflow_status[workflow_id]["progress"].append("✓ LLM enhancement completed")
                self.workflow_status[workflow_id]["output"] = result.stdout[:500]
            else:
                self.workflow_status[workflow_id]["status"] = "error"
                self.workflow_status[workflow_id]["error"] = result.stderr
                self.workflow_status[workflow_id]["progress"].append(f"✗ Enhancement failed")
            
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
