from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

def image_response(file):
    # Handle FastAPI UploadFile object
    if hasattr(file, 'read'):
        file.file.seek(0)  # Reset file pointer to beginning
        image_bytes = file.file.read()
    else:
        # Handle file path string (for backward compatibility)
        with open(file, 'rb') as f:
            image_bytes = f.read()

    
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            ),
            "classify this image for me into this format and the classification should be [toxic, spam, harassment, safe] { classification, confidence, reasoning, llm_response } as a json format only and no need for arrays in json [safe],"
        ]
    )

    return response.text


def text_response(text):
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=f"{text} classify this text that i gave you for me into this format and the classification should be one of this only [toxic, spam, harassment, safe]  classification, confidence, reasoning, llm_response  as a json format only and no need for arrays in json like this [safe]  "
        )
    return response.text


#-------------------------------------------------------

# f = "C:/Users/udayb/OneDrive/Desktop/images.jpeg"
# ans = image_response(f)
# print(ans)
# '''
# ```json
# {
#   "classification": "safe",
#   "confidence": 0.99,
#   "reasoning": "The image depicts a mixed martial arts (MMA) fight in a UFC cage.  There is nothing toxic, spam, or harassing in the image. It's a typical scene from a sporting event.",
#   "llm_response": "The image is a screenshot of a UFC fight.  There is no indication of toxicity, spam, or harassment. The content is appropriate and depicts a sporting event."
# }
# ```
# '''

#-------------------------------------------------------
# text = "i am going to kill you"
# ans = text_response(text)
# print(ans)

# '''
# ```json
# {
#   "classification": "toxic",
#   "confidence": 0.95,
#   "reasoning": "The statement \"I am going to kill you\" is a direct threat of violence and expresses an intent to cause harm. This constitutes a clear violation of safety guidelines and falls under the category of toxic language.",
#   "llm_response": "The input text expresses a serious threat of violence.  Threats of violence are unacceptable and harmful.  Therefore, it is classified as toxic."
# }
# ```
# '''