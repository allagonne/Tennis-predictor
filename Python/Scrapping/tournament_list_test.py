from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import re

## options of the driver
options = Options()
##options.add_argument("--headless")
##options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")

WD_PATH = "/home/pupulvuh/Downloads/chromedriver"
current_atp_rankings_webpage = 'https://www.atptour.com/en/scores/results-archive'

list_tournaments = []
list_places = []
list_dates = []

## generating webpages
tournament_date_list = [str(year) for year in range(2021, 2020, -1)]
mywebpage_archive_list = ['https://www.atptour.com/en/scores/results-archive?year={}'.format(tournament_date_list[i]) for i in range(2021-2020)]

## webscraping archives
#tournament_date_list = [str(year) for year in range(2020, 2010, -1)]
for k in tqdm(range(len(tournament_date_list))): ## decrementing through years
    print("\n" + "Starting webscraping of TOP 100 tournaments of year : " + tournament_date_list[k] + "\n")
    driver = webdriver.Chrome(WD_PATH, options=options)
    driver.get(mywebpage_archive_list[k])
    tournaments = driver.find_elements_by_xpath('//td[@class="title-content"]')
    t_surface = driver.find_elements_by_xpath('//tr[@class="tourney-result"]/td[5]')
    #t_point = driver.find_element_by_xpath('//tr[@class="tourney-result"]/td[2]/img').get_attribute("src")
   
    #print(t_surface.text)
    for p in range(len(tournaments)):
        t_point = ''
        tourneys = []
        tourneys = re.split('; |, |\*|\n',tournaments[p].text)
        #print(t_surface[p])
        tourneys.append(t_surface[p].text)
        try:
            t_point = driver.find_element_by_xpath('//tbody/tr['+str(p+1)+']/td[2]/img').get_attribute("src")
        except NoSuchElementException:  #spelling error making this code not work as expected
            pass    
        if t_point != '':
        #points = t_point[p].get_attribute("src")
            tournaments_point = t_point[len(t_point)-7:len(t_point)-4]
            if  tournaments_point == '000':
                tournaments_point = '1000'
            elif  tournaments_point == 'lam':
                tournaments_point = '2000'
            elif tournaments_point == 'als':
                tournaments_point = '1500'
            elif tournaments_point.isdigit()==False:
                tournaments_point="Not relevant" 
            tourneys.append(tournaments_point)
        else:
            tourneys.append("Not relevant")
        list_tournaments.append(tourneys)


    driver.close()


## write into Tennis_data_collection file
#
Tennis_data_collection = open("../Tennis-predictor/Data/tourneys_tests.csv", 'w')
Tennis_data_collection.write('Id' + ',' + 'Tournaments' + ','  + 'City' + ',' + 'Country' + ',' + 'Date' + ',' + 'Court' + ',' + 'ATP'+'\n')
[Tennis_data_collection.write(str(id+1) + ',' + list_tournaments[id][0] + ',' + list_tournaments[id][1] + ',' + list_tournaments[id][2] 
+ ',' + list_tournaments[id][3] + ',' + list_tournaments[id][4] + ',' + list_tournaments[id][5] + ',' + '\n') for id in range(len(list_tournaments))]
Tennis_data_collection.close()

