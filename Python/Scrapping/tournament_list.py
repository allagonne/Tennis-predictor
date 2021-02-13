from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

tournaments_data = open('tournaments.csv', 'w')
tournaments_data.write('Tournament' + ',' +  'Court' + ',' + 'Type'+'\n')
for i in tqdm(range(2, 13)):
    for j in tqdm(range(1, 11)):
        try:
            PATH = "C:\Program Files (x86)\chromedriver.exe"
            options = Options()
            # options.add_argument("--headless")
            # options.add_argument('--disable-gpu')
            options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(PATH,options=options)
            driver.get('https://www.atptour.com/en/tournaments')
            tournaments_name = driver.find_element_by_xpath('//*[@id="contentAccordionWrapper"]/div['+str(i)+']/div[2]/div/table/tbody/tr['+str(j)+']/td[2]/a').text
            tournaments_data.write(tournaments_name + ',')
            tournaments_court = driver.find_element_by_xpath('//*[@id="contentAccordionWrapper"]/div['+str(i)+']/div[2]/div/table/tbody/tr['+str(j)+']/td[3]/table/tbody/tr/td[2]').text
            tournaments_data.write(tournaments_court + ',')
            if i==8 and j ==7:
                tournaments_data.write('\n')
            else:
                src_point = driver.find_element_by_xpath('//*[@id="contentAccordionWrapper"]/div['+str(i)+']/div[2]/div/table/tbody/tr['+str(j)+']/td[1]/img').get_attribute("src")
                tournaments_point = src_point[len(src_point)-7:len(src_point)-4]
                if  tournaments_point == '000':
                    tournaments_point = '1000'
                elif  tournaments_point == 'lam':
                    tournaments_point = '2000'
                elif tournaments_point == 'als':
                    tournaments_point = '1500'
                elif tournaments_point.isdigit()==False:
                    tournaments_point="Not relevant"
                tournaments_data.write(tournaments_point + '\n')
                driver.close()
        except NoSuchElementException:
            break