# importing requirements
import requests
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

disease_names_list = []
url_of_disease = []

# path to download images
folder = r'C:\Users\Jagkrino Prasad\PycharmProjects\patona_assignment\disease_images'
website_url = 'https://dermnetnz.org/image-library'


def download_image(download_path, images_list, names_list):
    """
    This functions takes images sources list and their names list, then downloads images and saves them with their
    respective names.

    :param download_path: a Path refers to downloading path to images
    :images_list list: a list of image source urls
    :names_list: a list of Disease names
    :return: Downloads list of images in download_path directory & names the accordingly
    """
    for c in range(len(images_list) + 1):
        image_content = requests.get(images_list[c]).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')

        file_path = download_path + "\\" + '{}.jpg'.format(names_list[c])
        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')

    print('images saved')


# Initiate drivers & wait implicitly to get the required page loaded

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(2)
driver.get(website_url)
driver.implicitly_wait(2)

# get the disease name & href elements by XPATH
names_locations = driver.find_elements(By.XPATH, '//h6')
href_locations = driver.find_elements(By.XPATH, "//a[@href][@class='imageList__group__item']")

# append the names from the elements to a list
for name in names_locations:
    disease_names_list.append(name.text.rsplit(' ', 1)[0].replace('/', '~'))
# append the hrefs from the elements to a list
for href in href_locations:
    url_of_disease.append(href.get_attribute('href'))
# get the images source elements by xpath
image_elements = driver.find_elements(By.XPATH, '//div[@class="imageList__group__item__image"]/img')
# append the image sources to a list
image_sources_list = []
for image_elem in image_elements:
    image_sources_list.append(image_elem.get_attribute('src'))

# zip names list ,urls list and export as csv
name_url_df = pd.DataFrame(list(zip(*[disease_names_list, url_of_disease])), columns=['DiseaseNames', 'Url'])
name_url_df.to_csv('diseaseName-url_data.csv')

# terminate the driver
driver.close()
