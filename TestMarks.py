import datetime
import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt  # To visualize
import pandas  # To read data

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
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -{0} Days'.format(TDays))
    deltaFig.set_xticklabels(ticks, fontsize=8)
    deltaFig.minorticks_off()
    deltaFig.set_xticklabels(ticks, fontsize='xx-small')
    deltaFig.figure.set_size_inches(17, 11)
    deltaFig.legend(['Positive Cases'], fontsize='small', loc='upper left')
    x = deltaFig.patches[-14].get_x() - 0.2
    y = deltaFig.patches[1].get_y() + 0.2
    width = deltaFig.patches[-1].get_x() + deltaFig.patches[-1].get_width() - x
    height = CPDelta_df.Positive_Raw.last(TDays).max() + 2
    rect = patches.Rectangle((x, y), width, height, linewidth=2, linestyle='--', color='red', fill=False, zorder=10)
    # pprint.pprint(dir(rect))
    deltaFig.add_patch(rect)
    deltaFig.figure.tight_layout()
    deltaFig.annotate(
        '{0} Zoom'.format(TDays), xy=(x, height), xycoords='data',
        xytext=(0.8, 0.95), textcoords='axes fraction',
        arrowprops=dict(facecolor='red', shrink=0.05),
        horizontalalignment='right', verticalalignment='top'
    )
    plt.savefig('../../../Desktop/Kosovo COVID-19 Positive Cases -ALL with {0} Box Days Bar.png'.format(TDays), dpi=600)
