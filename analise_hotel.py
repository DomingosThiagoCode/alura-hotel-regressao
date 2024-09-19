# -*- coding: utf-8 -*-
"""Analise_hotel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GGHPbOM7lyR899yhbyJzLPwZw-xv_h7E

# Bibliotecas:
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from statsmodels.formula.api import ols
from sklearn.metrics import r2_score
import statsmodels.api as sm

"""# Dados:"""

dados = pd.read_csv("hoteis.csv")

dados.info()

#Correlação: Medir relação linear entre variáveis
corr = dados.corr()

corr["Preco"]

#Distribuição da variavél Preco
sns.displot(dados["Preco"],kde=True,color="blue")
plt.title('Distribuição do preço médio dos hotéis')
plt.xlabel('Preço')
plt.ylabel('Quantidade')
plt.show()

"""# Análise da Correlação entre Estrelas e o Preço:"""

#Definindo X e Y para o train_test_split:
y = dados["Preco"]
x = dados.drop(columns='Preco')

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)

df_train = pd.DataFrame(data=x_train)
df_train['Preco']= y_train

modelo_0 = ols('Preco ~Estrelas',data = df_train).fit()

print(modelo_0.summary())

#R²:
print(modelo_0.rsquared)

#Residuos:
modelo_0.resid

modelo_0.resid.hist()
plt.title("Distribuição dos resíduos")
plt.show()

#Definindo o Y previsto
y_predict = modelo_0.predict(x_test)

#R² previsto:
print("Predição de R²: ",r2_score(y_test,y_predict))

"""# Analisando correlação entre as variáveis:"""

sns.pairplot(df_train)

dados.columns

#Olhando apenas y_vars = 'Preco'
sns.pairplot(dados,y_vars='Preco',x_vars=['Estrelas', 'ProximidadeTurismo', 'Capacidade'])

#Adicionando o constante:
x_train = sm.add_constant(x_train)
x_train.head()

x_train.columns

#Criando modelo de regressão (sem fórmula):saturadp
modelo_1 = sm.OLS(y_train,x_train[['const','Estrelas', 'ProximidadeTurismo', 'Capacidade']]).fit()

#Criando modelo de regressão sem as Estrelas:
modelo_2 = sm.OLS(y_train,x_train[['const','ProximidadeTurismo', 'Capacidade']]).fit()

#Criando modelo de regressão sem as capacidades:
modelo_3 = sm.OLS(y_train,x_train[['const','ProximidadeTurismo','Estrelas']]).fit()

#Resumo modelo 1:
print(modelo_1.summary())

#Resumo modelo 2:
print(modelo_2.summary())

#Resumo modelo 3:
print(modelo_3.summary())

#Parametros utilizados por cada modelo:
print(len(modelo_0.params))
print(len(modelo_1.params))
print(len(modelo_2.params))
print(len(modelo_3.params))

#Comparação entre os modelos utilizando o R²:
print("R²")
print("Modelo 0: ",modelo_0.rsquared)
print("Modelo 1: ",modelo_1.rsquared)
print("Modelo 2: ",modelo_2.rsquared)
print("Modelo 3: ",modelo_3.rsquared)

"""Para a resolução deste exercicio escolheria o Modelo 1, pois é a que a presenta uma maior correlação e R² quando comparada a coluna preço."""