import os
import random
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USER_TOKEN = os.getenv("USER_TOKEN")
IMAGES_PATH = os.getenv("IMAGES_PATH", "images")
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
        current_image = random.choice(os.listdir(IMAGES_PATH))

    res = set_pfp(os.path.join(IMAGES_PATH, current_image))
    if res.status_code == 200 and res.json().get("ok"):
        print(f"Profile picture updated to {current_image}")
    else:
        print(f"Failed to update profile picture: {res.text}")

def main():
    while True:
        if not os.path.exists(IMAGES_PATH):
            print(f"Could not find {IMAGES_PATH}.")
            return
        
        images = os.listdir(IMAGES_PATH)
        if not images:
            print(f"No images found in {IMAGES_PATH}.")
            break

        randomize_pfp()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
