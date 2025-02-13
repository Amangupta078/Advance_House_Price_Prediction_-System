# -*- coding: utf-8 -*-
"""Advance_House_Price_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SiM9K5JHZ5T66Fp-MX5K3OZBMeLHFiVx

## Project Name: House Prices: Advanced Regression Techniques

##### Problem Statement ##############

Ask a home buyer to describe their dream house, and they probably won't begin with the height of the basement
 ceiling or the proximity to an east-west railroad.But this playground competition's dataset proves that
much more influences price negotiations than the number of bedrooms or a white-picket fence.

With 79 explanatory variables describing (almost) every aspect of residential homes in Ames, Iowa,
this competition challenges you to predict the final price of each home.


**The main aim of this project is to predict the house price based on various features which we will discuss as we go ahead**

#### Dataset to downloaded from the below link
# **https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data**
"""

##3 Importing libraries
import pandas as pd ## data preprocessing
import numpy as np  ## mathmatical calculation
import matplotlib.pyplot as plt
import seaborn as sns

pd.pandas.set_option('display.max_columns' , None)
#pd.pandas.set_option('display.max_rows' , None)




import warnings
warnings.filterwarnings("ignore")

train = pd.read_csv("/content/train.csv")
test = pd.read_csv("/content/test.csv")

train.head()

test.head()

train.shape

test.shape

df_train = pd.concat([train, test])
df_train.head()

df_train.tail()

df_train.shape

"""### **EDA and Feature Engineering**"""

duplicate = df_train[df_train.duplicated()]
duplicate

print(duplicate)

df_train.duplicated().sum()

df_train.iloc[1450:1470,:]

df_train.info()

df_train.describe()

"""### **Handling numerical  Missing values**"""

len(df_train.columns.unique()), df_train.columns.unique()

missing_values_continious = [feature for feature in df_train.columns if df_train[feature].dtype != "O" and len(df_train[feature].unique()) > 20 and df_train[feature].isnull().sum()>0]
missing_values_continious

len(df_train["LotFrontage"].unique())

df_train.columns

missing_values_continious = []
for feature in df_train.columns:
    if df_train[feature].dtype != "object" and len(df_train[feature].unique())>20:
        missing_values_continious.append(feature)
missing_values_continious

df_train['LotFrontage'].isnull().sum()

df_train['LotFrontage'].isnull().mean()

for feature in missing_values_continious:
    print(f'{feature} = {df_train[feature].isnull().mean() * 100} %')

for feature in missing_values_continious:
    print(f'{feature} = {round(df_train[feature].isnull().mean() , 2) * 100} %')

median_value = df_train["GarageYrBlt"].median()

median_value

for feature in missing_values_continious:
    if feature == "SalePrice":
        pass
    else:
        median_value = df_train[feature].median()
        df_train[feature].fillna(median_value,inplace=True)

for feature in missing_values_continious:
    print(feature, round(df_train[feature].isnull().mean(),4)*100)

df_train.shape

df_train.drop("Id" , inplace=True , axis = 1)

df_train.shape

"""# **2. For Descrete** **bold text**"""

missing_values_descrete = [feature for feature in df_train.columns if df_train[feature].dtype != "O" and len(df_train[feature].unique()) <20 and df_train[feature].isnull().sum()>0]
missing_values_descrete

missing_values_descrete = []
for feature in df_train.columns:
    if df_train[feature].dtype != "object" and len(df_train[feature].unique()) <=20:
        missing_values_descrete.append(feature)
len(missing_values_descrete)

for feature in missing_values_descrete:
    print(f' {feature} = {df_train[feature].isnull().mean()*100} %')

for feature in missing_values_descrete:
    print(f' {feature} = {round(df_train[feature].isnull().mean(),4)*100} %')

df_train["GarageCars"].value_counts()

df_train["GarageCars"].mode()

df_train["GarageCars"].mode()[0]

for feature in missing_values_descrete:
         mode_value = df_train[feature].mode()[0]
         df_train[feature].fillna(mode_value,inplace=True)

