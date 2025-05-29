# CrewAI Web Screenshot Agent

This project is a command-line tool that uses CrewAI and Selenium to take screenshots of websites and save them to your desktop. The agent is orchestrated by CrewAI and requires an OpenAI API key for operation.

## Features

- Takes screenshots of any website you specify.
- Saves screenshots to your desktop with a timestamped filename.
- Command-line interface for easy use.

## Requirements

- Python 3.8+
- Google Chrome browser installed
- ChromeDriver (automatically managed)
- OpenAI API key with available quota

## Installation

1. **Clone the repository or copy the script to your machine.**

2. **Install dependencies:**
   ```bash
   pip install selenium webdriver-manager python-dotenv rich crewai
   ```

3. **Set up your OpenAI API key:**
   - Create a file named `.env` in the same directory as `crew_web_screenshot_agent.py`.
   - Add your OpenAI API key (starts with `sk-...`):
     ```
     OPENAI_API_KEY=sk-...
     ```
   - You can get your API key from https://platform.openai.com/account/api-keys

## Usage

Run the script from your terminal:
```bash
python3 crew_web_screenshot_agent.py
```

You will see:
```
CrewAI Web Screenshot Agent
Enter a website URL to screenshot (or type 'exit' to quit):
```
- Enter the URL of the website you want to screenshot (e.g., `youtube.com`).
- The screenshot will be saved to your desktop.
- Type `exit` to quit.

## Troubleshooting

- **AuthenticationError or Invalid API Key:**  
  Make sure your `.env` file contains a valid OpenAI API key (starts with `sk-...`).

- **RateLimitError or Insufficient Quota:**  
  Your OpenAI account has run out of credits or quota. Visit https://platform.openai.com/account/billing to add credits.

- **Google Chrome not found:**  
  Make sure Google Chrome is installed on your system.

- **Other Selenium/ChromeDriver errors:**  
  Ensure your Chrome browser is up to date.

## Customization

- To use a different LLM provider (like Gemini), you will need to write a custom integration. CrewAI currently only supports OpenAI out of the box.

## License

MIT License
