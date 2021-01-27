<<<<<<< HEAD
## Data webscraping of ATP players from ATP website : https://www.atptour.com/

## libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm ## to get a progression line whilst running the code

options = Options()
# options.add_argument("--headless")
# options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")

WD_PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(WD_PATH, options=options)
mywebpage = 'https://www.atptour.com/en/rankings/singles'

Tennis_data_collection = open('Tennis_player_details.csv', 'w')
Tennis_data_collection.write('Id' + ',' + 'Player' + '\n')

##
for i in tqdm(range(1, 101)):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(WD_PATH, options=options)
    driver.get(mywebpage)
    player_name = driver.find_element_by_xpath('//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a').text
    Tennis_data_collection.write(str(i) + ',' + player_name + ',' + '\n')
    driver.close()

Tennis_data_collection.close()


=======
## Data webscraping of ATP players from ATP website : https://www.atptour.com/

## libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm ## to get a progression line whilst running the code

options = Options()
# options.add_argument("--headless")
# options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")

WD_PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(WD_PATH, options=options)
mywebpage = 'https://www.atptour.com/en/rankings/singles'

Tennis_data_collection = open('Tennis_player_details.csv', 'w')
Tennis_data_collection.write('Id' + ',' + 'Player' + '\n')

##
for i in tqdm(range(1, 101)):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(WD_PATH, options=options)
    driver.get(mywebpage)
    player_name = driver.find_element_by_xpath('//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a').text
    Tennis_data_collection.write(str(i) + ',' + player_name + ',' + '\n')
    driver.close()

Tennis_data_collection.close()


>>>>>>> 0e2658327ce3e690e51ade530aad4996e8b1b854
