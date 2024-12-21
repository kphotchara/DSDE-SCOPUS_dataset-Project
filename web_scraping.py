import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)

columns = ['title','publication_year','age_of_paper','aggregation_type','reference_count','open_access','has_funding_info','citation_count']
data = []

for idx in range(0,2):
    driver.get("https://link.springer.com")
    #scrap 2 time with 2 keywords
    keyword = ""
    if idx == 0:
        keyword = "Web Scraping"
        #Accept cookie
        cookie = driver.find_element(By.CLASS_NAME,"cc-banner__footer").click()
    else:
        keyword = "Computer"

    #Search with keyword
    search = driver.find_element(By.CLASS_NAME,"app-homepage-hero__input")
    search.send_keys(keyword+Keys.ENTER)

    #Get all links
    links = []
    for j in range(0,2):
        elements = driver.find_elements(By.CLASS_NAME,"app-card-open__link")
        for i in elements:
            link = i.get_attribute("href")
            links.append(link)
        btn =driver.find_elements(By.CLASS_NAME,"eds-c-pagination__link-container")
        btn[len(btn)-1].click()
    print(len(links))

    #scrap from all links
    for i in links:
        driver.get(i)

        #title
        try:
            title = driver.find_element(By.CLASS_NAME,"c-article-title").text
        except NoSuchElementException:
            # print("The element with ID 'Fun-section' was not found.")
            continue

        #funding
        funding = None
        try:
            funding = driver.find_element(By.ID, "Fun-section").text
            funding = funding[9:]
        except NoSuchElementException:
            # print("The element with ID 'Fun-section' was not found.")
            pass
        except WebDriverException as e:
            # print(f"An error occurred: {e}")
            pass

        #type open-access year
        publish = driver.find_elements(By.CLASS_NAME,"c-article-identifiers__item")
        if not("Open access" in publish[0].text or "Online" in publish[0].text or "Published" in publish[0].text):
            type = publish[0].text
        # access = {1: full access, 2: partial access}
        access = 2
        for i in publish:
            if "Open access" in i.text:
                access = 1
            if "Published" in i.text or "Online" in i.text:
                date = i.text
        year = date[len(date)-4:len(date)]
        age = 2024-int(year)
        
        #ref count
        ref = driver.find_elements(By.CLASS_NAME,"c-article-references__text")
        ref_count = len(ref)

        #citation count
        cited_count = 0
        cited = driver.find_elements(By.CLASS_NAME,"app-article-metrics-bar__count")
        for i in cited:
            if "Citation" in i.text:
                text = i.text
                split_text = text.split()
                cited_count = int(split_text[0])
                break
        row = [title,year,age,type,ref_count,access,funding,cited_count]
        data.append(row)


df = pd.DataFrame(data=data,columns=columns)
df.to_csv("sprinker_link.csv",encoding='utf-8')
    

