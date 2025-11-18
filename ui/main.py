"""
Simple UI for LLM Document Enhancer workflows
Each tab allows file selection and workflow execution
"""
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import os
import httpx
import asyncio
import json
from datetime import datetime

app = FastAPI(title="LLM Document Enhancer")

# Store workflow execution status
workflow_status = {}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Base paths
BASE_DIR = Path(__file__).parent.parent
WORKFLOWS_DIR = BASE_DIR / "workflows"
INPUTS_DIR = BASE_DIR / "inputs"

# Define workflow configurations
WORKFLOWS = {
    "tab1": {
        "name": "PDF to JSON",
        "input_dir": INPUTS_DIR / "pdfs",
        "input_ext": ".pdf",
        "output_dir": WORKFLOWS_DIR / "pdf_to_json" / "output",
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
        "name": "Metadata Enrichment",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "metadata_enrichment" / "output",
        "script": WORKFLOWS_DIR / "metadata_enrichment" / "scripts" / "generate_chapter_metadata.py"
    },
    "tab4": {
        "name": "Cache Merge",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "metadata_cache_merge" / "output",
        "script": WORKFLOWS_DIR / "metadata_cache_merge" / "scripts" / "merge_metadata_to_cache.py"
    },
    "tab5": {
        "name": "Base Guideline",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": ".json",
        "output_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "script": BASE_DIR / "Chapter Summaries" / "chapter_generator_all_text.py",
        "requires_taxonomy": True
    },
    "tab6": {
        "name": "Taxonomy Setup",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": ".json",
        "output_dir": INPUTS_DIR / "taxonomy",
        "script": None  # To be created
    },
    "tab7": {
        "name": "LLM Enhancement",
        "input_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output" / "chapter_summaries",
        "input_ext": ".md",
        "output_dir": WORKFLOWS_DIR / "llm_enhancement" / "output",
        "script": WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "integrate_llm_enhancements.py",
        "requires_taxonomy": True,
        "requires_llm": True
    }
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with 7 workflow tabs"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "workflows": WORKFLOWS
    })


@app.get("/files/{tab_id}")
async def get_files(tab_id: str):
    """Get list of files available for the workflow"""
    if tab_id not in WORKFLOWS:
        return {"error": "Invalid tab"}
    
    workflow = WORKFLOWS[tab_id]
    input_dir = workflow["input_dir"]
    
    if not input_dir.exists():
        return {"files": [], "input_dir": str(input_dir)}
    
    # Get all files with matching extension
    files = [f.name for f in input_dir.glob(f"*{workflow['input_ext']}")]
    
    # Special handling for taxonomy tab - return with tier support
    if tab_id == "tab6":
        return {
            "files": sorted(files),
            "input_dir": str(input_dir),
            "supports_tiers": True,
            "tiers": [
                {"id": "architecture", "name": "Architecture Spine"},
                {"id": "implementation", "name": "Implementation"},
                {"id": "practices", "name": "Engineering Practices"}
            ]
        }
    
    # Special handling for LLM tab - return taxonomy files and LLM options
    if tab_id == "tab7":
        taxonomy_dir = INPUTS_DIR / "taxonomy"
        taxonomy_files = []
        if taxonomy_dir.exists():
            taxonomy_files = [f.name for f in taxonomy_dir.glob("*.json")]
        
        # Fetch providers dynamically
        providers_data = await get_llm_providers()
        
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


@app.get("/taxonomy-files")
async def get_taxonomy_files():
    """Get list of available taxonomy files"""
    taxonomy_dir = INPUTS_DIR / "taxonomy"
    
    if not taxonomy_dir.exists():
        return {"files": []}
    
    files = [f.name for f in taxonomy_dir.glob("*.json")]
    return {"files": sorted(files)}


