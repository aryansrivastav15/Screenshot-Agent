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
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from PIL import Image

# Load environment variables
load_dotenv()

console = Console()

def upload_to_drive(filepath, filename):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    # Use absolute path for credentials.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'credentials.json')
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype='image/png')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

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
        console.print(f"[green]Screenshot saved locally: {filepath}[/green]")
        # Upload to Google Drive
        file_id = upload_to_drive(filepath, filename)
        console.print(f"[cyan]Screenshot uploaded to Google Drive with file ID: {file_id}[/cyan]")
        return f"Google Drive file ID: {file_id}"
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
