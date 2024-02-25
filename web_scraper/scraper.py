import os
import io
import re
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
        os.remove(file_path)
        raise e

def scrape_images(character, show, max_images=10):
    def scroll_down():
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    new_path = download_path + "/" + character + "_" + show
    if not os.path.exists(new_path):
        os.makedirs(download_path + "/" + character + "_" + show)

    search_term = character + "'s face from " + show + " anime"
    search_url = f"https://www.google.com/search?q={search_term}&tbm=isch"
    browser.get(search_url)
    image_urls = set()

    while len(image_urls) < max_images:
        print(f"Found {len(image_urls)} images, looking for more...")
        scroll_down()
        thumbnail_results = browser.find_elements(By.CLASS_NAME, "Q4LuWd")
        print(f"Found {len(thumbnail_results)} thumbnail images")

        for img in thumbnail_results:
            if(len(image_urls) >= max_images):
                print(f"Found {len(image_urls)} images, done")
                break
            try:
                img.click()
                time.sleep(0.3)
            except Exception:
                continue

            actual_images = browser.find_elements(By.CLASS_NAME, "iPVvYb")
            print(f"Found {len(actual_images)} actual images")
            for actual_image in actual_images:
                if actual_image.get_attribute('src') in image_urls:
                    break
                if actual_image.get_attribute("src") and "http" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute("src"))
                    try:
                        download_image(actual_image.get_attribute("src"), f"{character}_{len(image_urls)}.jpg", new_path)
                    except Exception as e:
                        image_urls.remove(actual_image.get_attribute("src"))

        
    return image_urls

print(absolute_path)
with open(absolute_path + '/character_list.txt', 'r') as file:
    for line in file:
        print(line)
        match = re.match(r'(.+?): (.+)', line)
        if match:
            character = match.group(1)
            show = match.group(2)
            image_urls = scrape_images(character, show, 200)
            print(f"Scraped {len(image_urls)} images for {character}'s face from {show} anime")

time.sleep(10)
browser.quit()