import datetime
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas  # To read data
from sklearn.linear_model import LinearRegression

COVID_Raw = pandas.read_csv("./Data/COVID_Raw.csv")
COVID_Raw['Date'] = pandas.to_datetime(COVID_Raw['Date'])
COVID_Raw = COVID_Raw.set_index('Date')
deltaFig = COVID_Raw.Positive_Raw.plot(title='Kosovo COVID-19 Cases wLin -All Days')
Y = COVID_Raw.Positive_Raw.values.reshape(-1, 1)
X = COVID_Raw.index.map(datetime.datetime.toordinal).values.reshape(-1, 1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions
plt.plot(X, Y_pred, color='red')
plt.show()
