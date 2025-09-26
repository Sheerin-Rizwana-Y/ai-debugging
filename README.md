# AI Debugging Toolkit

A modular, backend-first debugging assistant powered by FastAPI and Python ML workflows. This toolkit is designed to help developers trace, analyze, and resolve runtime issues using intelligent suggestions and structured logs.

##  Features

- **Trace Analyzer**: Parses stack traces and error logs to identify root causes.
- **ML-Powered Suggestions**: Uses trained models to recommend fixes based on historical error patterns.
- **Modular Architecture**: Clean folder structure for scalable backend development.
- **Log Ingestion Engine**: Accepts structured/unstructured logs via API and preprocesses them for analysis.
- **Test Harness**: Validate endpoints with sample logs and trace inputs.

## Project Structure
ai-debugging/ 
├── app/ │  
 ├── main.py             # FastAPI entry point 
 │   ├── api/                 # Route definitions 
 │   ├── core/                # Configs and constants 
 │   ├── models/              # Pydantic schemas 
 │   ├── services/            # ML logic and trace analysis 
 │   └── utils/               # Helper functions 
 ├── tests/                   # Unit and integration tests 
 ├── requirements.txt         # Python dependencies 
 └── README.md                # Project overview


##  Setup

```bash
# Clone the repo
git clone https://github.com/Sheerin-Rizwana-Y/ai-debugging.git
cd ai-debugging

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
