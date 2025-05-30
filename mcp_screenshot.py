import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Use OpenAI LLM
from mcp_use import MCPAgent, MCPClient
import json
import mcp_use
import pathlib
import functools

# --- Google Drive Upload Function ---
# Requires: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Also requires a credentials.json file from Google Cloud Console in this directory.
def upload_to_gdrive(local_file_path, drive_filename=None, folder_id=None):
    """
    Uploads a file to Google Drive.
    :param local_file_path: Path to the local file to upload.
    :param drive_filename: Name for the file in Google Drive (optional).
    :param folder_id: Google Drive folder ID to upload into (optional).
    """
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle

    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    # Token stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': drive_filename or pathlib.Path(local_file_path).name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(local_file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded to Google Drive with ID: {file.get('id')}")

async def main(website_url, output_path):
    # Load environment variables
    load_dotenv()
    mcp_use.set_debug(1)  # Reduce debug level
    # Load config from JSON file
    with open("playwright_mcp.json", "r") as f:
        config = json.load(f)
    client = MCPClient.from_dict(config)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    # System prompt to guide the agent
    system_prompt = (
        "You are an agent that can use ONLY the browser tools provided by Playwright MCP. "
        "To take a screenshot of a website, follow these steps: "
        "1. Use the browser_navigate tool to go to the specified website URL. "
        "2. Use the browser_take_screenshot tool to save the screenshot to the given file path. "
        "Always save the screenshot on the user's Desktop. "
        "Do not use the browser_snapshot tool. "
        "Do not perform any extra steps. "
        "Do not use any tools or methods other than browser_navigate and browser_take_screenshot from Playwright MCP. "
        "If a tool returns a very large output, only keep the first 500 characters of its output in your memory."
    )
    # NOTE: Context truncation of tool outputs is not possible with the current MCPAgent version.
    agent = MCPAgent(llm=llm, client=client, max_steps=4, system_prompt=system_prompt)
    prompt = f"Go to {website_url} and save a screenshot as {output_path}"
    result = await agent.run(prompt)
    print(f"\nResult: {result}")
    # Upload the screenshot to Google Drive
    upload_to_gdrive(output_path)

if __name__ == "__main__":
    # Prompt user for website only
    website = input("Enter the website URL to screenshot (e.g., https://example.com): ").strip()
    # Automatically determine the Desktop path in a cross-platform way
    desktop = pathlib.Path.home() / "Desktop" / "screenshot.png"
    asyncio.run(main(website, str(desktop)))
