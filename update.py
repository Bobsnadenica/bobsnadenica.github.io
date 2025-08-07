import openai
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

prompt = "Create a index.html file that serves as the front page for a fun, engaging, and professional website dedicated to Beans & Sausage. The design should showcase your best HTML and CSS skills, combining creativity with a clean layout. The website should:

    Professionally represent the theme of Beans & Sausage

    Be visually appealing and fun to explore

    Include sections such as a catchy hero/banner, product highlights, and a brief story or mission

    Use modern HTML5 structure and styling (you may include inline CSS or link to a stylesheet)

    Be responsive and user-friendly

Make it awesome!"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
)

content = response['choices'][0]['message']['content']

html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Daily ChatGPT Update</title>
  </head>
  <body>
    <h1>Fun Fact for {datetime.utcnow().strftime('%Y-%m-%d')}</h1>
    <p>{content}</p>
  </body>
</html>
"""

with open("Chatgpt.html", "w", encoding="utf-8") as f:
    f.write(html)
