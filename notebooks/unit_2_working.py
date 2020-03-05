# -*- coding: utf-8 -*-
"""unit_2_working.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GbuBR-54wqmRb7T1s0RwKmgGoYMqjYvQ
"""

# united 2 build working file 

# we will move the nice completed file to 'unit_2_production' when finished
#   this will allow me to fancy it up.

#commented out to work with my own hosted csv on google docs as the source 
# %%capture
# import sys

# # If you're on Colab:
# if 'google.colab' in sys.modules:
#     DATA_PATH = 'https://raw.githubusercontent.com/LambdaSchool/DS-Unit-2-Applied-Modeling/master/data/'
#     !pip install category_encoders==2.*
#     !pip install pandas-profiling==2.*

# # If you're working locally:
# else:
#     DATA_PATH = '../data/'

# Commented out IPython magic to ensure Python compatibility.
# import my main squeezeS
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# %matplotlib inline
import seaborn as sns

!pip install category_encoders==2.*
!pip install pandas-profiling==2.*

# import the dataset - lets establish some baselines 
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR6LzWx6lS1FOS0Fl2QFF1CJeNrhsH0MxLmqEp8vbYj0Z-zDRm5Xwu4PQkP9WbCSokITS4UwcF9hCQ3/pub?output=csv')

# for dealing with all the ugly column names. 
df.columns = (
    df.columns
    .str.replace(' - ', '_')
    .str.replace('/', '_')
    .str.replace(',', '_')
    .str.replace('.', '_')
    .str.replace('(', '_')
    .str.replace(')', '_')
    .str.replace(' ', '_')
    .str.replace('__', '_')
    .str.lower()
)

print(df.shape)
df.head()

# Count the mssing values
df.isna().sum().sort_values()

df.dtypes

# Pandas Profiling
from pandas_profiling import ProfileReport
profile = ProfileReport(df, minimal=True).to_notebook_iframe()

profile

"""# Baseline Accuracy"""

df['cost_of_living_index'].describe()

#This is the cost of living mae for the entire dataset together 
guess = df['cost_of_living_index'].mean()
error = guess - df['cost_of_living_index']
mean_absolute_error = error.abs().mean()
# repeat it back in a clearer format 
print(f'Guessed : {guess:,.2f} for every city ')
print(f'Our cost of living index would be off by {mean_absolute_error:,.2f} on average.')

# The distribution is right-skewed double humped
sns.distplot(df['cost_of_living_index']);

"""# Train Test Split"""

# from sklearn.model_selection import train_test_split I ended up not using this


"""
The following is an example of what the sklearn approach would be
# train = pd.merge(pd.read_csv(DATA_PATH+'waterpumps/train_features.csv'), 
#                  pd.read_csv(DATA_PATH+'waterpumps/train_labels.csv'))
# test = pd.read_csv(DATA_PATH+'waterpumps/test_features.csv')

# # Split train into train & val
# train, val = train_test_split(train, train_size=0.80, test_size=0.20, 
#                               stratify=train['status_group'], random_state=42)

# sample_submission = pd.read_csv(DATA_PATH+'waterpumps/sample_submission.csv')


# train.shape, val.shape, test.shape

"""

# split is the np function that train test split uses and split function 
# is easier for me to understand

# make a train test val split 
# 80% 10% 10%
train, val, test = np.split(df.sample(frac=1, random_state=42), [int(.8*len(df)), int(.9*len(df))])

print(train.shape)
print(val.shape)
print(test.shape)



#This is the cost of living mae for the train dataset alone now
train_guess = train['cost_of_living_index'].mean()
train_error = train_guess - train['cost_of_living_index']
train_mean_absolute_error = train_error.abs().mean()
# repeat it back in a clearer format 
print(f'*Training Set* Guessed : {train_guess:,.2f} for every city ')
print(f'Our cost of living index would be off by {train_mean_absolute_error:,.2f} on average. *Training Set*')

"""# Wrangle Function and Feature engineering"""

df.columns

train['domestic_beer_0_5_liter_bottle_'].describe()

