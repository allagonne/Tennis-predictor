import pandas as pd
import numpy as np
import datetime

# This is here for testing, should be errased later:
# path = '/home/pupulvuh/Code/tennis/tennisproyect/Tennis-predictor/Data/test.csv'
# df = pd.read_csv(path)

# df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d')
# df = df.sort_values(['tourney_date', 'match_num'])
# df = df.reset_index(drop=True)
# beg = datetime.datetime(2020,3,1) 
# end = df.tourney_date.iloc[-1]
# indices = df[(df.tourney_date>beg)&(df.tourney_date<=end)].index


def features_past_generation(features_creation_function,
                             days,
                             feature_names_prefix,
                             data,
                             indices):




    matches_outcomes=[]
    #This loop creates the data_frame
    for i,match_indice in enumerate(indices): #i is an index whhile it loops through indices with match_indice, indices the index of data (in this case is it date?)
        match=data.iloc[match_indice,:] #selects row based on match_indice

        past_matches = data[((data.tourney_date == match.tourney_date)&(data.match_num < match.match_num)) | 
        ((data.tourney_date<match.tourney_date)&(data.tourney_date>=match.tourney_date-datetime.timedelta(days=days)))] #not sure if the most efficent way to do it

        match_features_outcome_1=features_creation_function(1,match,past_matches) #function called for first player
        match_features_outcome_2=features_creation_function(2,match,past_matches) # same for second player, data is dubled
        matches_outcomes.append(match_features_outcome_1) #appends to initially empty matches_outcomes analysis per each match
        matches_outcomes.append(match_features_outcome_2) #same for second player
        if i%100==0:
            print(str(i)+"/"+str(len(indices))+" matches treated.")
    train=pd.DataFrame(matches_outcomes) #dataframe of all the matches of x vs y
    train.columns=['Wins','Losses','total_games','W/total_games', 'Wins_per_surface','Losses_per_surface','total_games_per_surface','W/total_games_per_surface', 
    'player_name', 'winner', 'loser', 'tourney name' ]
    #train.columns=[feature_names_prefix+str(i) for i in range(len(train.columns))]
    return train

 

def features_player_creation(outcome,match,past_matches): #Nested functions can use variablers of mother function. What is "Outcome though?"
    features_player=[] #new features per player per match
    ##### Match information extraction (according to the outcome)
    player=match.winner_name if outcome==1 else match.loser_name #declare current player winner_name or loser_name
    surface=match.surface #surface selection
    ##### General stats
    wins=past_matches[past_matches.winner_name==player]     #selects all rows of x player winning in the last matches
    losses=past_matches[past_matches.loser_name==player]    #elects all rows of x player lost in the last matches
    todo=pd.concat([wins,losses],0) #adds list of both wins and losses with all rows. the 0 is to say every entry is a new row 
    features_player+=[len(wins),len(losses),len(todo)] #adds number of win, lost, and total number of games
    per_victory=100*len(wins)/len(todo) if len(todo)>0 else np.nan # % of games won
    features_player.append(per_victory)
    ##### Surface
    past_surface=past_matches[past_matches.surface==surface] #matches in X surface
    wins_surface=past_surface[past_surface.winner_name==player]    #matches won per surface in the past
    losses_surface=past_surface[past_surface.loser_name==player]    #matches lost per surface in the past
    todo_surface=pd.concat([wins_surface,losses_surface],0) #list of all games in that period
    features_player+=[len(wins_surface),len(losses_surface),len(todo_surface)] #adds number of wins, lost and total number of games in that surface
    per_victory_surface=100*len(wins_surface)/len(todo_surface) if len(todo_surface)>0 else np.nan # % won in that surface
    features_player.append(per_victory_surface) #appends last bit
    features_player.append(player) #append player name
    features_player.append(match.winner_name)
    features_player.append(match.loser_name)
    features_player.append(match.tourney_name)
    # index_list = past_matches.index.tolist()
    # features_player.append(index_list)
    return features_player # returns to the function of main the result


# This is here for testing, should be errased later:


# features_player  = features_past_generation(features_player_creation,50,"playters_stats",df,indices)
# features_player.to_csv("/home/pupulvuh/Code/tennis/tennisproyect/Tennis-predictor/Data/Generated csv/features_player.csv",index=False)

# df.to_csv("/home/pupulvuh/Code/tennis/tennisproyect/Tennis-predictor/Data/Generated csv/testings.csv",index=False)