for feature in missing_values_descrete:
    print(f' {feature} = {round(df_train[feature].isnull().mean(),4)*100} %')

"""### Handling categorical missing values"""

missing_values_c = [feature for feature in df_train.columns if df_train[feature].dtype == "O" and df_train[feature].isnull().sum()>0]
missing_values_c

missing_values_c = []
for feature in df_train.columns:
    if df_train[feature].dtype == "O" and df_train[feature].isnull().sum()>0:
        missing_values_c.append(feature)
len(missing_values_c)

for feature in missing_values_c:
    print(f' {feature} = {round(df_train[feature].isnull().mean(),4)*100} %')

df_train['Utilities'].value_counts()

for feature in missing_values_c:
         mode_value = df_train[feature].mode()[0]
         df_train[feature].fillna(mode_value,inplace=True)
df_train.drop(["Alley" ,"PoolQC", "Fence", "MiscFeature", "FireplaceQu" ] , axis = 1 , inplace = True)

pd.pandas.set_option('display.max_rows' , None)

df_train.isnull().sum()

df_train.shape

df_train.head()

"""# **Handling year feature**"""

year = [feature for feature in df_train.columns if "Yr" in feature or "Year" in feature]
year

year = []
for feature in df_train.columns:
    if "Yr" in feature or "Year" in feature:
        year.append(feature)
year

for feature in year:
    print(f' {feature}    >>>>   len of data: {len(df_train[feature].unique())}    >>>> {df_train[feature].dtype}')

df_train["YrSold"].value_counts()

df_train.groupby('YrSold')['SalePrice'].median().plot()
plt.xlabel('Year Sold')
plt.ylabel('Median House Price')
plt.title("House Price vs YearSold")
plt.show()

year

df_train[year].head()

for feature in year:
    df_train[feature] = df_train['YrSold']-df_train[feature]
df_train.drop("YrSold", axis = 1 , inplace = True)

df_train.shape

df_train[['YearBuilt', 'YearRemodAdd', 'GarageYrBlt']].head()

df_train.head()

"""# **Handling continious values**"""

continious = [feature for feature in df_train.columns if len(df_train[feature].unique())>20 and df_train[feature].dtype != "O" and feature not in year]
continious

continious = []
for feature in df_train.columns:
     if df_train[feature].dtype != "O" and len(df_train[feature].unique())>20  and feature not in year:
            continious.append(feature)
continious

df_train["LotFrontage"].skew()

## We will be using logarithmic transformation
for feature in continious:
    data = df_train.copy()
    #data[feature]=np.log1p(data[feature])
    ax = sns.distplot(data[feature])
    ax.legend(["skewness : {:0.3f}".format(data[feature].skew())])
    plt.xlabel(feature)
    plt.ylabel('SalesPrice')
    plt.title(feature)
    plt.show()

skewed = [feature for feature in continious if data[feature].skew()<1]
skewed

skewed = []
for feature in continious:
    if abs(df_train[feature].skew())>1:
        skewed.append(feature)
skewed

for feature in continious:
    if feature == "SalePrice":
        pass
    else:
        df_train[feature] = np.log1p(df_train[feature])

## We will be using logarithmic transformation
for feature in continious:
    data = df_train.copy()
    #data[feature]=np.log1p(data[feature])
    ax = sns.distplot(data[feature])
    ax.legend(["skewness : {:0.3f}".format(data[feature].skew())])
    plt.xlabel(feature)
    plt.ylabel('SalesPrice')
    plt.title(feature)
    plt.show()

df_train.shape

# correlation heatmap
plt.figure(figsize=(25,25))
ax = sns.heatmap(df_train[continious].corr(), cmap = "coolwarm", annot=True, linewidth=2)

# correlation heatmap of higly correlated features with SalePrice
low_corr = df_train[continious].corr()
low_corr_features = low_corr.index[low_corr["SalePrice"] < 0.10]
low_corr_features

df_train.drop(low_corr_features,axis=1,inplace=True)

df_train.shape

