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
prompt = """Create a full standalone HTML page named Chatgpt.html that is a joke meme site themed around "beans and sausage". Make it fun, ridiculous, and full of emojis everywhere possible.
There should be zero code comments. Use a silly font from Google Fonts, giant headings and random silly facts or fake quotes about beans and sausages.
The background should be beans and sausages, use huge emoji buttons that do pointless things, and show popups or meme quotes when clicked.
Also include:
    Random memes or fake news ticker at the bottom
    An auto-playing bean-themed sound/music
    A spinning sausage GIF or rotating emoji
    An input box that says “Tell us your bean secret 😳🫘” and just prints a funny response
    Random game of the day
    A random conspiracy theory
The more emojis the better. Make it absolutely ridiculous, but valid HTML. No external JS files – everything inline. Do not explain anything, just give the raw HTML.
"""

# Fetch response from OpenAI
openai_content = None
try:
    openai_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    openai_content = openai_response.choices[0].message.content
except openai.RateLimitError as e:
    logger.error(f"OpenAI API rate limit exceeded: {e}")
except Exception as e:
    logger.error(f"OpenAI API call failed: {e}")

# Fetch response from Grok
grok_content = None
try:
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
except Exception as e:
    logger.error(f"Grok API call failed: {e}")

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
else:
    logger.warning("Skipping Chatgpt.html generation due to OpenAI API failure")

# Create HTML for Grok if content is available
if grok_content:
    grok_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily Grok Update</title>
  </head>
  <body>
    <h1>Fun Fact for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {grok_content}
  </body>
</html>
"""
    with open("Grok.html", "w", encoding="utf-8") as f:
        f.write(grok_html)
else:
    logger.warning("Skipping Grok.html generation due to Grok API failure")
