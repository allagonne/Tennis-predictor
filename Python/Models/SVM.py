import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.decomposition import PCA

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

df0_downsample = resample(df0,replace=False,n_samples=1000,random_state=9)
df1_downsample = resample(df1,replace=False,n_samples=1000,random_state=9)

df_downsample = pd.concat([df0_downsample, df1_downsample])

X = df_downsample.drop('outcome', axis = 1).copy()
Y = df_downsample['outcome'].copy()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state = 9)
X_train_scaled = scale(X_train)
X_test_scaled = scale(X_test)

svm = SVC(random_state = 9)
svm.fit(X_train_scaled, Y_train)

plot_confusion_matrix(svm, X_test_scaled, Y_test, display_labels=['P1 lost','P1 won'])
preds_auto = svm.predict(X_test_scaled)
print (classification_report(Y_test,preds_auto))
print ('Accuracy: %.2f' % (accuracy_score(Y_test,preds_auto)*100),'%')

param_grid =[
    {'C': [0.5, 1, 10, 100],
    'gamma' : ['scale', 1, 0.1, 0.01, 0.001, 0.0001],
    'kernel':['rbf']},
]

optimal_params = GridSearchCV(
        SVC(),
        param_grid,
        cv = 5,
        scoring = 'accuracy',
        verbose = 0
)
optimal_params.fit(X_train_scaled, Y_train)
print(optimal_params.best_params_)

svm_optimized = SVC(random_state = 9, C = 0.5, gamma = 0.01)
svm_optimized.fit(X_train_scaled, Y_train)

plot_confusion_matrix(svm_optimized, X_test_scaled, Y_test, display_labels=['P1 lost','P1 won'])
preds=svm_optimized.predict(X_test_scaled)
print ('Accuracy: %.2f' % (accuracy_score(Y_test,preds)*100),'%')
print (classification_report(Y_test,preds))

pca = PCA()
X_train_pca = pca.fit_transform(X_train_scaled)

per_var = np.round(pca.explained_variance_ratio_ * 100, decimals = 1)
labels = [str(x) for x  in range(1, len(per_var)+1)]

plt.bar(x=range(1, len(per_var)+1), height = per_var)
plt.tick_params(
    axis = 'x',
    which ='both',
    bottom = False,
    top = False,
    labelbottom = False)
plt.ylabel('Percentage of explained variables')
plt.xlabel('Principal component')
plt.title('Scree Plot')
plt.show()

print(pca.explained_variance_ratio_)