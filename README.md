# MCP Screenshot Agent

## Overview
This project is an automated agent that uses Playwright MCP and an LLM (Groq or OpenAI) to:
- Open a browser and navigate to any website you specify
- Take a screenshot and save it to your Desktop
- Automatically upload the screenshot to your Google Drive

## Features
- **Cross-platform:** Works on any OS (macOS, Windows, Linux)
- **Flexible LLM backend:** Supports Groq (Llama 3) or OpenAI (GPT-3.5 Turbo)
- **Google Drive integration:** Uploads screenshots directly to your Drive
- **Configurable via JSON and .env files**

## Setup

### 1. Clone the repository and enter the directory
```bash
git clone <your-repo-url>
cd mcp_screenshot_Agent
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
# Or, if requirements.txt is missing:
pip install python-dotenv langchain-groq langchain-openai mcp-use google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 4. Environment Variables
Create a `.env` file in the project root with your API keys:
```
# For Groq (Llama 3)
GROQ_API_KEY=your-groq-api-key
# For OpenAI (GPT-3.5 Turbo)
OPENAI_API_KEY=sk-...
```

### 5. Google Drive Integration
- Go to the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Create an OAuth 2.0 Client ID (Desktop app)
- Download `credentials.json` and place it in your project directory
- The first time you run the script, a browser will open for authentication

## Usage

### Run the Agent
```bash
python mcp_screenshot.py
```
- Enter the website URL when prompted (e.g., `https://example.com`)
- The screenshot will be saved as `screenshot.png` on your Desktop
- The screenshot will also be uploaded to your Google Drive

### Configuration
- MCP/Playwright config is in `playwright_mcp.json`
- LLM model can be switched in `mcp_screenshot.py` (Groq or OpenAI)

## Troubleshooting
- **No API key error:** Check your `.env` file and restart your terminal
- **Quota errors:** Check your Groq or OpenAI usage and billing
- **Google Drive upload issues:** Ensure `credentials.json` is present and you complete the browser authentication
- **Screenshot not saving:** Check Desktop permissions and path

## License
MIT License 