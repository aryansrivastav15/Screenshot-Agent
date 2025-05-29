# AI Screenshot Agent

A Python-based screenshot tool that uses CrewAI and OpenAI to manage screenshots.

## Setup

1. Install dependencies:
```bash
pip install pyautogui keyboard rich crewai python-dotenv Pillow
```

2. Create a `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the script:
```bash
python screenshot_agent.py
```

### Menu Options
1. Take Single Screenshot
2. Start Continuous Capture
3. Stop Continuous Capture
4. View Screenshot History
5. Exit

Screenshots are saved to your desktop. 
