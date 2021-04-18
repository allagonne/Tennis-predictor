from datetime import datetime,timedelta

from past_attributes import *
from elo_attributes import *
from categorical_attributes import *
#from stategy_assessment import *

import os.path as path
import glob

one_up = path.abspath(path.join(__file__ ,".."))
two_up =  path.abspath(path.join(__file__ ,"../.."))
three_up =  path.abspath(path.join(__file__ ,"../../.."))
print()
#remember to pip3 install --upgrade pip before 'pip install -r requirements.txt'


################################################################################
######################### Building of the raw dataset ##########################
################################################################################

## Dataset presentation (Jeff Sackman tennis_ATP matches)

path = three_up + '/Data/atp_matches*.csv'
filenames=list(glob.glob(path))
dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename))
## Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True)

## Cleaning of NAN values in 'loser_hand'
big_frame = big_frame.dropna(axis=0, subset=['loser_hand']) 
big_frame = big_frame.reset_index(drop=True)

## Tourney_date type configuration
big_frame['tourney_date'] = pd.to_datetime(big_frame['tourney_date'], format='%Y%m%d')
big_frame = big_frame.sort_values(['tourney_date', 'match_num'])
big_frame = big_frame.reset_index(drop=True)

################################################################################
############################ Adding Relevant Values ############################
################################################################################


## Adding ELO to each row
elo_rankings = compute_elo_rankings(big_frame)
big_frame = pd.concat([big_frame,elo_rankings],1)


## Selecting Period we are interested in

df = big_frame
beg = datetime.datetime(2020,3,1) 
end = df.tourney_date.iloc[-1]
indices = df[(df.tourney_date>beg)&(df.tourney_date<=end)].index

#os._exit(0)

## Building of attributes based on the past matches

features_player  = features_past_generation(features_player_creation,120,"playters_stats",df,indices)
features_player.to_csv(three_up + "/Data/Generated csv/features_player.csv",index=False)

################################################################################
############################ Final dataset selection ###########################
################################################################################


#selection of our period dataset

df_selected = df.iloc[indices,:].reset_index(drop=True)
df_selected.shape


# Categorical data

#Categorical_data = df_selected[["surface","draw_size","winner_hand","winner_ioc","loser_hand","loser_ioc","best_of","round"]]
''' Pree cleaning:
surface: 3 cat columns
draw_size: 6 cat columns
winner_hand: 3 cat columns
winner_ioc: 71 cat columns
loser_ioc: 82 cat columns
loser_hand: 3 cat columns
best_of: 2 cat colimns
round: 8 cat features
'''
categorical_data = df_selected[["surface","draw_size","winner_hand","loser_hand","best_of","round"]]
cat_table = categorical_features_encoding(categorical_data)
#cat_table.to_csv("/home/pupulvuh/Code/tennis/tennisproyect/Tennis-predictor/Data/Generated csv/atp_data_attributes.csv",index=False)

# DATA DUPLICATION
'''Data duplication: Duplicate each match'''
# ELO
elo_rankings = df_selected[["elo_winner","elo_loser","proba_elo"]]
elo_1 = elo_rankings
elo_2 = elo_1[["elo_loser","elo_winner","proba_elo"]]
elo_2.columns = ["elo_winner","elo_loser","proba_elo"]
elo_2.proba_elo = 1-elo_2.proba_elo
elo_2.index = range(1,2*len(elo_1),2)
elo_1.index = range(0,2*len(elo_1),2)
features_elo_ranking = pd.concat([elo_1,elo_2]).sort_index(kind='merge')
features_elo_ranking

# Rankings

#atp_rankings = df_selected[['winner_rank','winner_rank_points','loser_rank','loser_rank_points']]
atp_rankings = df_selected[['winner_rank_points','loser_rank_points']]
rank_1 = atp_rankings
rank_2 = rank_1[['loser_rank_points', 'winner_rank_points']]
rank_2.columns = ['winner_rank_points','loser_rank_points']
rank_2.index = range(1,2*len(rank_1),2)
rank_1.index = range(0,2*len(rank_1),2)
features_atp_ranking = pd.concat([rank_1,rank_2]).sort_index(kind='merge')
print(features_atp_ranking.shape)

#Categorical data

features_cat = pd.DataFrame(np.repeat(cat_table.values,2, axis=0),columns=cat_table.columns)
features_cat

# Final Concatenation

ml_data = pd.concat([features_elo_ranking,
                  features_cat,
                  features_player],1)

ml_data.to_csv(three_up + "/Data/Generated csv/atp_data_attributes.csv",index=False)
