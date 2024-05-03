import os
import requests
from PIL import Image

def process_image(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # You can perform your operations here. For now, let's just show the image.
        img.show()

def scan_images(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        # Check if the file is an image based on its extension
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Create full path to the image
            full_path = os.path.join(directory, filename)
            print(f'Processing {full_path}')
            # Process each image
            process_image(full_path)
        else:
            print(f'Skipped {filename}, not an image')

# Replace '/home/aly/Desktop/AI Hackathon/PythonSignLanguageTrainerWithGemini/symbols' with your actual directory path
directory_path = '/home/aly/Desktop/AI Hackathon/PythonSignLanguageTrainerWithGemini/symbols/'
scan_images(directory_path)


# Download the ASL diagram image
asl_diagram_img_path = "https://raw.githubusercontent.com/asadsheikh1/PythonSignLanguageTrainerWithGemini/main/train.png"
asl_diagram_response = requests.get(asl_diagram_img_path)
if asl_diagram_response.status_code != 200:
    print(code=1002, reason="Failed to download ASL diagram")
