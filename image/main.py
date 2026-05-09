from dotenv import load_dotenv
load_dotenv()   
import os
from openai import OpenAI

# if want to take image from user's local machine
# import base64
# image_path = input("Enter the path of the image: ")
# with open(image_path, "rb") as image_file:
#     image_data = base64.b64encode(image_file.read()).decode("utf-8")

# ext = image_path.split(".")[-1].lower()
# mime_type = f"image/{ext}"

client = OpenAI(
    
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": """Generate a caption for this image in about 20 words or less,
         but it should be cool and catchy and in a genz style"""},
        {"role": "user", "content": [
            {"type":"text", "text":"Generate a caption for this image."},
            {"type":"image_url", "image_url": {"url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MH"}}
            # {"type":"image_url", "image_url": {"url": f"data:{mime_type};base64,{image_data}"}} if file is take from user's local machine
            ]
        }
    ]
)


print("Response: ", response.choices[0].message.content)