def clean(X):

    # Prevent SettingWithCopyWarning
    X = X.copy()

    X = X.drop(columns='cost_of_living_plus_rent')
    # drop the column that will leak data into the model 
    # drop

    # # convert pd_to datetime 
    # X['inspection_date'] = pd.to_datetime(X['inspection_date'], infer_datetime_format=True)

    # # drop columns masking
    # drop_cols = ['dba_name', 'aka_name', 'address', 'state', 'location']
    # X = X.drop(columns=drop_cols)

    # # deal with them zeroes and nannies 
    # # also assign a columne for missing values incase of significance 
    # cols_with_zeros = ['longitude', 'latitude', 'zip', 'city', 'violations']
    # for col in cols_with_zeros:
    #     X[col] = X[col].replace(0, np.nan)
    #     X[col+'_MISSING'] = X[col].isnull()

    # domestic_beer_0_5_liter_bottle_
    # X['domestic_beer_0_5_liter_bottle_'] = X['domestic_beer_0_5_liter_bottle_'].replace(0, np.nan)
    # Replacing with nan breaks my linear regression model 

    # fill column with the mean price 
    # or I could impute mean
    # mean_beer = X[X['domestic_beer_0_5_liter_bottle_']>0]['domestic_beer_0_5_liter_bottle_'].mean()
    # X.loc[X['domestic_beer_0_5_liter_bottle_']==0, 'domestic_beer_0_5_liter_bottle_'] = int(mean_beer)

    X.fillna(X.mean(), inplace=True)
    #or alternatively X = X.fillna(X.mean())

    # mean_license = X[X['license_#']>0]['license_#'].mean()
    # X.loc[X['license_#']==0, 'license_#'] = int(mean_license)

    # # reduce cardinality for inspection type 
    # # Get a list of the top 10 'inspection_type'
    # top10_insp_type = X['inspection_type'].value_counts()[:10].index

    # # At locations where the 'inspection_type' is NOT in the top 10, 
    # # replace the 'inspection_type' with 'Other'
    # X.loc[~X['inspection_type'].isin(top10_insp_type), 'inspection_type'] = 'Other'  

    # # reduce cardinality for facility_type
    # # Get a list of the top 10 'facility_type'
    # top10_fac_type = X['facility_type'].value_counts()[:10].index

    # # At locations where the 'facility_type' is NOT in the top 10, 
    # # replace the 'facility_type' with 'Other'
    # X.loc[~X['facility_type'].isin(top10_fac_type), 'facility_type'] = 'Other'  

    # # make a column about violation string length - longer is badder
    # X['violations_length'] = X['violations'].str.len()    
    
    # # return cleaned df
    return X

train = clean(train)
val = clean(val)
test = clean(test)

# mean_beer = X[X['domestic_beer_0_5_liter_bottle_']>0]['domestic_beer_0_5_liter_bottle_'].mean()
#     X.loc[X['domestic_beer_0_5_liter_bottle_']==0, 'domestic_beer_0_5_liter_bottle_'] = int(mean_beer)


train['domestic_beer_0_5_liter_bottle_'].describe()

# Seaborn pairplot to show relationship of the data to my variables

# pp = sns.pairplot(data=data,
#                   y_vars=['age'],
#                   x_vars=['weight', 'height', 'happiness'])

# cost_of_living_plus_rent restaurant_price_index

# apartment_city_center_1bed apartment_utilities internet_monthly groceries_index

pairplot = sns.pairplot(data=train,
                        y_vars=['cost_of_living_index'],
                        x_vars= ['rent_index', 'restaurant_price_index'])

pairplot = sns.pairplot(data=train,
                        y_vars=['cost_of_living_index'],
                        x_vars= ['apartment_city_center_1bed', 'apartment_utilities', 'internet_monthly', 'groceries_index'])

numeric = train.select_dtypes('number')
for col in sorted(numeric.columns):
    sns.lmplot(x=col, y='cost_of_living_index', data=train, scatter_kws=dict(alpha=0.65))
    plt.show()

"""# !!! Save Space for doing Cross Validation here !!!"""

# put my cross validation code here







"""# Target / Features X train - y feature matrix"""

