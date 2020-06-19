import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt  # To visualize
import pandas  # To read data
from sklearn.linear_model import LinearRegression

tickFormatter = mdates.DateFormatter('%m-%d')

COVID_Raw = pandas.read_csv("./Data/COVID_Raw.csv")
COVID_Raw['Date'] = pandas.to_datetime(COVID_Raw['Date'])
COVID_Raw = COVID_Raw.set_index('Date')
COVID_Raw[['Tested_Cum']] = COVID_Raw[['Tested_Raw']].cumsum()
COVID_Raw[['Positive_Cum']] = COVID_Raw[['Positive_Raw']].cumsum()
COVID_Raw[['Recovered_Cum']] = COVID_Raw[['Recovered_Raw']].cumsum()
COVID_Raw[['Died_Cum']] = COVID_Raw[['Died_Raw']].cumsum()
COVID_Raw['Active_Infections'] = (COVID_Raw['Positive_Cum'] - (COVID_Raw['Recovered_Cum'] + COVID_Raw['Died_Cum']))

with plt.xkcd():

    deltaFig = COVID_Raw.Active_Infections.plot(title='Kosovo COVID-19 Active Infections wLin -All Days', label='Positive Cases', zorder=10)
    Y = COVID_Raw.Active_Infections.values.reshape(-1, 1)
    X = COVID_Raw.index.map(datetime.datetime.toordinal).values.reshape(-1, 1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    CPDelta_df = COVID_Raw[['Active_Infections']]
    CPDelta_df.insert(0, 'LinReg', Y_pred, True)
    CPDelta_df.insert(0, 'Mean_Active', COVID_Raw['Active_Infections'].mean(), True)
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Active Infections -All Days', zorder=10)
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(['Mean Active Infections', 'Projected Regression', 'Active Infections'], fontsize='small')
    deltaFig.figure.tight_layout()

    plt.savefig('../../../Desktop/Kosovo COVID-19 Active wLinRegandMean -All Days Plot.png', dpi=600)
