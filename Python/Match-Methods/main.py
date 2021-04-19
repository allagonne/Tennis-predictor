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

## Seperate Sets/Games


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

features_player  = features_past_generation(120,360,df,indices)
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

# Final Concatenation

ml_data = pd.concat([features_player, cat_table],1)

# Re-order columns
cols = ml_data.columns.tolist()
cols = cols[0:5] + cols[-16:-15]  + cols[-15:-14] + cols[-14:-13] + cols[5:19] + cols[-13:-12]  + cols[-12:-11] + cols[-11:-10] + cols[19:30] + cols[31:40] + cols[46:56] + cols[30:31]
ml_data = ml_data[cols]

ml_data.to_csv(three_up + "/Data/Generated csv/atp_data_attributes.csv",index=False)