# The COL Index is the target
target = 'cost_of_living_index'

# Get a dataframe with all train columns except the target
train_features = train.drop(columns=[target])

# Get a list of the numeric features
numeric_features = train_features.select_dtypes(include='number').columns.tolist()

# Get a series with the cardinality of the nonnumeric features
cardinality = train_features.select_dtypes(exclude='number').nunique()

# Get a list of all categorical features with cardinality <= 60
# increased to 60 for this exercise 
categorical_features = cardinality[cardinality <= 60].index.tolist()

# Combine the lists 
features = numeric_features + categorical_features

# Arrange data into X features matrix and y target vector 

X_train = train[features]
y_train = train[target]

X_val = val[features]
y_val = val[target]

X_test = test[features]
y_test = test[target]



print(X_train.shape)
X_train.head()

"""# Working pipe here - This is using all the features"""

X_train = train[features]
y_train = train[target]

X_val = val[features]
y_val = val[target]

X_test = test[features]
y_test = test[target]

import warnings
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

#instantiate scaler to standardize values 
# apply to train test val 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_val_scaled = scaler.transform(X_val)

type(X_train_scaled)



# X_train_scaled_df = pd.DataFrame(X_train_scaled)
# X_train_scaled_df
# sns.distplot(X_train_scaled_df['cost_of_living_index'])

# X_test_scaled_df = pd.DataFrame(X_test_scaled)
# X_test_scaled_df
# sns.distplot(X_test_scaled_df['cost_of_living_index']);

# loop through all the options of k best from 1 to size of length of columns
for k in range(1, len(X_train.columns)+1):
    print(f'{k} features')
    
    #instantiate selector
    selector = SelectKBest(score_func=f_regression, k=k)
    #Fit train set
    X_train_selected = selector.fit_transform(X_train_scaled, y_train)
    # apply fit to the validation and test 
    X_val_selected = selector.transform(X_val_scaled)
    X_test_selected = selector.transform(X_test_scaled)
    
    #instantiate the model / fit the model 
    model = LinearRegression()
    model.fit(X_train_selected, y_train)
    
    # apply the model to the validation set 
    y_pred = model.predict(X_val_selected)
    mae = mean_absolute_error(y_val, y_pred)
    print(f'MAE:  versus my validation set  {mae:,.4f} \n')



"""# !!!!!  Which features made what difference   !!!!!

1.   ?
2.   ?
"""



"""# DO the XGBoost here now"""









"""# New comprehensive regression approach"""



X_train

X_test

import numpy as np
from sklearn import linear_model
from sklearn import svm

# classifiers = [
#     svm.SVR(),
#     linear_model.SGDRegressor(),
#     linear_model.BayesianRidge(),
#     linear_model.LassoLars(),
#     linear_model.ARDRegression(),
#     linear_model.PassiveAggressiveRegressor(),
#     linear_model.TheilSenRegressor(),
#     linear_model.LinearRegression()]

# trainingData    = np.array([ [2.3, 4.3, 2.5],  [1.3, 5.2, 5.2],  [3.3, 2.9, 0.8],  [3.1, 4.3, 4.0]  ])
# trainingScores  = np.array( [3.4, 7.5, 4.5, 1.6] )
# predictionData  = np.array([ [2.5, 2.4, 2.7],  [2.7, 3.2, 1.2] ])

# for item in classifiers:
#     print(item)
#     clf = item
#     clf.fit(trainingData, trainingScores)
#     print(clf.predict(predictionData),'\n')

classifiers = [
#     svm.SVR(),
#     linear_model.SGDRegressor(),
     linear_model.BayesianRidge(),
#     linear_model.LassoLars(),
#     linear_model.ARDRegression(),
#     linear_model.PassiveAggressiveRegressor(),
#     linear_model.TheilSenRegressor(),
     linear_model.LinearRegression()]

# trainingData    = np.array([ [2.3, 4.3, 2.5],  [1.3, 5.2, 5.2],  [3.3, 2.9, 0.8],  [3.1, 4.3, 4.0]  ])
# trainingScores  = np.array( [3.4, 7.5, 4.5, 1.6] )
# predictionData  = np.array([ [2.5, 2.4, 2.7],  [2.7, 3.2, 1.2] ])

