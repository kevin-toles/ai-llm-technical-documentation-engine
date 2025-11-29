# TPM Job Runner UI

Recreated front-end UI from the original TPM Job Finder application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
cd ui
python main.py
```

3. Open browser to:
```
http://127.0.0.1:8000
```

## Features

- **macOS-style window** with traffic light controls
- **Form controls** matching original TPM UI:
  - Job Filtering Mode dropdown
  - Work Arrangement dropdown
  - API Aggregators checkboxes
  - Browser Scrapers checkboxes
  - LLM Providers checkboxes
  - Operation selection dropdown
  - File path inputs
- **Real-time status updates** using HTMX
- **Progress tracking** with status, current step, and error log
- **Action buttons**: Execute, Stop, Clear

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML + HTMX
- **Styling**: Pure CSS (macOS Big Sur style)
- **Templates**: Jinja2

## File Structure

```
ui/
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── templates/
│   ├── index.html          # Main UI template
│   └── partials/
│       └── status.html     # Status section partial
└── static/
    ├── css/
    │   └── style.css       # macOS-style CSS
    └── js/
        └── (future JS files)
```

## Usage

1. Select your job filtering mode and work arrangement
2. Choose aggregators, scrapers, and LLM providers
3. Select the operation to execute
4. Provide file paths for resume and output
5. Click **Execute** to run the workflow
6. Monitor progress in the status section
7. Use **Stop** to cancel or **Clear** to reset logs

## API Endpoints

- `GET /` - Main UI
- `POST /execute` - Start workflow
- `POST /stop` - Stop running workflow
- `POST /clear` - Clear logs
- `GET /status` - Get current status (polled every 1s)
