## Data webscraping of ATP players from ATP website : https://www.atptour.com/

## libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm ## to get a progression line whilst running the code

## options on the driver
options = Options()
##options.add_argument("--headless")
##options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")

WD_PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(WD_PATH, options=options)
mywebpage = 'https://www.atptour.com/en/rankings/singles'

Tennis_data_collection = open('Tennis_player_details.csv', 'w')
Tennis_data_collection.write('Id' + ',' + 'Player' + '\n')

list_players = []

## actual TOP 100 ## just 10 for test
print("Starting webscraping of TOP 100 current players\n")
## webscraping the ATP ranking page without a loop
driver = webdriver.Chrome(WD_PATH, options=options)
driver.get(mywebpage)
players = driver.find_elements_by_xpath('//td[@class="player-cell"]')
for p in range(len(players)):
    list_players.append(players[p].text)
driver.close()

## generating webpages
dates_archive = ['2020-01-06', '2019-01-07', '2018-01-01', '2017-01-02', '2016-01-04', '2015-01-05', '2014-01-06', '2013-01-07', '2012-01-02', '2011-01-03']
mywebpage_archive_list = ['https://www.atptour.com/en/rankings/singles?rankDate={}&rankRange=0-100'.format(dates_archive[i]) for i in range(10)]

## webscraping archives without a loop
strarchdate_list = [str(year) for year in range(2020, 2010, -1)]
for k in range(len(strarchdate_list)): ## decrementing through years
    print("\n" + "Starting webscraping of TOP 100 players of year : " + strarchdate_list[k] + "\n")
    driver = webdriver.Chrome(WD_PATH, options=options)
    driver.get(mywebpage_archive_list[k])
    players = driver.find_elements_by_xpath('//td[@class="player-cell"]')
    for p in range(len(players)):
        if players[p].text not in list_players:
            list_players.append(players[p].text)
    driver.close()

## write into Tennis_data_collection file
[Tennis_data_collection.write(str(id+1) + ',' + list_players[id] + ',' + '\n') for id in range(len(list_players))]
"""
for i in tqdm(range(1, 101)):
    id = i
    driver = webdriver.Chrome(WD_PATH, options=options)
    driver.get(mywebpage)
    player_name = driver.find_element_by_xpath('//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a').text
    Tennis_data_collection.write(str(id) + ',' + player_name + ',' + '\n')
    list_players.append(player_name)
    driver.close()

## generating webpages

dates_archive = ['2020-01-06', '2019-01-07', '2018-01-01', '2017-01-02', '2016-01-04', '2015-01-05', '2014-01-06', '2013-01-07', '2012-01-02', '2011-01-03']
mywebpage_archive_list = ['https://www.atptour.com/en/rankings/singles?rankDate={}&rankRange=0-100'.format(dates_archive[i]) for i in range(10)]

## webscraping players in archived rankings
strarchdate_list = [str(year) for year in range(2020, 2010, -1)]
for k in range(len(strarchdate_list)): ## decrementing through years
    print("\n" + "Starting webscraping of TOP 100 players of year : " + strarchdate_list[k] + "\n")
    for i in tqdm(range(1, 101)):
        driver = webdriver.Chrome(WD_PATH, options=options)
        driver.get(mywebpage_archive_list[k])
        player_name = driver.find_element_by_xpath('//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a').text
        if player_name not in list_players:
            id += 1
            Tennis_data_collection.write(str(id) + ',' + player_name + ',' + '\n')
            list_players.append(player_name)
        driver.close()
"""
Tennis_data_collection.close()

