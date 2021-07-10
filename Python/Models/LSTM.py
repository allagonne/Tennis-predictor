import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from matplotlib import pyplot as plt
from keras.wrappers.scikit_learn import KerasClassifier
from keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


ml_data = pd.read_csv('atp_data_attributes.csv')
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
#df_final.shape

# create training and testing vars

dataset = df_final  
X2 = dataset.iloc[:, 0: 22].values
Y2 = dataset.iloc[:, 22].values
Y2 = np.vstack((Y2, abs(Y2-1))).transpose()


# Encoding
from sklearn.preprocessing import LabelEncoder
labelencoder_X_1 = LabelEncoder() #instantiate an object of the class LabelEncoder
X2[:, 0] = labelencoder_X_1.fit_transform(X2[:, 0]) #ordinal encoding for column 1
X2[:, 0]
labelencoder_X_2 = LabelEncoder()
X2[:, 9] = labelencoder_X_2.fit_transform(X2[:, 9]) #ordinal encoding for column 2
#X = np.array(ct.fit_transform(X), dtype=np.float)

#Standardise the data (x_standardised = (x - x_mean)/std_dev)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
'''X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test) #note that we use the scale set from the training set to transform the test set'''
X2 = sc.fit_transform(X2)


x_train, x_test, y_train, y_test = train_test_split(X2, Y2, test_size=0.2)

x_train=np.reshape(x_train,(8873,22,1))
x_test=np.reshape(x_test,(2219,22,1))

batch_size = 18
# Each MNIST image batch is a tensor of shape (batch_size, 22, 1).
# Each input sequence will be of size (22, 1).
input_dim = 22

units = 18
output_size = 2  # binary 1 - 0

# Build the RNN model
def build_model(allow_cudnn_kernel=True):
    # CuDNN is only available at the layer level, and not at the cell level.
    # This means `LSTM(units)` will use the CuDNN kernel,
    # while RNN(LSTMCell(units)) will run on non-CuDNN kernel.
    if allow_cudnn_kernel:
        # The LSTM layer with default options uses CuDNN.
        lstm_layer = keras.layers.LSTM(units, input_shape=(input_dim,1))
    else:
        # Wrapping a LSTMCell in a RNN layer will not use CuDNN.
        lstm_layer = keras.layers.RNN(
            keras.layers.LSTMCell(units), input_shape=(input_dim,1)
        )
    model = keras.models.Sequential(
        [
            lstm_layer,
            keras.layers.BatchNormalization(),
            keras.layers.Dense(output_size),
        ]
    )
    return model

model = build_model(allow_cudnn_kernel=True)

model.compile(
    loss=keras.losses.CategoricalCrossentropy(from_logits=True),
    optimizer="Adam",
    metrics=["accuracy"]
)

model.summary()

# Create callbacks
callbacks = [EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)]

history = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=batch_size, epochs=10, callbacks=callbacks)
loss, acc = model.evaluate(x_test, y_test, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))

