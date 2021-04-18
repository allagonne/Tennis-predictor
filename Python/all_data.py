import os
import glob
import pandas as pd
os.chdir("C:/Users/Thang/Desktop/Python-DSTI/Tennis-predictor/Data")

def Combine_csv():
    extension = 'csv'
    all_filenames = [i for i in glob.glob('atp*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    combined_csv.to_csv( "atp_matches_2011-2021.csv", index=False, encoding='utf-8-sig')

def Merge_id():
    df1 = pd.read_csv('atp_matches_2011-2021.csv',low_memory=False)
    df2=df1[['winner_name','loser_name','winner_id','loser_id']]
    df3 =pd.read_csv('Player_details.csv', low_memory=False)
    df4= df3.iloc[:,0:2].replace("-"," ", regex=True).rename(columns={'Player': 'winner_name'})
    df4=df4.replace(['Cristian Garin'],'Christian Garin')
    df4=df4.replace(['Alex de Minaur'],'Alex De Minaur')
    df4=df4.replace(['Albert Ramos-Vinolas'],'Albert Ramos')
    df4=df4.replace(['Jo Wilfried Tsonga'],'Jo-Wilfried Tsonga')
    df4=df4.replace(['Soonwoo Kwon'],'Soon Woo Kwon')
    df4=df4.replace(['Carlos Alcaraz'],'Carlos Alcaraz Garfia')
    df4=df4.replace(['Botic Van de Zandschulp'],'Botic van de Zandschulp')
    df4=df4.replace(['Victor Estrella Burgos'],'Victor Estrella')
    df4=df4.replace(['Duckhee Lee'],'Duck Hee Lee')
    df4=df4.replace(['James McGee'],'James Mcgee')
    df4=df4.replace(['Fred Gil'],'Frederico Gil')
    df4=df4.replace(['Izak Van der Merwe'],'Izak Van Der Merwe')
    df5= df3.iloc[:,0:2].replace("-", " ", regex=True).rename(columns={'Player': 'loser_name'})
    winner = pd.merge(df4, df2, on ='winner_name', how ='inner').drop_duplicates(subset=['winner_name'])
    winner = winner[['Id', 'winner_id','winner_name']]
    winner.columns = ['id','big_id','Player']
    loser = pd.merge(df5, df2, on ='loser_name', how ='inner').drop_duplicates(subset=['loser_name'])
    loser = loser[['Id', 'loser_id','loser_name']]
    loser.columns = ['id','big_id','Player']
    final=pd.concat([winner, loser]).drop_duplicates(subset=['Player'])
    final=final.sort_values(by=['id'])
    final.to_csv( "ids.csv", index=False, encoding='utf-8-sig')

def main():
    Combine_csv()
    Merge_id()

main()