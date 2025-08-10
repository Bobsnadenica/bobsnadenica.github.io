import openai
import os
import requests
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
grok_api_key = os.getenv("GROK_API_KEY")
grok_api_url = "https://api.x.ai/v1/chat/completions"

# Prompt for both APIs
prompt = """Make a single html page about the wildest conspiracy theories. Make it nice, show some skills, go crazy. Use lots of different techniques to showcase your website building skills. Make sure you give lots of info."""

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
    logger.error(f"OpenAI API rate limit exceeded: {e}")
except Exception as e:
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
    logger.error(f"Grok API call failed: {e}")
    grok_content = "<p>Failed to fetch Grok response due to error: {}</p>".format(str(e))

# Create HTML for ChatGPT if content is available
if openai_content:
    chatgpt_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily ChatGPT Update</title>
  </head>
  <body>
    <h1>Fun Fact for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {openai_content}
  </body>
</html>
"""
    with open("Chatgpt.html", "w", encoding="utf-8") as f:
        f.write(chatgpt_html)
    logger.info("Wrote Chatgpt.html")
else:
    logger.warning("Skipping Chatgpt.html generation due to OpenAI API failure")

# Always create Grok.html, even if Grok API fails
grok_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily Grok Update</title>
  </head>
  <body>
    <h1>Fun Fact for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {grok_content or '<p>No content available due to Grok API failure</p>'}
  </body>
</html>
"""
with open("Grok.html", "w", encoding="utf-8") as f:
    f.write(grok_html)
logger.info("Wrote Grok.html")
