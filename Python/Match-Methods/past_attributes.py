import pandas as pd
import numpy as np
import datetime


###################### FEATURES BASED ON THE past_matches OF THE PLAYERS ###############
def features_past_generation(days_all,
                              days_h2h,
                              data,
                              indices):
    matches_outcomes=[]
    matches_h2h=[]
    #This loop creates the data_frame
    for i,match_indice in enumerate(indices): #i is an index whhile it loops through indices with match_indice, indices the index of data (in this case is it date?)
        match=data.iloc[match_indice,:] #selects row based on match_indice

        #### Selection of Player1/Player2
        player1= match.winner_name if match_indice % 2 == 1 else match.loser_name #selects randomly who player1 is (based on if the index is odd)
        player2=match.winner_name if player1==match.loser_name else match.loser_name #selects player2 based on player1
        surface=match.surface #surface selection

        #### Calculation of past_matches games of player1/player2
        past_matches = data[((data.tourney_date == match.tourney_date)&(data.match_num < match.match_num)) | 
        ((data.tourney_date<match.tourney_date)&(data.tourney_date>=match.tourney_date-datetime.timedelta(days=days_all)))] #not sure if the most efficent way to do it
        match_features_all=features_player_creation(match, past_matches, player1, player2, surface) #function called for first player
        matches_outcomes.append(match_features_all) #appends to initially empty matches_outcomes analysis per each match


        #### Calculation of h2h of player1/player2
        past_matches = data[((data.tourney_date == match.tourney_date)&(data.match_num < match.match_num)) | 
        ((data.tourney_date<match.tourney_date)&(data.tourney_date>=match.tourney_date-datetime.timedelta(days=days_h2h)))] #not sure if the most efficent way to do it
        match_features_h2h=features_duo_creation(past_matches, player1, player2) #function called for first player
        matches_h2h.append(match_features_h2h) #appends to initially empty matches_outcomes analysis per each match
        

        if i%100==0:
            print(str(i)+"/"+str(len(indices))+" matches treated.")
    matches_outcomes=pd.DataFrame(matches_outcomes)
    matches_h2h=pd.DataFrame(matches_h2h)

    train=pd.concat([matches_outcomes,matches_h2h],1) #dataframe of all the matches of x vs y
    train.columns=[
                    'player1_name',
                    'player1_age',
                    'player1_height',
                    'player1_hand',
                    'player1_ranking_points',
                    'player1_elo',
                    'player1_wins',
                    'player1_losses',
                    'player1_total_games',
                    'player1_W/total_games', 
                    'player1_Wins_per_surface',
                    'player1_Losses_per_surface',
                    'player1_total_games_per_surface',
                    'player1_W/total_games_per_surface', 
                    'player2_name',
                    'player2_age',
                    'player2_height',
                    'player2_hand',
                    'player2_ranking_points',
                    'player2_elo',
                    'player2_wins',
                    'player2_losses',
                    'player2_total_games',
                    'player2_W/total_games',
                    'player2_Wins_per_surface',
                    'player2_Losses_per_surface',
                    'player2_total_games_per_surface',
                    'player2_W/total_games_per_surface',
                    'outcome',
                    'games_h2h',
                    'player1_won_h2h',
                    'player2_won_h2h',
                    'player1_winrate',
                  ]
    cols = train.columns.tolist()
    cols = cols[0:14] + cols[-3:-2]  + cols[14:28] + cols[-2:-1] + cols[29:30] + cols[32:33] + cols[28:29]
    train = train[cols]

    #train.columns=[feature_names_prefix+str(i) for i in range(len(train.columns))]
    return train

 

