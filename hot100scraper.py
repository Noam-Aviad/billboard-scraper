import datetime as dt
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# start date is set by default to August 4th 1958 - the first chart available
def get_data(from_date = dt.datetime(1958,8,4), to_date = dt.datetime.now(), timeout = 10):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    base_url = "https://www.billboard.com/charts/hot-100/"
    date = from_date
    while (to_date-date).total_seconds()>=0:
        date_str = dt.datetime.strftime(date, "%Y-%m-%d")
        print(f"Reading chart from the week of {date_str}")
        driver.get(base_url + date_str)
        songs = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.lrv-a-unstyle-list h3#title-of-a-story")))
        artists = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.lrv-a-unstyle-list span.c-label")))
        songs = [item.text for item in songs]
        artists = [item.text for item in artists]
        # Cleaning up the results:
        while '' in artists:
            artists.remove('')
        while '-' in artists:
            artists.remove('-')
        while 'NEW' in artists:
            artists.remove('NEW')
        for i in range(101):
            while str(i) in artists:
                artists.remove(str(i))
        temp_dict = {}
        for i in range(100):
            temp_dict[i+1] = {'Song' : songs[i], 'Artist' : artists[i]}
        with open(f"{date_str}.json", "w") as data_file:
            data_file.write(json.dumps(temp_dict, indent=4))
        date = date + dt.timedelta(7)

get_data()


