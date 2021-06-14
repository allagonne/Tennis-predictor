import pandas as pd
import numpy as np
#import xgboost as xgb
import sklearn
from sklearn.model_selection import StratifiedKFold,KFold
import os.path as path
import glob

one_up = path.abspath(path.join(__file__ ,".."))
two_up =  path.abspath(path.join(__file__ ,"../.."))
three_up =  path.abspath(path.join(__file__ ,"../../.."))


path = three_up + '/Data/Generated csv/atp_data_attributes.csv'
ml_dataset = pd.read_csv(path)