def features_player_creation(match, past_matches, player1, player2, surface): #Nested functions can use variablers of mother function. What is "Outcome though?"
    features_player=[] #new features per player per match


    ##### Player Information

    if (match.winner_name == player1):
      player1_age = match.winner_age
      player1_ht = match.winner_ht
      player1_hand = match.winner_hand
      player1_rk_points = match.winner_rank_points
      player1_elo_points = match.elo_winner
      player2_age = match.loser_age
      player2_ht = match.loser_ht
      player2_hand = match.loser_hand      
      player2_rk_points = match.loser_rank_points
      player2_elo_points = match.elo_loser
    else:
      player1_age = match.loser_age
      player1_ht = match.loser_ht
      player1_hand = match.loser_hand      
      player1_rk_points = match.loser_rank_points
      player1_elo_points = match.elo_loser
      player2_age = match.winner_age
      player2_ht = match.winner_ht
      player2_hand = match.winner_hand    
      player2_rk_points = match.winner_rank_points
      player2_elo_points = match.elo_winner


    ##### PLAYER 1

    features_player.append(player1) 
    features_player.append(player1_age) 
    features_player.append(player1_ht) 
    features_player.append(player1_hand)
    features_player.append(player1_rk_points)
    features_player.append(player1_elo_points)

    ##### General stats player1
    player1_wins=past_matches[past_matches.winner_name==player1]     #selects all rows of x player1 winning in the last matches
    player1_losses=past_matches[past_matches.loser_name==player1]    #elects all rows of x player lost in the last matches
    todo1=pd.concat([player1_wins,player1_losses],0) #adds list of both wins and losses with all rows. the 0 is to say every entry is a new row 
    features_player+=[len(player1_wins),len(player1_losses),len(todo1)] #adds number of win, lost, and total number of games
    player1_per_victory=100*len(player1_wins)/len(todo1) if len(todo1)>0 else np.nan # % of games won
    features_player.append(player1_per_victory)

    ##### Surface player1
    past_surface=past_matches[past_matches.surface==surface] #matches in X surface
    player1_wins_surface=past_surface[past_surface.winner_name==player1]    #matches won per surface in the past
    player1_losses_surface=past_surface[past_surface.loser_name==player1]    #matches lost per surface in the past
    player1_todo_surface=pd.concat([player1_wins_surface,player1_losses_surface],0) #list of all games in that period
    features_player+=[len(player1_wins_surface),len(player1_losses_surface),len(player1_todo_surface)] #adds number of wins, lost and total number of games in that surface
    player1_per_victory_surface=100*len(player1_wins_surface)/len(player1_todo_surface) if len(player1_todo_surface)>0 else np.nan # % won in that surface
    features_player.append(player1_per_victory_surface) #appends last bit


    ##### PLAYER 2

    features_player.append(player2) 
    features_player.append(player2_age) 
    features_player.append(player2_ht) 
    features_player.append(player2_hand)
    features_player.append(player2_rk_points)
    features_player.append(player2_elo_points)

    ##### General stats player2
    player2_wins=past_matches[past_matches.winner_name==player2]     #selects all rows of x player2 winning in the last matches
    player2_losses=past_matches[past_matches.loser_name==player2]    #elects all rows of x player lost in the last matches
    todo2=pd.concat([player2_wins,player2_losses],0) #adds list of both wins and losses with all rows. the 0 is to say every entry is a new row 
    features_player+=[len(player2_wins),len(player2_losses),len(todo2)] #adds number of win, lost, and total number of games
    player2_per_victory=100*len(player2_wins)/len(todo2) if len(todo2)>0 else np.nan # % of games won
    features_player.append(player2_per_victory)

    ##### Surface player2
    player2_wins_surface=past_surface[past_surface.winner_name==player2]    #matches won per surface in the past
    player2_losses_surface=past_surface[past_surface.loser_name==player2]    #matches lost per surface in the past
    player2_todo_surface=pd.concat([player2_wins_surface,player2_losses_surface],0) #list of all games in that period
    features_player+=[len(player2_wins_surface),len(player2_losses_surface),len(player2_todo_surface)] #adds number of wins, lost and total number of games in that surface
    player2_per_victory_surface=100*len(player2_wins_surface)/len(player2_todo_surface) if len(player2_todo_surface)>0 else np.nan # % won in that surface
    features_player.append(player2_per_victory_surface) #appends last bit

    ##### Player Information
    outcome = 1 if player1==match.winner_name else 0
    features_player.append(outcome)
    return features_player # returns to the function of main the result


def features_duo_creation(past_matches, player1, player2):
    features_duo=[]

    ##### General duo features
    # % of the previous matches between these 2 players won by each.
    duo1=past_matches[(past_matches.winner_name==player1)&(past_matches.loser_name==player2)]    #H2H of: Player 1 won and Player 2 lost
    duo2=past_matches[(past_matches.winner_name==player2)&(past_matches.loser_name==player1)]    #H2H of: Player 2 won and Player 1 lost
    duo=pd.concat([duo1,duo2],0)
    features_duo+=[len(duo),len(duo1),len(duo2)] #total games, games player1 won, games player2 won
    per_victory_player1=100*len(duo1)/len(duo) if len(duo)>0 else np.nan #winrate_player1
    features_duo.append(per_victory_player1)


    return features_duo