trainingData = X_train_scaled
trainingScores = y_train
predictionData = X_test_scaled

for item in classifiers:
    print(item, '-Classifer \n')
    clf = item
    clf.fit(trainingData, trainingScores)
    print(clf.predict(predictionData),'\n')

classifiers = [
#     svm.SVR(),
#     linear_model.SGDRegressor(),
     linear_model.BayesianRidge(),
#     linear_model.LassoLars(),
#     linear_model.ARDRegression(),
#     linear_model.PassiveAggressiveRegressor(),
#     linear_model.TheilSenRegressor(),
     linear_model.LinearRegression()]

# trainingData    = np.array([ [2.3, 4.3, 2.5],  [1.3, 5.2, 5.2],  [3.3, 2.9, 0.8],  [3.1, 4.3, 4.0]  ])
# trainingScores  = np.array( [3.4, 7.5, 4.5, 1.6] )
# predictionData  = np.array([ [2.5, 2.4, 2.7],  [2.7, 3.2, 1.2] ])

trainingData = X_train_scaled
trainingScores = y_train
predictionData = X_val_scaled

for item in classifiers:
    print(item, '-Classifer \n')
    clf = item
    clf.fit(trainingData, trainingScores)
    print(clf.predict(predictionData),'\n')


    y_pred = clf.predict(predictionData)
    mae = mean_absolute_error(y_val, y_pred) #was y-Pred
    print(f'MAE:  versus my validation set {mae:,.4f} \n')

"""# Now do this with all the regressors."""

classifiers = [
    svm.SVR(),
    linear_model.SGDRegressor(),    
    linear_model.BayesianRidge(),
    linear_model.LassoLars(),
    linear_model.ARDRegression(),
    linear_model.PassiveAggressiveRegressor(),
    linear_model.TheilSenRegressor(),
    linear_model.LinearRegression()]



trainingData = X_train_scaled
trainingScores = y_train
predictionData = X_val_scaled

for item in classifiers:
    print(item, '-Classifer \n')
    clf = item
    clf.fit(trainingData, trainingScores)
    print(clf.predict(predictionData),'\n')


    y_pred = clf.predict(predictionData)
    mae = mean_absolute_error(y_val, y_pred) #was y-Pred
    print(f'MAE:  versus my validation set {mae:,.4f} \n')

"""# Now all regressors with visuals"""

classifiers = [
    svm.SVR(),
    linear_model.SGDRegressor(),    
    linear_model.BayesianRidge(),
    linear_model.LassoLars(),
    linear_model.ARDRegression(),
    linear_model.PassiveAggressiveRegressor(),
    linear_model.TheilSenRegressor(),
    linear_model.LinearRegression()]



trainingData = X_train_scaled
trainingScores = y_train
predictionData = X_val_scaled

for item in classifiers:
    print(item, '-Classifer \n')
    
    clf = item
    clf.fit(trainingData, trainingScores)
    print(clf.predict(predictionData),'\n')


    y_pred = clf.predict(predictionData)
    mae = mean_absolute_error(y_val, y_pred) #was y-Pred
    print(f'MAE:  versus my validation set{mae:,.4f} \n')

    # sns.regplot(x="total_bill", y="tip", data=tips);
    fig, ax = plt.subplots()
    sns.distplot(y_val, hist=False, kde=True, ax=ax, label='Actual')
    sns.distplot(y_pred, hist=False, kde=True, ax=ax, label='Predicted')

    title_string = str(item)
    mae_round = round(mae,4)
    mae_string = str(mae_round)
    sep = '('
    title_string = title_string.split(sep, 1)[0]
    title_acc = str(title_string + " Mae vs Val " + mae_string)
    ax.set_title(title_acc)
    # ax.legend().set_visible(False)

"""# Now everything
## all titles cleaned up
## label added to graph about what MAE accuracy metric was.
"""



y_pred

print('train', X_train_scaled.shape)
print('test',X_test_scaled.shape)
print('val',X_val_scaled.shape)
y_train.shape

