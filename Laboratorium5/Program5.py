from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import argparse
import json

parser = argparse.ArgumentParser()  #argumenty

parser.add_argument('-json', '--nazwa_json', default = 'plik_z_danymi')

args = parser.parse_args()

output_json = args.nazwa_json  

options = Options()
#options.add_argument('--headless') # nie wyswietlaj strony
options.add_argument('--disable-notifications') # usuniecie wyskakujacych okienek

service = Service('webdriver/chromedriver.exe')
driver = webdriver.Chrome(service = service, options = options)

driver.get('https://www.youtube.com/') #strona


# wcisniecie guzika
button = driver.find_element(By.CSS_SELECTOR, '#content > div.body.style-scope.ytd-consent-bump-v2-lightbox > div.eom-buttons.style-scope.ytd-consent-bump-v2-lightbox > div:nth-child(1) > ytd-button-renderer:nth-child(1) > yt-button-shape > button')
button.click()
time.sleep(1) #chce zeby najpierw wcisnal przycisk dopiero potem przewijam w dol

filmy = []

# przewijanie w dol

for _ in range(5):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


elements = driver.find_elements( By.CSS_SELECTOR, '#dismissible') # znalezienie wszystkich lotow

for element in elements: # iteruje sie po filmach
    element.find_element
    film = element.text
    film_split = film.splitlines() #dziele info z filmami
    filmy.append(film_split)

filmy_pop = list(filter(None, filmy)) #ograniczenie zeby nie zapisywac pustych tablic

with open(str(output_json)+'.json','w', encoding="utf8") as f:     #zapis listy filmow
        json.dump(filmy_pop, f, ensure_ascii=False, indent=4)
        print("Zapisano do pliku json")


time.sleep(5) #po tym czasie zamykam strone

driver.close()
