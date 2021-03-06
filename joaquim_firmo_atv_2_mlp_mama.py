# -*- coding: utf-8 -*-
"""Joaquim_Firmo_ATV_2_MLP_MAMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aHPFYR0d4yC5hx3yiKqwZPzWJTnWfOVg
"""

# importando o conjunto de dados:  breast_cancer_formated.csv 
from google.colab import files
data = files.upload()

# lendo os dados e criando o dataFrame
import pandas as pd
import io

df = pd.read_csv(io.StringIO(data['breast_cancer_formated.csv'].decode('utf-8')))

# renomeando as colunas
df=df.rename(columns = {'5.000000000000000000e+00':'Clump Thickness','1.000000000000000000e+00':'Uniformity of Cell Size','1.000000000000000000e+00.1':'Uniformity of Cell Shape:','1.000000000000000000e+00.2':'Marginal Adhesion','2.000000000000000000e+00': 'Single Epithelial Cell Size','1.000000000000000000e+00.3': 'Bare Nucle','3.000000000000000000e+00': 'Bland Chromatin','1.000000000000000000e+00.4':'Normal Nucleoli', '1.000000000000000000e+00.5':'Mitoses', '0.000000000000000000e+00':'Classes'})
df

#X features/características e y = target/rotulos( quem o modelo quer prevê)
# linhas e colunas das features e target as classes.
X = df.iloc[:,:-1].values
y = df.iloc[:,9].values

print(X)
print(y)

from sklearn.model_selection import train_test_split
# divide os dados em dois conjuntos (treino e teste)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


print(X_train.shape)
print(y_train.shape)

print(X_test.shape)
print(y_test.shape)

# importa o MLPClassifier da biblioteca sklearn
from sklearn.neural_network import MLPClassifier
# instancia um objeto da tecnica MLPClassifier
mlp = MLPClassifier(random_state=1, max_iter=600, activation='relu',learning_rate_init=0.01)
# treina um modelo de classificacao
mlp.fit(X_train, y_train)

import matplotlib.pyplot as plt
plt.plot(mlp.loss_curve_,label="treino")

plt.title("Curva do erro de treinamento \n learning_rate 0.01 \n max_iter 600")
plt.xlabel("Iterações")
plt.ylabel("Erro")
plt.legend()

# comparação do resultado predito com o esperado
y_pred=mlp.predict(X_test)

y_true = y_test

print("Classe predita:   ", y_pred)
print("Classe verdadeira:", y_true)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_true, y_pred)

#tn = verdadeiro negativo
#fp = falso positivo 
#fn = falso negativo 
#tp = verdadeiro positivo  

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
(tn, fp, fn, tp)

from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
acuSemGridS = acc
[acc, prec, f1, recall]

# precisão do resultado
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#importando o GridSearchCV
from sklearn.model_selection import GridSearchCV
mlp2 = MLPClassifier(random_state=1)

parameters = { 'hidden_layer_sizes':[(100,100),(10,100,120),(100,120,180)],'learning_rate_init': [0.01,0.1,0.001] ,'activation': ["identity","tanh", "relu"],'max_iter': [100,300,500]}

grid = GridSearchCV(mlp2,parameters)
grid.fit(X_train, y_train)

#tabela com as 5 melhores combinações encontradas pela GrindSearchCV

pd.DataFrame(grid.cv_results_).sort_values(by=['rank_test_score'])[['params','rank_test_score','mean_test_score']].head(5)

# Imprime os parâmetros que produziram o ".best_score_".
grid.best_params_

# Imprimindo o score.
grid.best_score_

from statistics import mean
l_acc = []
l_prec = []
l_f1 = []
l_recall = []

# validação cruzada com k-fold com o melhor modelo encontrado pelo GridSearchCV
from sklearn.model_selection import KFold
kf = KFold(n_splits=10)
mlpBest = MLPClassifier(hidden_layer_sizes = (10,100,120),random_state=1, max_iter=100, activation='identity',learning_rate_init = 0.001)

for train_indices, test_indices in kf.split(X):
    mlpBest.fit(X[train_indices], y[train_indices])
    y_pred=mlp.predict(X[test_indices])
    acc = accuracy_score(y[test_indices], y_pred)
    prec = precision_score(y[test_indices], y_pred, average='macro')
    f1 = f1_score(y[test_indices], y_pred, average='macro')
    recall = recall_score(y[test_indices], y_pred, average='macro')
    l_acc.append(acc)
    l_prec.append(prec)
    l_f1.append(f1)
    l_recall.append(recall)

#media das metricas
print("A média da  acc é ", round(mean(l_acc),2))
print("A média da precisão é ", round(mean(l_prec),2))
print("A média f1 é ", round(mean(l_f1),2))
print("A média do recall é ", round(mean(l_recall),2))

#comparando os resultados da acuracia com e sem o uso do GridSearchCV
acCG = round(mean(l_acc),2)
acSG = round(acuSemGridS,2)
table = pd.DataFrame({"MLB": [acSG, acCG]} ,index=['Sem GridSearchCV','Com GridSearchCV'])
table.style.set_caption('Tabela de Comparação das acurácia')