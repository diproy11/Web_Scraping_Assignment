# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import requests

website = "https://dermnetnz.org/image-library"
option= webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option, service=Service(ChromeDriverManager().install()))
driver.get(website)
time.sleep(3)

#Finding Names/ Links/ Images
name_list = driver.find_elements(by=By.XPATH,value='//div[@class="imageList__group__item__copy"]')
link_list = driver.find_elements(by=By.XPATH,value='//a[@class="imageList__group__item"]')
image_list = driver.find_elements(by=By.XPATH, value='//div[@class="imageList__group__item__image"]/img')


#Creating List
name = []
links = []
images = []

for n in name_list:
    name.append(n.text[:-7])
for l in link_list:
    links.append(l.get_attribute("href"))
for img in image_list:
    images.append(img.get_attribute("src"))

#Creating Folder and Downloading files

folder = r'C:/Users/VS/PycharmProjects/WebScrapping/images'
os.makedirs(folder, exist_ok=True)

for i in image_list:
    url = i.get_attribute('src')
    filename = url.split("/")[-1]

    path_img = os.path.join(folder, filename)
    response = requests.get(url)

    with open(path_img, 'wb') as im:
        im.write(response.content)

driver.quit()

#Creating DataSet

df = pd.DataFrame({"Name": name, "Link": links, "Images": images})
df.to_csv("disease.csv", index=False)