async def fetch_openai_models():
    """Fetch available models from OpenAI API (free, no token cost)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Return default models if no API key
        return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()
                # Filter to only chat models (gpt-4*, gpt-3.5*)
                models = [m["id"] for m in data.get("data", []) 
                         if m["id"].startswith(("gpt-4", "gpt-3.5"))]
                return sorted(models, reverse=True)
    except Exception:
        pass
    
    # Fallback to known models
    return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]


@app.get("/llm-providers")
async def get_llm_providers():
    """Get available LLM providers and their models"""
    openai_models = await fetch_openai_models()
    
    return {
        "openai": {
            "name": "OpenAI",
            "models": openai_models
        },
        "anthropic": {
            "name": "Anthropic",
            "models": [
                # Current Models (Recommended)
                "claude-sonnet-4-5-20250929",  # Latest & Recommended
                "claude-haiku-4-5-20251001",   # Fastest
                "claude-opus-4-1-20250805",    # Most Powerful
                # Legacy Models (Still Available)
                "claude-sonnet-4-20250514",
                "claude-opus-4-20250514", 
                "claude-3-7-sonnet-20250219",
                "claude-3-5-haiku-20241022",
                "claude-3-haiku-20240307"
            ]
        }
    }


@app.post("/run/{tab_id}")
async def run_workflow(tab_id: str, request: Request, background_tasks: BackgroundTasks):
    """Execute workflow with selected files"""
    data = await request.json()
    
    if tab_id not in WORKFLOWS:
        return {"error": "Invalid tab"}
    
    workflow = WORKFLOWS[tab_id]
    workflow_id = f"{tab_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize status
    workflow_status[workflow_id] = {
        "status": "starting",
        "workflow": workflow["name"],
        "started_at": datetime.now().isoformat(),
        "progress": []
    }
    
    # Handle LLM tab with configuration
    if tab_id == "tab7" and "llm_config" in data:
        background_tasks.add_task(execute_llm_enhancement, workflow_id, data["llm_config"], workflow)
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started LLM enhancement with {data['llm_config']['provider']}/{data['llm_config']['model']}"
        }
    
    # Handle taxonomy tab with tiers
    if tab_id == "tab6" and "tiers" in data:
        background_tasks.add_task(execute_taxonomy_generation, workflow_id, data["tiers"], workflow)
        total_files = sum(len(files) for files in data["tiers"].values())
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started taxonomy generation with {total_files} file(s)"
        }
    
    # Regular file selection
    selected_files = data.get("files", [])
    if not selected_files:
        return {"error": "No files selected"}
    
    # Execute workflow in background
    background_tasks.add_task(execute_workflow, workflow_id, tab_id, selected_files, workflow)
    
    return {
        "status": "started",
        "workflow_id": workflow_id,
        "workflow": workflow["name"],
        "message": f"Started processing {len(selected_files)} file(s)"
    }


@app.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get status of a running workflow"""
    if workflow_id not in workflow_status:
        return {"error": "Workflow not found"}
    
    return workflow_status[workflow_id]


async def execute_workflow(workflow_id: str, tab_id: str, files: list, workflow: dict):
    """Execute a workflow with selected files"""
    try:
        workflow_status[workflow_id]["status"] = "running"
        script_path = workflow.get("script")
        
        if not script_path or not Path(script_path).exists():
            workflow_status[workflow_id]["status"] = "error"
            workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
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
                workflow_status[workflow_id]["progress"].append(f"Processing: {file}")
                
                # Build command based on tab
                if tab_id == "tab1":  # PDF to JSON
                    cmd = ["python3", str(script_path), str(file_path)]
                elif tab_id == "tab2":  # Metadata Extraction
                    cmd = ["python3", str(script_path), "--input", str(file_path), "--auto-detect"]
                elif tab_id == "tab3":  # Metadata Enrichment
                    cmd = ["python3", str(script_path), "--input", str(file_path)]
                elif tab_id == "tab4":  # Cache Merge
                    cmd = ["python3", str(script_path), "--input", str(file_path)]
                elif tab_id == "tab5":  # Base Guideline
                    cmd = ["python3", str(script_path), str(file_path)]
                else:
                    continue
                
                # Execute command
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(BASE_DIR)
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    successful.append(file)
                    workflow_status[workflow_id]["progress"].append(f"✓ Completed: {file}")
                else:
                    failed.append(file)
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    workflow_status[workflow_id]["progress"].append(f"✗ Failed: {file} - {error_msg[:100]}")
                    
            except Exception as e:
                failed.append(file)
                workflow_status[workflow_id]["progress"].append(f"✗ Error: {file} - {str(e)}")
        
        # Update final status
        workflow_status[workflow_id]["status"] = "completed"
        workflow_status[workflow_id]["successful"] = successful
        workflow_status[workflow_id]["failed"] = failed
        workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        workflow_status[workflow_id]["summary"] = f"Completed: {len(successful)} successful, {len(failed)} failed"
        
    except Exception as e:
        workflow_status[workflow_id]["status"] = "error"
        workflow_status[workflow_id]["error"] = str(e)


