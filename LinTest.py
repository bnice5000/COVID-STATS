import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt  # To visualize
import pandas  # To read data
from sklearn.linear_model import LinearRegression

tickFormatter = mdates.DateFormatter('%m-%d')

COVID_Raw = pandas.read_csv("./Data/COVID_Raw.csv")
COVID_Raw['Date'] = pandas.to_datetime(COVID_Raw['Date'])
COVID_Raw = COVID_Raw.set_index('Date')

Y = COVID_Raw.Positive_Raw.values.reshape(-1, 1)
X = COVID_Raw.index.map(datetime.datetime.toordinal).values.reshape(-1, 1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions

CPDelta_df = COVID_Raw[['Positive_Raw']]
CPDelta_df['LinReg'] = Y_pred
deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases wLin -All Days', label='Positive Cases', zorder=10)
deltaFig.xaxis.set_major_formatter(tickFormatter)
deltaFig.legend(fontsize='xx-small')
deltaFig.figure.tight_layout()
# plt.plot(X, Y_pred, label='Projected Regression')

plt.show()
