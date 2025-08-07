import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """Create a full standalone HTML page named Chatgpt.html that is a joke meme site themed around "beans and sausage". Make it fun, ridiculous, and full of emojis everywhere possible 😂🌭🫘🔥.
There should be zero code comments. Use a silly font from Google Fonts (like 'Comic Neue' or 'Chewy'), giant headings like “BEANS & SAUSAGE 4EVER!!!” and random silly facts or fake quotes about beans and sausages (e.g. “Einstein once said beans > relativity 🧠➡️🫘”).
The background should be colorful or use a gradient, use huge emoji buttons that do pointless things (like "Launch the Sausage Cannon 🌭💥"), and show popups or meme quotes when clicked.
Also include:
    Random memes or fake news ticker at the bottom (like “BREAKING: Sausage elected President 🌭🇺🇸”)
    An auto-playing bean-themed sound/music (host from an online source or simulate)
    A spinning sausage GIF or rotating emoji
    An input box that says “Tell us your bean secret 😳🫘” and just prints a funny response
The more emojis the better. Make it absolutely ridiculous, but valid HTML. No external JS files – everything inline. Do not explain anything, just give the raw HTML.
"""

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
)

content = response.choices[0].message.content

html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily ChatGPT Update</title>
  </head>
  <body>
    <h1>Fun Fact for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    {content}
  </body>
</html>
"""

with open("Chatgpt.html", "w", encoding="utf-8") as f:
    f.write(html)
