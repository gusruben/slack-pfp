import os
import random
import time
import requests
from PIL import Image, ImageOps  # Add ImageOps to your imports
from dotenv import load_dotenv

load_dotenv()
USER_TOKEN = os.getenv("USER_TOKEN")
IMAGES_PATH = os.getenv("IMAGES_PATH", "images")
CROPPED_IMAGES_PATH = os.getenv("CROPPED_IMAGES_PATH", "images/cropped")
INTERVAL = int(os.getenv("INTERVAL", 30 * 60))

current_image = ""

def set_pfp(image_path):
    url = "https://slack.com/api/users.setPhoto"
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}"
    }
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, headers=headers, files=files)
    
    return response

def randomize_pfp():
    global current_image
    last_image = current_image
    while current_image == last_image:
        current_image = random.choice(os.listdir(CROPPED_IMAGES_PATH))

    res = set_pfp(os.path.join(CROPPED_IMAGES_PATH, current_image))
    if res.status_code == 200 and res.json().get("ok"):
        print(f"Profile picture updated to {current_image}")
    else:
        print(f"Failed to update profile picture: {res.text}")

def main():
    print("Cropping and scaling images...")
    if not os.path.exists(CROPPED_IMAGES_PATH):
        os.makedirs(CROPPED_IMAGES_PATH)
    for filename in os.listdir(IMAGES_PATH):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # scale and crop image to 512x512
            image_path = os.path.join(IMAGES_PATH, filename)
            image = Image.open(image_path)
            new_size = (512, 512)
            
            # Use ImageOps.fit for scaling and cropping
            new_image = ImageOps.fit(image, new_size, Image.Resampling.LANCZOS)
            new_image.save(os.path.join(CROPPED_IMAGES_PATH, filename))
            
            print(f"Processed {filename}")

    print("Starting!")
    while True:
        if not os.path.exists(CROPPED_IMAGES_PATH):
            print(f"Could not find {CROPPED_IMAGES_PATH}.")
            return
        
        images = os.listdir(CROPPED_IMAGES_PATH)
        if not images:
            print(f"No images found in {CROPPED_IMAGES_PATH}.")
            break

        randomize_pfp()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")