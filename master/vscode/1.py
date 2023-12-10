
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import f1_score
from sklearn.metrics import det_curve
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import matplotlib.pyplot as plt
import  pandas as pd
import numpy as np

lectura = pd.read_csv('datos_infarto.csv')

y = lectura['Infarto']
x = lectura.drop(['Infarto'], axis=1)
columnas_a_dummies = ['Genero','Tipo_Trabajo','Residencia_habitual','Casado','Fumador']
df_dummies = pd.get_dummies(x, columns=columnas_a_dummies)
colnomod = ['Edad','Hipertension','Enfermedad_Corazon','Nivel_medio_glucosa','IMC']
df_dummies[colnomod] = x[colnomod]
df_dummies = df_dummies.drop(['ID'], axis=1)
min_max_scaler = MinMaxScaler()
data_min_max = min_max_scaler.fit_transform(df_dummies)
data_min_max_df = pd.DataFrame(data_min_max, columns=df_dummies.columns)
x_train, x_test, y_train, y_test = train_test_split(data_min_max_df, y, test_size=0.15, random_state=42)


oversample = RandomOverSampler(sampling_strategy='minority', random_state=42)
undersample = RandomUnderSampler(sampling_strategy='majority', random_state=42)
x_under, y_under = undersample.fit_resample(x_train, y_train)
x_over, y_over = oversample.fit_resample(x_train, y_train)





x_train = x_over
y_train = y_over
def LR (x_train, y_train):
    lr = LogisticRegression(class_weight='balanced' ,max_iter=1000)
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    return y_pred

def Dt (x_train, y_train):
    
    
    clf = tree.DecisionTreeClassifier(random_state=42, max_depth=2)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    return y_pred
    
def metrics(y_test,y_pred):
    err= np.mean(np.abs(y_test-y_pred))
    print(f'Error: {err}')
    acc = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {acc}')
    F1 = f1_score(y_test, y_pred, average='weighted')
    print(f'F1: {F1}')
    det = det_curve(y_test, y_pred)
    print(f'Det: {det}')
    rec = recall_score(y_test, y_pred)
    print(f'Recall: {rec}')
    conf = confusion_matrix(y_test, y_pred, normalize='true')	
    disp = ConfusionMatrixDisplay(confusion_matrix=conf)
    disp.plot()
    plt.show()
    
 
    



model = LR(x_train, y_train)
model2 = Dt(x_under, y_under)

metrics(y_test, model)
metrics(y_test, model2)

  