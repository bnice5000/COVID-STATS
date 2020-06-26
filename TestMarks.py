import datetime
import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt  # To visualize
import pandas  # To read data
from sklearn.linear_model import LinearRegression

import pprint

tickFormatter = mdates.DateFormatter('%m-%d')

COVID_Raw = pandas.read_csv("./Data/COVID_Raw.csv")
COVID_Raw['Date'] = pandas.to_datetime(COVID_Raw['Date'])
COVID_Raw = COVID_Raw.set_index('Date')
COVID_Raw[['Tested_Cum']] = COVID_Raw[['Tested_Raw']].cumsum()
COVID_Raw[['Positive_Cum']] = COVID_Raw[['Positive_Raw']].cumsum()
COVID_Raw[['Recovered_Cum']] = COVID_Raw[['Recovered_Raw']].cumsum()
COVID_Raw[['Died_Cum']] = COVID_Raw[['Died_Raw']].cumsum()
COVID_Raw['Tested_Positive_Ratio'] = (COVID_Raw['Positive_Raw'] / COVID_Raw['Tested_Raw']) * 100
COVID_Raw['Active_Infections'] = (COVID_Raw['Positive_Cum'] - (COVID_Raw['Recovered_Cum'] + COVID_Raw['Died_Cum']))

with plt.xkcd():

    TDays = '14D'

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -All Days')
    deltaFig.set_xticklabels(ticks, fontsize=8)
    deltaFig.minorticks_off()
    deltaFig.set_xticklabels(ticks, fontsize='xx-small')
    deltaFig.figure.set_size_inches(17, 11)
    deltaFig.legend(['Positive Cases'], fontsize='small', loc='upper left')
    pprint.pprint(dir(deltaFig.patches))
    # start = plt.bar[-7]
    # end = plt.bar[-1]
    # width = 25  # end - start
    # height = 25  # CPDelta_df.Positive_Raw.max()
    # rect = patches.Rectangle((start, end), width, height, linewidth=1, color='red', fill=False)
    # deltaFig.add_patch(rect)
    deltaFig.figure.tight_layout()

    # plt.savefig('../../../Desktop/Kosovo COVID-19 Positive Cases -ALL Days Bar.png'.format(TDays), dpi=600)
