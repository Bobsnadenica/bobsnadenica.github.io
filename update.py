import openai
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

prompt = """Create an index.html file that serves as the front page for a fun, engaging, and professional website dedicated to Beans & Sausage. The design should showcase your best HTML and CSS skills, combining creativity with a clean layout. The website should:
- Include a header with a logo
- Use warm colors and friendly fonts
- Display featured products with images
- Have a responsive design for mobile devices
"""

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
