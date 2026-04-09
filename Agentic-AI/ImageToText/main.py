from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role" : "user", "content" : [
            {"type" : "text", "text" : "what do you see in the image?"},
            {"type" : "image_url", "image_url" : {
                "url" : "https://images.pexels.com/photos/36834297/pexels-photo-36834297.jpeg"
            }}
        ]}
    ]
)

print(response.choices[0].message.content)