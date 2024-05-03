"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai

genai.configure(api_key="AIzaSyCn2cEOZ625Gt6reE-mfqUDFceWskk0qe8")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": upload_if_needed("symbols/train.png")
  },
  {
    "role": "user",
    "parts": ["The image above shows the American Sign Language Diagram.Based on the diagram, classify the letter the hand gesture is referring to. Answer with just the class. Example: A"]
  },
  {
    "role": "model",
    "parts": ["Y"]
  },
  {
    "role": "user",
    "parts": ["what is the class of this gesture according to the above image"]
  },
  {
    "role": "user",
    "parts": upload_if_needed("symbols/fist.jpg")
  },
  {
    "role": "model",
    "parts": ["A"]
  },
  {
    "role": "user",
    "parts": ["what is the class of this gesture according to the above image"]
  },
  {
    "role": "user",
    "parts": upload_if_needed("symbols/1.jpeg")
  },
  {
    "role": "model",
    "parts": ["S"]
  },
  {
    "role": "user",
    "parts": upload_if_needed("symbols/check.jpg")
  },
  {
    "role": "user",
    "parts": ["what is the class of this gesture according to the above image"]
  },
  {
    "role": "model",
    "parts": ["G"]
  },
])

convo.send_message("")
print(convo.last.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)