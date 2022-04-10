# cs32-final-project
Final project for Harvard's CS32

## Group members
1. Bozen Peng
2. Innocent Munai

## Brief introduction
Bozen and I are planning to provide a user interface (maybe a Python-based web application) for users to input a dataset (in .csv) that is prepared for Classification in Machine Learning. 

- We will provide the users with some help to preprocess their dataset. 
- We then train the preprocessed datasets by different algorithm, such as linear regression, Support Vector Regression, Decision Tree Regression, Random Forest Regression, and so on. 
- We allow the user to customize their preferable parameters for the trainings before implementaing those. 
- After we finish the trainings by different algorithms, we test these by test set and calculate confusion matrices for each model trained. 
- We present the models as well as the accuracy of each to the user so that they can choose to use those models based on the performance.

## The libries needed
numpy, scikit-learn, pandas, glob, os, etc

## Some sample codes
**(1)** we will provide the users with some help to preprocess their dataset:

For instance, label normalization:
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
A = LabelEncoder()
```

Another example is to encode numbers into categorization:
```python
import pandas as pd
EncodedNumber = pd.cut(session_rate['Number'], bins = [0, 10, 100, 1000],
include_lowest=True, labels=[0, 1, 2])
```

**(2)** we need to do some preprocessing steps before starting the training. 

For example, extract independent and dependent variables, X and y
```python
import numpy as np
X = session_rate.iloc[:, 0:3].values
y = session_rate.iloc[:, 3].values
y = np.array(y)
```

Also, splitting train set and test set:
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
```

Another example is to perform standardization on independent variable
```python
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) X_test = sc_X.transform(X_test)
```

 
**(3)** we need to train the set with different algorithm. 

One example is Random Forest
```python
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 50, criterion = 'entropy', n_jobs = 8)
classifier.fit(X_train, y_train)
```

**(4)** We also need to calculate confusion matrix to different models, e.g.:
```python
from sklearn.metrics import confusion_matrix 
cm_RF = confusion_matrix(y_test, y_pred)
```

An example of outputted confusion matrix for one model:
- <img width="501" alt="Snipaste_2022-04-10_16-36-48" src="https://user-images.githubusercontent.com/42286547/162638796-9ac3257b-9702-4b24-bc09-56bd5f9a80d6.png">