async def execute_taxonomy_generation(workflow_id: str, tiers: dict, workflow: dict):
    """Generate taxonomy from tier data"""
    try:
        workflow_status[workflow_id]["status"] = "running"
        workflow_status[workflow_id]["progress"].append("Building taxonomy structure...")
        
        # Create taxonomy JSON structure
        taxonomy = {
            "name": "Generated Taxonomy",
            "created_at": datetime.now().isoformat(),
            "tiers": {
                "architecture": {"priority": 1, "books": tiers.get("architecture", [])},
                "implementation": {"priority": 2, "books": tiers.get("implementation", [])},
                "practices": {"priority": 3, "books": tiers.get("practices", [])}
            }
        }
        
        # Save taxonomy file
        output_dir = workflow["output_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f"taxonomy_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(taxonomy, f, indent=2)
        
        workflow_status[workflow_id]["status"] = "completed"
        workflow_status[workflow_id]["output_file"] = str(output_file)
        workflow_status[workflow_id]["progress"].append(f"✓ Taxonomy saved to: {output_file.name}")
        workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        workflow_status[workflow_id]["status"] = "error"
        workflow_status[workflow_id]["error"] = str(e)


async def execute_llm_enhancement(workflow_id: str, llm_config: dict, workflow: dict):
    """Execute LLM enhancement workflow"""
    try:
        workflow_status[workflow_id]["status"] = "running"
        script_path = workflow.get("script")
        
        if not script_path or not Path(script_path).exists():
            workflow_status[workflow_id]["status"] = "error"
            workflow_status[workflow_id]["error"] = f"Script not found: {script_path}"
            return
        
        # Build command with LLM config
        guideline_path = workflow["input_dir"] / llm_config["guideline"]
        taxonomy_path = INPUTS_DIR / "taxonomy" / llm_config["taxonomy"]
        
        workflow_status[workflow_id]["progress"].append(f"Guideline: {llm_config['guideline']}")
        workflow_status[workflow_id]["progress"].append(f"Taxonomy: {llm_config['taxonomy']}")
        workflow_status[workflow_id]["progress"].append(f"Provider: {llm_config['provider']}")
        workflow_status[workflow_id]["progress"].append(f"Model: {llm_config['model']}")
        
        # Set environment variables for LLM
        env = os.environ.copy()
        env["LLM_PROVIDER"] = llm_config["provider"]
        env["LLM_MODEL"] = llm_config["model"]
        
        cmd = [
            "python3", str(script_path),
            "--guideline", str(guideline_path),
            "--taxonomy", str(taxonomy_path)
        ]
        
        workflow_status[workflow_id]["progress"].append("Starting LLM enhancement...")
        
        # Execute command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=str(BASE_DIR)
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            workflow_status[workflow_id]["status"] = "completed"
            workflow_status[workflow_id]["progress"].append("✓ LLM enhancement completed")
            workflow_status[workflow_id]["output"] = stdout.decode()[:500]  # First 500 chars
        else:
            workflow_status[workflow_id]["status"] = "error"
            workflow_status[workflow_id]["error"] = stderr.decode()
            workflow_status[workflow_id]["progress"].append(f"✗ Enhancement failed")
        
        workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        workflow_status[workflow_id]["status"] = "error"
        workflow_status[workflow_id]["error"] = str(e)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
