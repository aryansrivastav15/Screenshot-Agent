from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv()

console = Console()

def take_website_screenshot(url: str) -> str:
    save_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(save_dir, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        console.print(f"[yellow]Navigating to {url}...[/yellow]")
        driver.get(url)
        driver.implicitly_wait(5)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crew_web_screenshot_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)
        driver.save_screenshot(filepath)
        console.print(f"[green]Screenshot saved: {filepath}[/green]")
        return filepath
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return f"Error: {e}"
    finally:
        driver.quit()

# Define the agent
screenshot_agent = Agent(
    role="Web Screenshot Agent",
    goal="Take screenshots of websites as instructed by the user.",
    backstory="You are an AI agent that can take screenshots of any website using Selenium and save them to the user's desktop.",
    verbose=True
)

def main():
    console.print("[bold cyan]CrewAI Web Screenshot Agent[/bold cyan]")
    while True:
        url = Prompt.ask("Enter a website URL to screenshot (or type 'exit' to quit)")
        if url.lower() == 'exit':
            break
        # Instead of a Tool, just call the function directly in the task
        def screenshot_task_func():
            return take_website_screenshot(url)
        task = Task(
            description=f"Take a screenshot of {url}",
            agent=screenshot_agent,
            expected_output="Path to the saved screenshot.",
            func=screenshot_task_func
        )
        crew = Crew(
            agents=[screenshot_agent],
            tasks=[task],
            process="sequential"
        )
        result = crew.kickoff()
        console.print(f"[blue]Result: {result}[/blue]")

if __name__ == "__main__":
    main() 