import pandas as pd
import numpy as np
from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from keras.wrappers.scikit_learn import KerasClassifier
import tensorflow as tf
import os.path as path


one_up = path.abspath(path.join(__file__ ,".."))
two_up =  path.abspath(path.join(__file__ ,"../.."))
three_up =  path.abspath(path.join(__file__ ,"../../.."))

ml_data = pd.read_csv(three_up + "/Data/Generated csv/atp_data_attributes.csv")
ml_data = ml_data[['player1_name',
                   'player1_age',#'player1_height',
                   'player1_ranking_points',
                   'player1_elo',
                   'player1_hand_1',
                   'player1_hand_2',
                   'player1_W/total_games',
                   'player1_W/total_games_per_surface',
                   'player1_won_h2h',
                   'player2_name',
                   'player2_age',#'player2_height',
                   'player2_ranking_points',
                   'player2_elo',
                   'player2_hand_1',
                   'player2_hand_2',
                   'player2_W/total_games',
                   'player2_W/total_games_per_surface',
                   'player2_won_h2h',
                   'player1_winrate',
                   'surface_1',
                   'surface_2',
                   'best_of_3',
                   'outcome']]

### Dropping Columns with low amount of  NA values

ml_data2 = ml_data.dropna(axis=0, subset=['player1_age','player2_age', 'player1_ranking_points','player2_ranking_points'])
ml_data2 = ml_data2.reset_index(drop=True)

###

def check_clm_na():
  '''Checks columns with NA values'''
  top_players = ml_data[ml_data['player1_ranking_points'] > 1000] # players with more than X amount of Ranking Points
  nan_values = top_players.isna()
  nan_columns = nan_values.any()
  columns_with_nan = top_players.columns[nan_columns].tolist()
  return columns_with_nan

columns_with_nan = check_clm_na()

def check_na(na_columns):
  ''' This function cheks columns with NA values and their counts'''
  counts_na = ml_data[na_columns].isnull().sum()
  return counts_na

check_na(columns_with_nan)

ml_data = ml_data[ml_data['player1_ranking_points'] > 1000]
ml_data['player1_winrate'] = ml_data['player1_winrate'].fillna(0.5)
ml_data['player1_W/total_games_per_surface'] = ml_data['player1_W/total_games_per_surface'].fillna(0)
ml_data['player2_W/total_games_per_surface'] = ml_data['player2_W/total_games_per_surface'].fillna(0)
ml_data['player1_W/total_games'] = ml_data['player1_W/total_games'].fillna(0)
ml_data['player2_W/total_games'] = ml_data['player2_W/total_games'].fillna(0)
ml_data = ml_data.reset_index(drop=True)
check_clm_na()
print('NA in columns: ', check_na(columns_with_nan))

def low_amount_games(nb_games):
  ''' This function takes out players games with less than it's 'x' amount of games'''
  players = ml_data.melt(None,['player1_name','player2_name'])['value'].value_counts() #selects all unique strings that are both in column player1_name and player2_name 
  players_out = players[players < nb_games].index.tolist()
  new_data = ml_data[~(ml_data['player1_name'].isin(players_out) | ml_data['player2_name'].isin(players_out))] 
  #ml_data5 = ml_data4[~ml_data4['player2_name'].isin(players_out)] 
  print("Number of Players games deleted:", len(players_out))
  return new_data
df_final = low_amount_games(5)
rows = len(df_final.index)
print('WATCH HERE ::', df_final.shape)


X = df_final.iloc[:, 0: 22].values
Y = df_final.iloc[:, 22].values
#X[:, 9]

# create dataset
dataset = df_final  
X = dataset.iloc[:, 0: 22].values
Y = dataset.iloc[:, 22].values
from sklearn.preprocessing import LabelEncoder
labelencoder_X_1 = LabelEncoder() #instantiate an object of the class LabelEncoder
X[:, 0] = labelencoder_X_1.fit_transform(X[:, 0]) #ordinal encoding for column 1
X[:, 0]
labelencoder_X_2 = LabelEncoder()
X[:, 9] = labelencoder_X_2.fit_transform(X[:, 9]) #ordinal encoding for column 2

#Standardise the data (x_standardised = (x - x_mean)/std_dev)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
print('WATCH HERE AGAIN ::', X.shape)


# configure the outer cross-validation procedure
cv_outer = KFold(n_splits=5, shuffle=True, random_state=1)

def build_classifier(optimizer):
  model = tf.keras.models.Sequential()
  model.add(tf.keras.layers.Dense(units = 48, kernel_initializer = 'uniform', activation = 'relu', input_dim = 22))
  model.add(tf.keras.layers.Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
  model.compile(optimizer = optimizer, loss = 'binary_crossentropy', metrics = ['accuracy']) # binary_crossentropy sparse_categorical_crossentropy
  return model

my_model = KerasClassifier(build_fn = build_classifier)


# enumerate splits
outer_results = list()
for train_ix, test_ix in cv_outer.split(X):
	# split data
	X_train, X_test = X[train_ix, :], X[test_ix, :]
	y_train, y_test = Y[train_ix], Y[test_ix]
	# configure the inner cross-validation procedure
	cv_inner = KFold(n_splits=10, shuffle=True, random_state=1)
	# define the model
	model = my_model
	# define search space :
	space = {'batch_size': [10], 'nb_epoch': [15], 'optimizer': ['adam']}
    #space = {'batch_size': [10,15], 'nb_epoch': [10,15], 'optimizer': ['RMSprop','adam']}
	# define search
	search = GridSearchCV(model, space, scoring='accuracy',cv=cv_inner,refit=True) #, cv=cv_inner
 
	# execute search
	result = search.fit(X_train, y_train)
	# get the best performing model fit on the whole training set
	best_model = result.best_estimator_
	# evaluate model on the hold out dataset
	yhat = best_model.predict(X_test)
	# evaluate the model
	acc = accuracy_score(y_test, yhat)
	# store the result
	outer_results.append(acc)
	# report progress
	print('>acc=%.3f, est=%.3f, cfg=%s' % (acc, result.best_score_, result.best_params_))

print('Accuracy: %.3f (%.3f)' % (mean(outer_results), std(outer_results)))


