from fastapi import FastAPI, WebSocket
import uvicorn
import google.generativeai as genai
import requests

app = FastAPI()

# Configure the API key globally, not in the endpoint
genai.configure(api_key="AIzaSyCn2cEOZ625Gt6reE-mfqUDFceWskk0qe8")

@app.websocket('/detect')
async def detect(websocket: WebSocket):
    await websocket.accept()
    frame = await websocket.receive_bytes()  # Receive the image bytes directly

    image_path = 'received_image.jpg'

    # Write the bytes to a file
    with open(image_path, 'wb') as image_file:
        image_file.write(frame)

    # Download the ASL diagram image
    asl_diagram_img_path = "https://raw.githubusercontent.com/asadsheikh1/PythonSignLanguageTrainerWithGemini/main/train.png"
    asl_diagram_response = requests.get(asl_diagram_img_path)
    if asl_diagram_response.status_code != 200:
        await websocket.close(code=1002, reason="Failed to download ASL diagram")
        return

    # Prepare prompt parts
    image_parts = [{"mime_type": "image/jpeg", "data": frame}]
    text_parts = [
        "\nThe image above shows the American Sign Language Diagram.\n",
        "\nBased on the diagram, classify the letter the hand gesture is referring to. "
        "Answer with just the class. Example: A\nanswer: "
    ]
    prompt_parts = [
        image_parts[0],
        {"text": text_parts[0] + text_parts[1]}
    ]

    # Generation and safety settings
    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 256
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]
    
    # Create model instance
    model_pro_1_0_vision = genai.GenerativeModel(
        model_name="gemini-1.0-pro-vision-latest",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    # Generate the response
    response = model_pro_1_0_vision.generate_content(prompt_parts)
    print(response)
    await websocket.send_text(response.text.strip().lower())

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