"""## Handling categorical variables"""

Categorical = [feature for feature in df_train.columns if df_train[feature].dtype =="O"]
Categorical

Categorical = []
for feature in df_train.columns:
  if df_train[feature].dtype=="object":
      Categorical.append(feature)
len(Categorical)

Categorical

for feature in Categorical:
  df_train.groupby(feature)["SalePrice"].median().plot.bar()
  sns.barplot(x =df_train[feature], y = df_train["SalePrice"])
  plt.xlabel(feature)
  plt.ylabel("Sale Price")
  plt.title(feature)
  plt.show()

Categorical

from pandas.api.types import CategoricalDtype

"""# **Ordinal**"""

df_train['BsmtCond'].unique()

df_train['BsmtCond'].value_counts()

df_train['BsmtCond']= df_train['BsmtCond'].astype(CategoricalDtype(categories=['TA', 'Gd', 'Fa', 'Po'], ordered=True)).cat.codes

df_train["BsmtCond"]

df_train['BsmtCond'].value_counts()

df_train['BsmtExposure'] = df_train['BsmtExposure'].astype(CategoricalDtype(categories=['NA', 'Mn', 'Av', 'Gd'], ordered = True)).cat.codes
df_train['BsmtFinType1'] = df_train['BsmtFinType1'].astype(CategoricalDtype(categories=['NA', 'Unf', 'LwQ', 'Rec', 'BLQ','ALQ', 'GLQ'], ordered = True)).cat.codes
df_train['BsmtFinType2'] = df_train['BsmtFinType2'].astype(CategoricalDtype(categories=['NA', 'Unf', 'LwQ', 'Rec', 'BLQ','ALQ', 'GLQ'], ordered = True)).cat.codes
df_train['BsmtQual'] = df_train['BsmtQual'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['ExterQual'] = df_train['ExterQual'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['ExterCond'] = df_train['ExterCond'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['Functional'] = df_train['Functional'].astype(CategoricalDtype(categories=['Sal', 'Sev', 'Maj2', 'Maj1', 'Mod','Min2','Min1', 'Typ'], ordered = True)).cat.codes
df_train['GarageCond'] = df_train['GarageCond'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['GarageQual'] = df_train['GarageQual'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['GarageFinish'] = df_train['GarageFinish'].astype(CategoricalDtype(categories=['NA', 'Unf', 'RFn', 'Fin'], ordered = True)).cat.codes
df_train['HeatingQC'] = df_train['HeatingQC'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['KitchenQual'] = df_train['KitchenQual'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df_train['PavedDrive'] = df_train['PavedDrive'].astype(CategoricalDtype(categories=['N', 'P', 'Y'], ordered = True)).cat.codes
df_train['Utilities'] = df_train['Utilities'].astype(CategoricalDtype(categories=['ELO', 'NASeWa', 'NASeWr', 'AllPub'], ordered = True)).cat.codes

ordinal = ["BsmtCond" , "BsmtExposure" , "BsmtFinType1" , "BsmtFinType2" , "BsmtQual" , "ExterQual" , "ExterCond" , "Functional",
          "GarageCond" , "GarageQual" , "GarageFinish" , "HeatingQC" , "KitchenQual" , "PavedDrive" , "Utilities"]

len(ordinal)

df_train.shape

df_train.head()

"""# **Nominal**

# **One Hot Encoding Technique**
"""

nominal = [feature for feature in Categorical if feature not in ordinal]

nominal

len(nominal)

nominal = []
for feature in Categorical:
  if feature not in ordinal:
    nominal.append(feature)
len(nominal)

for feature in nominal:
  print(feature ,len(df_train[feature].unique()))

new_nominal=["Neighborhood","Exterior1st","Exterior2nd"]
new_nominal

Nominal_1 = []
for feature in nominal:
  if feature not in new_nominal:
    Nominal_1.append(feature)
len(Nominal_1)

Nominal_variable = pd.get_dummies(df_train[Nominal_1], drop_first=True)
#Nominal_variable.drop(new_nominal, inplace = True)

Nominal_variable.shape

Nominal_variable = Nominal_variable.astype(int)

Nominal_variable.head()

df_train['Neighborhood'].value_counts()

def top_ten(feature):
  top_ten = []
  for x in feature.value_counts().sort_values(ascending=False).head(10).index:
    top_ten.append(x)
  return top_ten

top_ten(df_train["Neighborhood"])

top_10_Neighborhood=top_ten(df_train["Neighborhood"])
top_10_Exterior1st=top_ten(df_train["Exterior1st"])
top_10_Exterior2nd =top_ten(df_train["Exterior2nd"])

for i in top_10_Neighborhood:
  df_train[i]=np.where(df_train["Neighborhood"]==i,1,0)
for lable in top_10_Exterior1st:
  df_train[i]=np.where(df_train["Exterior1st"]==lable,1,0)
for a in top_10_Exterior2nd:
  df_train[i]=np.where(df_train["Exterior2nd"]==a,1,0)

df_train[top_10_Neighborhood].head()

df_train.head()

len(nominal)

df_train.shape

df_train.drop(nominal,axis=1,inplace=True)

df_train.head()

df_train.shape

train=pd.concat([Nominal_variable,df_train],axis=1)

train.shape

train.head()

train.columns.duplicated().sum()

train.isnull().sum()

"""# **Spilit The Dataset Into Train And Test**"""

train_df = train.iloc[:1460,:]
df_test = train.iloc[1460:,:]

print(train_df.shape)
print(df_test.shape)

df_test["SalePrice"]

test = df_test.drop("SalePrice" , axis = 1)
test.shape

X=train_df.drop("SalePrice",axis=1)
y= train_df["SalePrice"]

X.head()

X.shape

y.head()

"""# **Feature Selection**"""

from sklearn.ensemble import ExtraTreesRegressor
model=ExtraTreesRegressor()
model.fit(X,y)

print(model.feature_importances_)

X.columns

plt.figure(figsize=(16,10))
ranked_feature = pd.Series(model.feature_importances_,X.columns)
ranked_feature.nlargest(40).plot(kind="barh")
plt.show()

features = ranked_feature.nlargest(23)
features

features.index

X = train_df[features.index]

X.shape

X.head()

"""# **Model Building**"""

## split dataset into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 5)

"""# **Robust Scaller**"""

df_test= test[features.index]
df_test.head()

df_test.shape

from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)
df_test= scaler.fit_transform(df_test)

X_train

X_test

df_test

"""## **Machine Learning Modeling**

### **Linear Regression**
"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score# for calculating mean_squared error,for measering the goodness of best fit line


reg =LinearRegression()
reg.fit(X_train,y_train)


y_pred_train=reg.predict(X_train)
rmse1=np.sqrt(mean_squared_error(y_train,y_pred_train))
train_score=r2_score(y_train,y_pred_train)


y_pred=reg.predict(X_test)
rmse2=np.sqrt(mean_squared_error(y_test,y_pred))
test_score=r2_score(y_test,y_pred)

print(f"Value Of R2_Score For Training Data is {train_score}")
print(f"RMSE Value is {rmse1}")
print("\n")
print(f"Value Of R2_Score For Test Data is {test_score}")
print(f"RMSE Value is {rmse2}")

"""## **Decision Tree**"""

from sklearn.tree import DecisionTreeRegressor
DT = DecisionTreeRegressor()
DT.fit(X_train,y_train)

prediction = DT.predict(X_test)
score = r2_score(y_test , prediction)

print(score)

"""## **Random Forest**"""

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor()
rf.fit(X_train,y_train)

y_pred_rf = rf.predict(X_test)
score_rf =r2_score(y_test,y_pred_rf)
rmse=np.sqrt(mean_squared_error(y_test,y_pred_rf))

print(f"Value Of R2 Score {score_rf}")
print(f"Value Of RMSE {rmse}")

from sklearn.model_selection import cross_val_score
cross_validation =cross_val_score(estimator=rf,X=X_train,y=y_train,cv=10,verbose=True)
print("Cross validation accuracy of random forest model = ", cross_validation)
print("\n Cross validation mean accuracy of random forest model =",cross_validation.mean())

"""## **XGBoost**"""

import xgboost

xg = xgboost.XGBRegressor()
xg.fit(X_train,y_train)

y_pred_xg=xg.predict(X_test,)
score_xg=r2_score(y_test,y_pred)
xg_rmse=np.sqrt(mean_squared_error(y_test,y_pred))

print(f"value of R^2 is {score_xg}")
print(f"rmse value is {xg_rmse}")

from sklearn.model_selection import cross_val_score
cross_validation =cross_val_score(estimator=xg,X=X_train,y=y_train,cv=10,verbose=True)
print("Cross validation accuracy of random forest model = ", cross_validation)
print("\n Cross validation mean accuracy of random forest model =",cross_validation.mean())

y_pred_hyper = xg.predict(df_test)
y_pred_hyper

df = pd.read_csv("test.csv" , usecols = ["Id"])

df

df.head()

submit_df_test=pd.concat([df["Id"],pd.DataFrame(y_pred_hyper)],axis=1)
submit_df_test

submit_df_test.head(10)

submit_df_test.info()

"""# **Hyper Parameter Tunning**"""

from sklearn.model_selection import RandomizedSearchCV,GridSearchCV

#Randomized Search CV
# Number of trees in random forest
n_estimators=[int(x) for x in np.linspace(start=100,stop=1200,num=12) ]
# Number of features to consider at every split
#criterion = ["squared_error" , "absolute_error" , "poisson"]
max_features=["auto","sqrt","log2"]
# Maximum number of levels in tree
max_depth=([int(x) for x in np.linspace(5,30,num=6)])
# Minimum number of samples required to split a node
min_samples_split=[2,5,10,15,100]
# Minimum number of samples required at each leaf node
min_samples_leaf=[1,2,5,10]

# Create the random grid
random_grid ={"n_estimators":n_estimators,
              "max_features":max_features,
              "max_depth":max_depth,
              "min_samples_split":min_samples_split,
              "min_samples_leaf":min_samples_leaf}

rf_random=RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=10, cv=5, verbose=2, n_jobs=-1, random_state=5)
rf_random

rf_random.fit(X_train,y_train)

rf_random.best_params_

prediction = rf_random.predict(X_test)
score_rf=r2_score(y_test,prediction)


print(f"value of R^2 is {score_rf}")
print('RMSE:', np.sqrt(mean_squared_error(y_test, prediction)))

y_pred_hyper = rf_random.predict(df_test)
y_pred_hyper

"""# **Hyper Parameter Tunning with XGBoost**"""

params={
  "learning_rate"    : [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ,
 "max_depth"        : [ 3, 4, 5, 6, 8, 10, 12, 15],
 "min_child_weight" : [ 1, 3, 5, 7 ],
 "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ],
 "colsample_bytree" : [ 0.3, 0.4, 0.5 , 0.7 ]
}

xgb_random=RandomizedSearchCV(xg,param_distributions=params,n_iter=10,scoring="r2",n_jobs=-1,cv=5,verbose=3)
xgb_random

xgb_random.fit(X_train , y_train)
y_pred = xgb_random.predict(df_test)
y_pred

xgb_random.best_params_

prediction = xgb_random.predict(X_test)
score_rf=r2_score(y_test,prediction)


print(f"value of R^2 is {score_rf}")
print('RMSE:', np.sqrt(mean_squared_error(y_test, prediction)))

df = pd.read_csv("test.csv" , usecols = ["Id"])
submit_test1 = pd.concat([df["Id"], pd.DataFrame(y_pred)], axis=1)
submit_test1.columns=['Id', 'SalePrice']

# submit_test1 = submit_test1.astype({'Id': 'int', 'SalePrice': 'float'})
submit_test1.to_csv('sample_submission_xgboost.csv', index=False)

submit_test1

submit_test1.head(15)















