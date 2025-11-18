"""
Simple UI for LLM Document Enhancer workflows
Each tab allows file selection and workflow execution
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import os
import httpx

app = FastAPI(title="LLM Document Enhancer")

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
async def run_workflow(tab_id: str, request: Request):
    """Execute workflow with selected files"""
    data = await request.json()
    
    if tab_id not in WORKFLOWS:
        return {"error": "Invalid tab"}
    
    workflow = WORKFLOWS[tab_id]
    
    # Handle LLM tab with configuration
    if tab_id == "tab7" and "llm_config" in data:
        llm_config = data["llm_config"]
        
        return {
            "status": "ready",
            "workflow": workflow["name"],
            "llm_config": llm_config,
            "message": f"Would enhance using {llm_config['provider']}/{llm_config['model']}"
        }
    
    # Handle taxonomy tab with tiers
    if tab_id == "tab6" and "tiers" in data:
        tier_data = data["tiers"]
        total_files = sum(len(files) for files in tier_data.values())
        tier_summary = ", ".join([f"{tier}: {len(files)}" for tier, files in tier_data.items()])
        
        return {
            "status": "ready",
            "workflow": workflow["name"],
            "tiers": tier_data,
            "message": f"Would create taxonomy from {total_files} file(s)\n{tier_summary}"
        }
    
    # Regular file selection
    selected_files = data.get("files", [])
    
    return {
        "status": "ready",
        "workflow": workflow["name"],
        "files": selected_files,
        "script": str(workflow.get("script", "Not implemented")),
        "message": f"Would process {len(selected_files)} file(s)"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
