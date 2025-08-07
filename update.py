import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """Create a whimsical and animated homepage for a Beans & Sausage World. The design should transport visitors into a cartoon-like universe where beans and sausages are the main characters. This should feel like a fun, meme-driven website, as if beans and sausages are living their own animated lives. 
The page should be colorful, interactive, and engaging with playful animations and effects.
Key Features:
    Header: A playful logo that features animated beans and sausages bouncing or dancing around.
    Fun Animation: Beans and sausages interacting in an animated environment. For example, sausages might be rolling down a hill, beans bouncing up and down, or having a party. Maybe they interact with each other in funny ways (slapstick humor!).
    Meme-Inspired Design: Bright colors (warm tones like reds, oranges, yellows), quirky typography (think Comic Sans, Poppins, or something friendly and playful), and silly effects like beans jumping out of the screen.
    Featured Sections:
        Bean World: An area where beans can be seen in different "roles" (bean superheroes, bean musicians, etc.).
        Sausage Adventures: A section where sausages embark on hilarious adventures—sailing on a hot dog boat, having a BBQ party, etc.
        Interactive Animation: Hover effects where beans and sausages react to your cursor (like they follow the mouse or move when clicked).
    Mobile Responsiveness: The page should still feel engaging and fun on mobile. Beans and sausages should shrink or adjust to fit the screen without losing their charm.
    Footer: A "Contact" section with a funny twist like "Want to talk to the beans? Just send a message to the Sausage HQ."
Let the design be playful, and the layout should be clean yet eccentric. The whole page should feel like it's a meme playground for beans and sausages, with surprising little animations and humor popping up everywhere.
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
