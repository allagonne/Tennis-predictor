import pandas as pd
from sklearn.neighbors import KNeighborsClassifier as KNN


df = pd.read_csv('atp_data_attributes.csv')
df_drop=df.drop(['player1_name','player1_age','player1_height','player2_name','player2_age','player2_height',],axis = 1)
df_drop["player1_winrate"].fillna(0.5, inplace = True)
df_drop.dropna(inplace=True)

df_drop.isnull().sum()
len(df_drop)

df_p1 = df_drop[df_drop['player1_ranking_points'] > 1000]
df_p2 = df_p1[df_p1['player2_ranking_points'] > 1000]
len(df_p2)

df0 = df_p2[df_p2['outcome']==0]
df1 = df_p2[df_p2['outcome']==1]

df0_downsample = resample(df0,replace=False,n_samples=2000,random_state=3)
df1_downsample = resample(df1,replace=False,n_samples=2000,random_state=3)

df_downsample = pd.concat([df0_downsample, df1_downsample])

X = df_downsample.drop('outcome', axis = 1).copy()
Y = df_downsample['outcome'].copy()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state = 3)
X_train_scaled = scale(X_train)
X_test_scaled = scale(X_test)

knn = KNN()
knn.fit(X_train_scaled, Y_train)
preds_auto = knn.predict(X_test_scaled)
print (classification_report(Y_test,preds_auto))
print ('Accuracy: %.2f' % (accuracy_score(Y_test,preds_auto)*100),'%')