from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

############################### CATEGORICAL FEATURES ENCODING ##################

### The features "player1", "player2" and "Tournament" are treated differently
### from the other features. 

def categorical_features_encoding(cat_data):
    """
    Categorical features encoding.
    Simple one-hot encoding.
    """
    cat_data=cat_data.apply(preprocessing.LabelEncoder().fit_transform)
    ohe=OneHotEncoder()
    cat_data=ohe.fit_transform(cat_data)
    cat_data=pd.DataFrame(cat_data.todense())
    cat_data.columns=["cat_data_"+str(i) for i in range(len(cat_data.columns))]
    cat_data=cat_data.astype(int)
    return cat_data

