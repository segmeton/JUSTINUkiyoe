from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import platform, json, os
import pandas as pd

def initBrowser(headless=False):
    if "Windows" in platform.system():
        chrome_path = "driver/chromedriver.exe"
    else:
        chrome_path = "driver/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--disable-features=NetworkService")
    if headless:
        chrome_options.add_argument('headless')
    return webdriver.Chrome(options=chrome_options,executable_path=chrome_path)

def get_page_links(driver):
    page_links = []

    for page_index in range(23):
        page_links.append("https://research.britishmuseum.org/research/collection_online/search.aspx?searchText=Ukiyo&page=" + str(page_index+1))

    return page_links

def get_image_urls(driver, page_links):
    image_urls = []
    if os.path.exists("Data/image-urls.txt"):
        with open("Data/image-urls.txt", 'r') as f:
            for url in f.readlines():
                image_urls.append(url)
    else:
        with open("Data/image-urls.txt", 'a') as f:
            for page in page_links:
                driver.get(page)

                wait = WebDriverWait(driver, 10)
                wait.until(lambda driver: driver.execute_script('return document.readyState == "complete"'))

                image_links = driver.find_elements_by_xpath('//a[@class="image"]')

                for img_link in image_links:
                    link = img_link.get_attribute('href')
                    image_urls.append(link)
                    f.write(link + "\n")
    
    return image_urls

def get_img_info(driver, url):
    print("url " + url)
    img_info = {}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.execute_script('return document.readyState == "complete"'))

        title = driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div[1]/h2').text
        print('title ' + title)
        image = driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div[4]/a/img')
        img_link = image.get_attribute('src')
        print("image link " + img_link)
        img_description = image.get_attribute('alt')
        print('image description ' + img_description)

        keywords = []
        try:
            subjects_text = driver.find_element_by_xpath("//*[contains(text(), 'Subjects')]")
            print("subject text " + subjects_text.text)
            subjects = subjects_text.find_elements_by_xpath("../ul/li")
            
            for subject in subjects:
                try:
                    keyword = subject.find_element_by_xpath('.//a[1]').text
                    print("keyword " + keyword)
                    keywords.append(keyword)
                except Exception as e:
                    print('url ' + url + ' error ' + str(e))
        except Exception as e:
            print("error " + str(e))
        
    except:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.execute_script('return document.readyState == "complete"'))

        title = driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div[1]/h2').text
        print('retry title ' + title)
        image = driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div[4]/a/img')
        img_link = image.get_attribute('src')
        print("retry image link " + img_link)
        img_description = image.get_attribute('alt')
        print('retry image description ' + img_description)

        keywords = []
        try:
            subjects_text = driver.find_element_by_xpath("//*[contains(text(), 'Subjects')]")
            print("subject text " + subjects_text.text)
            subjects = subjects_text.find_elements_by_xpath("../ul/li")
            
            for subject in subjects:
                try:
                    keyword = subject.find_element_by_xpath('.//a[1]').text
                    print("retry keyword " + keyword)
                    keywords.append(keyword)
                except Exception as e:
                    print('retry url ' + url + ' error ' + str(e))
        except Exception as e:
            print("retry error " + str(e))
        
    img_info['title'] = title
    img_info['src'] = img_link
    img_info['description'] = img_description
    img_info['keywords'] = keywords

    return img_info



driver = initBrowser()

page_links = get_page_links(driver)

urls = get_image_urls(driver, page_links)
print(len(urls))

ukiyo_images = {}
titles = []
srcs = []
descriptions = []
keywords = []
for url in urls:
    img_info = get_img_info(driver, url)
    print(json.dumps(img_info))
    titles.append(img_info.get('title'))
    srcs.append(img_info.get('src'))
    descriptions.append(img_info.get('description'))
    keywords.append(';'.join(img_info.get('keywords')))

ukiyo_images['Title'] = titles
ukiyo_images['Source'] = srcs
ukiyo_images['Description'] = descriptions
ukiyo_images['Keywords'] = keywords

imagedf = pd.DataFrame(ukiyo_images, columns= ['Title', 'Source', 'Description', 'Keywords'])

print(ukiyo_images)
imagedf.to_csv('Data/ukiyo-e-content-original.csv', index=None, header=True)




# ukiyo_images = {}
# titles = []
# srcs = []
# descriptions = []
# keywords = []
# img_info = get_img_info(driver, "https://research.britishmuseum.org/research/collection_online/collection_object_details.aspx?objectId=784083&partId=1&searchText=ukiyo&page=1")
# print(json.dumps(img_info))
# titles.append(img_info.get('title'))
# srcs.append(img_info.get('src'))
# descriptions.append(img_info.get('description'))
# keywords.append(';'.join(img_info.get('keywords')))

# ukiyo_images['Title'] = titles
# ukiyo_images['Source'] = srcs
# ukiyo_images['Description'] = descriptions
# ukiyo_images['Keywords'] = keywords

# imagedf = pd.DataFrame(ukiyo_images, columns= ['Title', 'Source', 'Description', 'Keywords'])

# print(ukiyo_images)
# imagedf.to_csv('Data/ukiyo-e-test.csv', index=None, header=True)






