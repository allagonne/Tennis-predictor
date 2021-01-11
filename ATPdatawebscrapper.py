## Data webscraping from ATP website : https://www.atptour.com/
from selenium import webdriver

Tennis_data_collection = open('Tennis_player_details_scrape.csv', 'w')

Tennis_data_collection.write('Player' + ',' + 'Career_length'+ ',' +  'Aces' + ',' + 'Double_faults' + ',' + 'First_serve' + ',' + '1st_Serve_Points_Won'
                             + ',' + '2nd_Serve_Points_Won' + ',' + 'Break_Points_Faced' + ',' + 'Break_Points_Saved' + ',' + 'Service_Games_Played' + ',' +
                             'Service_Games_Won' + ',' + 'Total_Service_Points_Won' + ',' + '\n')