import os
import io
import time
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


absolute_path = os.path.dirname(__file__)
relative_image_path = "images/"
download_path = os.path.join(absolute_path, relative_image_path)
if not os.path.exists(download_path):
   os.makedirs(download_path)

chrome_options = Options()
# chrome_options.add_argument("--headless") # Hides the browser window
chrome_options.add_argument("--no-sandbox") # Bypass OS security model
# chrome_options.add_experimental_option("detach", True) # Keeps the browser open after the script finishes

homedir = os.path.expanduser("~")
chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def download_image(url, file_name, path=download_path):
    try:
        img_content = requests.get(url).content
        img_file = io.BytesIO(img_content)
        img = Image.open(img_file)
        file_path = os.path.join(path, file_name)
        with open(file_path, "wb") as f:
            img.save(f, "JPEG")
        print(f"Image {file_name} downloaded successfully")
    except Exception as e:
        print(f"Error downloading image {file_name}: {e}")

download_image("https://i.pcmag.com/imagery/roundups/02LMa8L6W4XQ6fHDsoqjrs8-3.fit_lim.size_1050x.jpg", "test.jpg")


time.sleep(10)
browser.quit()