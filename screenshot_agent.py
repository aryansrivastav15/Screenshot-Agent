from dotenv import load_dotenv
import os
load_dotenv()

# Explicitly set the API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
os.environ['OPENAI_API_KEY'] = api_key

import pyautogui
import os
import platform
from datetime import datetime
from crewai import Agent, Task, Crew
from rich.console import Console
from rich.prompt import Prompt
import keyboard
import time

class ScreenshotModel:
    """Model: Handles data and business logic"""
    def __init__(self):
        self.screenshot_dir = self._get_desktop_path()
        self.screenshot_history = []
        
    def _get_desktop_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # macOS and Linux
            return os.path.join(os.path.expanduser("~"), "Desktop")
            
    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        self.screenshot_history.append({
            'timestamp': timestamp,
            'filepath': filepath
        })
        
        return filepath
        
    def get_screenshot_history(self):
        return self.screenshot_history

class ScreenshotContext:
    """Context: Manages state and environment"""
    def __init__(self, model):
        self.model = model
        self.is_capturing = False
        self.console = Console()
        
    def start_capture(self):
        self.is_capturing = True
        self.console.print("[green]Starting continuous capture...[/green]")
        
    def stop_capture(self):
        self.is_capturing = False
        self.console.print("[red]Stopping continuous capture...[/red]")
        
    def capture_loop(self):
        while self.is_capturing:
            self.model.take_screenshot()
            time.sleep(1)  # Wait 1 second between captures

class ScreenshotProtocol:
    """Protocol: Defines communication and interface rules"""
    def __init__(self):
        self.model = ScreenshotModel()
        self.context = ScreenshotContext(self.model)
        self.console = Console()
        self.setup_crew()
        # self.setup_keyboard_listeners()  # Disabled hotkeys for menu-only mode
        
    def setup_crew(self):
        # Define the screenshot agent
        self.screenshot_agent = Agent(
            role="Screenshot Assistant",
            goal="Take and manage screenshots efficiently",
            backstory="You are an AI assistant specialized in managing screenshots and visual data capture.",
            verbose=True,
            allow_delegation=False
        )
        
        # Define the screenshot task
        screenshot_task = Task(
            description="Take a screenshot and save it to the desktop",
            agent=self.screenshot_agent,
            expected_output="Confirmation that the screenshot was saved with the file path."
        )
        
        # Create the crew
        self.crew = Crew(
            agents=[self.screenshot_agent],
            tasks=[screenshot_task],
            verbose=True
        )
        
    def setup_keyboard_listeners(self):
        keyboard.add_hotkey('alt+shift+1', self.take_single_screenshot)
        keyboard.add_hotkey('alt+shift+2', self.start_continuous_capture)
        keyboard.add_hotkey('alt+shift+3', self.stop_continuous_capture)
        
    def take_single_screenshot(self):
        try:
            filepath = self.model.take_screenshot()
            self.console.print(f"[green]Screenshot saved: {filepath}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error taking screenshot: {str(e)}[/red]")
            
    def start_continuous_capture(self):
        if not self.context.is_capturing:
            self.context.start_capture()
            import threading
            capture_thread = threading.Thread(target=self.context.capture_loop)
            capture_thread.daemon = True
            capture_thread.start()
            
    def stop_continuous_capture(self):
        if self.context.is_capturing:
            self.context.stop_capture()
            
    def show_menu(self):
        while True:
            self.console.print("\n[bold cyan]Screenshot Agent Menu[/bold cyan]")
            self.console.print("1. Take Single Screenshot")
            self.console.print("2. Start Continuous Capture")
            self.console.print("3. Stop Continuous Capture")
            self.console.print("4. View Screenshot History")
            self.console.print("5. Exit")
            
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.take_single_screenshot()
            elif choice == "2":
                self.start_continuous_capture()
            elif choice == "3":
                self.stop_continuous_capture()
            elif choice == "4":
                history = self.model.get_screenshot_history()
                if history:
                    self.console.print("\n[bold]Screenshot History:[/bold]")
                    for item in history:
                        self.console.print(f"Time: {item['timestamp']}, File: {item['filepath']}")
                else:
                    self.console.print("[yellow]No screenshots taken yet.[/yellow]")
            elif choice == "5":
                self.console.print("[red]Exiting...[/red]")
                break

if __name__ == "__main__":
    agent = ScreenshotProtocol()
    agent.show_menu()
    