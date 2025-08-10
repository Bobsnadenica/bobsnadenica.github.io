import openai
import os
import requests
from datetime import datetime
import logging
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
grok_api_key = os.getenv("GROK_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
grok_api_url = "https://api.x.ai/v1/chat/completions"

# GitHub repository details
GITHUB_USERNAME = "Bobsnadenica"
GITHUB_REPO = "bobsnadenica.github.io"
GITHUB_PATH = "errors/error.txt"  # Path in repo where error.txt will be stored

# Prompt for both APIs
prompt = """Make a single html page about the wildest conspiracy theories. Make it nice, show some skills, go crazy. Use lots of different techniques to showcase your website building skills. Make sure you give lots of info."""

# Initialize error message list
error_messages = []

# Fetch response from OpenAI
openai_content = None
try:
    logger.info("Attempting OpenAI API call")
    openai_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    openai_content = openai_response.choices[0].message.content
    logger.info("OpenAI API call succeeded")
except openai.RateLimitError as e:
    error_messages.append(f"OpenAI API rate limit exceeded: {e}")
    logger.error(f"OpenAI API rate limit exceeded: {e}")
except Exception as e:
    error_messages.append(f"OpenAI API call failed: {e}")
    logger.error(f"OpenAI API call failed: {e}")

# Fetch response from Grok
grok_content = None
try:
    logger.info("Attempting Grok API call")
    headers = {
        "Authorization": f"Bearer {grok_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-3",
        "messages": [{"role": "user", "content": prompt}],
    }
    grok_response = requests.post(grok_api_url, json=payload, headers=headers)
    grok_response.raise_for_status()
    grok_content = grok_response.json()["choices"][0]["message"]["content"]
    logger.info("Grok API call succeeded")
except Exception as e:
    error_messages.append(f"Grok API call failed: {e}")
    logger.error(f"Grok API call failed: {e}")

# Create HTML for ChatGPT if content is available
if openai_content:
    chatgpt_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily ChatGPT Conspiracy Theories</title>
  </head>
  <body>
    <h1>Conspiracy Theories for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {openai_content}
  </body>
</html>
"""
    with open("Chatgpt.html", "w", encoding="utf-8") as f:
        f.write(chatgpt_html)
    logger.info("Wrote Chatgpt.html")
else:
    logger.warning("Skipping Chatgpt.html generation due to OpenAI API failure")

# Create HTML for Grok if content is available
if grok_content:
    grok_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily Grok Conspiracy Theories</title>
  </head>
  <body>
    <h1>Conspiracy Theories for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {grok_content}
  </body>
</html>
"""
    with open("Grok.html", "w", encoding="utf-8") as f:
        f.write(grok_html)
    logger.info("Wrote Grok.html")
else:
    logger.warning("Skipping Grok.html generation due to Grok API failure")

# If there were any errors, create error.txt and upload to GitHub
if error_messages:
    error_content = f"Errors occurred at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC:\n" + "\n".join(error_messages)
    with open("error.txt", "w", encoding="utf-8") as f:
        f.write(error_content)
    logger.info("Wrote error.txt")
    
    # Upload error.txt to GitHub
    try:
        github_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_PATH}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check if file exists to get SHA for update
        response = requests.get(github_url, headers=headers)
        sha = None
        if response.status_code == 200:
            sha = response.json().get("sha")
        
        # Prepare file content for GitHub
        encoded_content = base64.b64encode(error_content.encode()).decode()
        payload = {
            "message": f"Update error.txt - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": encoded_content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha
            
        # Upload file
        response = requests.put(github_url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info("Successfully uploaded error.txt to GitHub")
    except Exception as e:
        logger.error(f"Failed to upload error.txt to GitHub: {e}")