"""# !!!  All Pipe below here broken !!!"""



"""# Linear Regression Model"""

# after a baseline can I make a linear regression model that beats guessing.

#1 import estimator from scikit lear 
from sklearn.linear_model import LinearRegression

#2 instantiate the class
model = LinearRegression()

#3 X feature Y target matrix
# this is being done for just 1 feature and 1 target with no split so far 

# X feature y Target split was done above.

train.isnull().sum()

#4fit the model
model.fit(X_train, y_train)

#5apply model to new data 
y_pred = model.predict(X_test)

"""# Sprint Challenge 7 approach

This is currently broken because I have floats trying to describe a float instead of a categorical 

article here explains and it gave me an idea 
https://stackoverflow.com/questions/41925157/logisticregression-unknown-label-type-continuous-using-sklearn-in-python
"""

Stop here

# imports for the next couple steps. Look for more along the way 
import category_encoders as ce
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

pipeline = make_pipeline(
    ce.OneHotEncoder(use_cat_names=True), 
    SimpleImputer(strategy='median'), 
    RandomForestClassifier(random_state=0, n_jobs=-1)
)

# Fit on train, score on val
pipeline.fit(X_train, y_train)
print('Validation Accuracy', pipeline.score(X_val, y_val))

"""# RF REGRESSOR Pipeline"""

pipeline = make_pipeline(
    ce.TargetEncoder(), 
    SimpleImputer(), 
    RandomForestRegressor(random_state=42)
)

param_distributions = {
    'targetencoder__min_samples_leaf': randint(1, 1000), 
    
#     Remove this hyperparameter, because of an issue: 
#     https://github.com/scikit-learn-contrib/categorical-encoding/issues/184
#     'targetencoder__smoothing': uniform(1, 1000), 
    
    'simpleimputer__strategy': ['mean', 'median'], 
    'randomforestregressor__n_estimators': randint(50, 500), 
    'randomforestregressor__max_depth': [5, 10, 15, 20, None], 
    'randomforestregressor__max_features': uniform(0, 1), 
}

# If you're on Colab, decrease n_iter & cv parameters
search = RandomizedSearchCV(
    pipeline, 
    param_distributions=param_distributions, 
    n_iter=15, 
    cv=5, 
    scoring='neg_mean_absolute_error', 
    verbose=10, 
    return_train_score=True, 
    n_jobs=-1
)

search.fit(X_train, y_train);

print('Best hyperparameters', search.best_params_)
print('Cross-validation MAE', -search.best_score_)

"""# Ryan Herr example Project 2"""

# this was the interest rate pickled. 

import category_encoders as ce
from joblib import dump, load
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor

# history = pd.read_csv('LoanStats_securev1_2019Q1.csv.zip', engine='python', skiprows=1, skipfooter=2)

# condition = (history.grade.isin(['A','B','C','D'])) & (history.term==' 36 months')
# history = history[condition]

# history['Interest Rate'] = history['int_rate'].str.strip('%').astype(float)

# history = history.rename(columns=                     
    # {'annual_inc': 'Annual Income', 
    #  'fico_range_high': 'Credit Score', 
    #  'funded_amnt': 'Loan Amount', 
    #  'title': 'Loan Purpose'})

# history['Monthly Debts'] = history['Annual Income'] / 12 * history['dti'] / 100

# columns = ['Annual Income', 
#            'Credit Score', 
#            'Loan Amount', 
#            'Loan Purpose', 
#            'Monthly Debts', 
#            'Interest Rate']

# history = history[columns]
# history = history.dropna()

# X = history.drop(columns='Interest Rate')
# y = history['Interest Rate']
# y_log = np.log1p(y)

# pipeline = make_pipeline(
#     ce.OneHotEncoder(use_cat_names=True), 
#     XGBRegressor(n_estimators=200, n_jobs=-1)
# )

# pipeline.fit(X, y_log)
# dump(pipeline, 'pipeline.joblib')

# history['Annual Income'] = history['Annual Income'].astype(int)
# history['Monthly Debts'] = history['Monthly Debts'].round(2)
# history.to_csv('lending-club.csv', index=False)
