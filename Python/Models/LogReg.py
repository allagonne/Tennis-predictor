import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


data = pd.read_csv("../../Data/Generated csv/atp_data_attributes.csv")
data = data.dropna(subset=['player1_ranking_points', 'player2_ranking_points'])
data["player1_winrate"] = data["player1_winrate"].fillna(0.5)
data1 = data[data['player1_ranking_points'] > 2000]
data = data1[data1['player2_ranking_points'] > 2000]

## separate X and y
# we drop many useless or with NaN variables
X_extract = ['outcome','player1_name','player2_name', 'player1_height','player2_height', 'player1_age','player1_ranking_points','player1_W/total_games','player1_W/total_games_per_surface','player2_age','player2_ranking_points','player2_W/total_games','player2_W/total_games_per_surface', 'player1_winrate']
X = data.drop(columns = X_extract)
y = data.loc[:, data.columns == 'outcome']
X_bis = data[['player1_ranking_points', 'player1_elo', 'player2_ranking_points' , 'player2_elo']] ## a smaller X

## logistic regression part
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
columns = X_train.columns
print('sample sizes : X {}, y {}, X_train {},X_test {},y_train {},y_test {}'.format(X.shape, y.shape, X_train.shape, X_test.shape, y_train.shape, y_test.shape)) ##sizes of train and test X and y
X_bis_train, X_bis_test, y_bis_train, y_bis_test = train_test_split(X_bis, y, test_size=0.3, random_state=1)
print('sample sizes : X_bis {}, y {}, X_bis_train {},X_bis_test {},y_train {},y_test {}'.format(X_bis.shape, y.shape, X_bis_train.shape, X_bis_test.shape, y_train.shape, y_test.shape)) ##sizes of train and test, X_bis and y
logreg = LogisticRegression(max_iter = 2000, penalty = 'none')
logreg_bis = LogisticRegression(max_iter = 2000, penalty = 'none')
logreg.fit(X_train, y_train.values.ravel())
logreg_bis.fit(X_bis_train, y_bis_train.values.ravel())

## get the accuracy results
y_pred = logreg.predict(X_test)
y_bis_pred = logreg_bis.predict(X_bis_test)
print('Accuracy of logistic regression classifier X on test set: {:.3f}'.format(logreg.score(X_test, y_test)))
print('Accuracy of logistic regression classifier X_bis on test set: {:.3f}'.format(logreg_bis.score(X_bis_test, y_bis_test)))