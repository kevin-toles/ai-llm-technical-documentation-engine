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

# Service Layer imports (Architecture Patterns Ch. 4)
from ui.async_workflow_services import (
    AsyncWorkflowExecutionService,
    AsyncFileListService,
    AsyncTaxonomyGenerationService,
    JSON_EXT,
    JSON_GLOB,
    MD_EXT,
    PDF_EXT
)

app = FastAPI(title="LLM Document Enhancer")

# Store workflow execution status
workflow_status = {}

# Base paths
UI_DIR = Path(__file__).parent
BASE_DIR = UI_DIR.parent
WORKFLOWS_DIR = BASE_DIR / "workflows"

# Mount static files
app.mount("/static", StaticFiles(directory=str(UI_DIR / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(UI_DIR / "templates"))

# Define workflow configurations
WORKFLOWS = {
    "tab1": {
        "name": "PDF to JSON",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "input",
        "input_ext": PDF_EXT,
        "output_dir": WORKFLOWS_DIR / "pdf_to_json" / "output",
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
        "name": "Metadata Enrichment",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "metadata_enrichment" / "output",
        "script": WORKFLOWS_DIR / "metadata_enrichment" / "scripts" / "generate_chapter_metadata.py"
    },
    "tab4": {
        "name": "Taxonomy Setup",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "taxonomy_setup" / "output",
        "script": None  # To be created
    },
    "tab5": {
        "name": "Base Guideline",
        "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
        "input_ext": JSON_EXT,
        "output_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "script": WORKFLOWS_DIR / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py",
        "requires_taxonomy": True
    },
    "tab6": {
        "name": "LLM Enhancement",
        "input_dir": WORKFLOWS_DIR / "base_guideline_generation" / "output",
        "input_ext": JSON_EXT,
        "exclude_dirs": ["chapter_summaries"],
        "output_dir": WORKFLOWS_DIR / "llm_enhancement" / "output",
        "script": WORKFLOWS_DIR / "llm_enhancement" / "scripts" / "integrate_llm_enhancements.py",
        "requires_taxonomy": True,
        "requires_llm": True
    }
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with 6 workflow tabs"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "workflows": WORKFLOWS
    })


@app.get("/files/{tab_id}")
async def get_files(tab_id: str):
    """Get list of files for workflow (refactored: CC 16 → 3)"""
    if tab_id not in WORKFLOWS:
        return {"error": "Invalid tab"}
    
    workflow = WORKFLOWS[tab_id]
    exclude_dirs = workflow.get("exclude_dirs", [])
    files = AsyncFileListService.get_files_for_workflow(
        workflow["input_dir"], 
        workflow["input_ext"],
        exclude_dirs=exclude_dirs
    )
    
    response = {
        "files": files,
        "input_dir": str(workflow["input_dir"])
    }
    
    # Add tab-specific metadata
    if tab_id == "tab5":
        response.update(_get_tab5_metadata())
    elif tab_id == "tab4":
        response.update(_get_tab4_metadata())
    elif tab_id == "tab6":
        response.update(await _get_tab6_metadata())
    else:
        response["output_dir"] = str(workflow["output_dir"])
    
    return response


def _get_tab5_metadata():
    """Get Base Guideline tab metadata with validated taxonomy files"""
    taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
    taxonomy_files = AsyncFileListService.get_taxonomy_files_with_validation(taxonomy_dir)
    return {"taxonomy_files": taxonomy_files}


def _get_tab4_metadata():
    """Get Taxonomy Setup tab metadata with tier definitions"""
    return {
        "supports_tiers": True,
        "tiers": [
            {"id": "architecture", "name": "Architecture Spine", "priority": 1},
            {"id": "implementation", "name": "Implementation", "priority": 2},
            {"id": "practices", "name": "Engineering Practices", "priority": 3}
        ]
    }


async def _get_tab6_metadata():
    """Get LLM Enhancement tab metadata with taxonomy files and providers"""
    taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
    taxonomy_files = AsyncFileListService.get_taxonomy_files(taxonomy_dir)
    providers_data = await get_llm_providers()
    return {
        "taxonomy_files": taxonomy_files,
        "llm_providers": providers_data
    }


@app.get("/taxonomy-files")
async def get_taxonomy_files():
    """Get list of available taxonomy files"""
    taxonomy_dir = WORKFLOWS_DIR / "taxonomy_setup" / "output"
    
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
                # Previous Generation (Still Available)
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
    if tab_id == "tab6" and "llm_config" in data:
        background_tasks.add_task(execute_llm_enhancement, workflow_id, data["llm_config"], workflow)
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "workflow": workflow["name"],
            "message": f"Started LLM enhancement with {data['llm_config']['provider']}/{data['llm_config']['model']}"
        }
    
    # Handle taxonomy tab with tiers
    if tab_id == "tab4" and "tiers" in data:
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
    
    # Get taxonomy file if provided (for workflows that require it)
    taxonomy_file = data.get("taxonomy")
    
    # Execute workflow in background
    background_tasks.add_task(execute_workflow, workflow_id, tab_id, selected_files, workflow, taxonomy_file)
    
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


async def execute_workflow(workflow_id: str, tab_id: str, files: list, workflow: dict, taxonomy_file: str = None):
    """Execute workflow (refactored: CC 21 → 2)"""
    service = AsyncWorkflowExecutionService(workflow_status, BASE_DIR, WORKFLOWS_DIR)
    await service.execute(workflow_id, tab_id, files, workflow, taxonomy_file)


async def execute_taxonomy_generation(workflow_id: str, tiers: dict, workflow: dict):
    """Generate concept taxonomy (refactored: CC 12 → 2)"""
    service = AsyncTaxonomyGenerationService(workflow_status, BASE_DIR, WORKFLOWS_DIR)
    await service.execute(workflow_id, tiers, workflow)


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
        taxonomy_path = WORKFLOWS_DIR / "taxonomy_setup" / "output" / llm_config["taxonomy"]
        
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
            workflow_status[workflow_id]["progress"].append("✗ Enhancement failed")
        
        workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        workflow_status[workflow_id]["status"] = "error"
        workflow_status[workflow_id]["error"] = str(e)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
