from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

############################### CATEGORICAL FEATURES ENCODING ##################

### The features "player1", "player2" and "Tournament" are treated differently
### from the other features. 
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

    #cat_data.columns=["cat_feature_"+str(i) for i in range(len(cat_data.columns))]
def categorical_features_encoding(cat_data):
    """
    Categorical features encoding.
    Simple one-hot encoding.
    """

    cat_data=cat_data.apply(preprocessing.LabelEncoder().fit_transform)
    ohe=OneHotEncoder()
    cat_data=ohe.fit_transform(cat_data)
    cat_data=pd.DataFrame(cat_data.todense())
    cat_data.columns=[
                    'surface_1',
                    'surface_2',
                    'surface_3',
                    'draw_size_1',
                    'draw_size_2',
                    'draw_size_3',
                    'draw_size_4',
                    'draw_size_5',
                    'draw_size_6',
                    'draw_size_7',
                    'draw_size_8',
                    'draw_size_9',
                    'draw_size_10',
                    'best_of_3',
                    'best_of_5',
                    'round_1',
                    'round_2',
                    'round_3',
                    'round_4',
                    'round_5',
                    'round_6',
                    'round_7',
                    'round_8',
                    'player1_hand_1',
                    'player1_hand_2',
                    'player1_hand_3',
                    'player2_hand_1',
                    'player2_hand_2',
                    'player2_hand_3'
                  ]
    cat_data=cat_data.astype(int)
    return cat_data
