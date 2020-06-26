#!/usr/bin/env python
# coding: utf-8

import datetime
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

import pandas


def addStats(df):
    stats = df.describe(include='all')
    stats.loc['var'] = df.var().tolist()
    stats.loc['skew'] = df.skew().tolist()
    stats.loc['kurt'] = df.kurtosis().tolist()
    stats.loc['mad'] = df.mad().tolist()

    return stats


pandas.set_option('use_inf_as_na', True)

COVID_Raw = pandas.read_csv("./Data/COVID_Raw.csv")
COVID_Raw['Date'] = pandas.to_datetime(COVID_Raw['Date'])
COVID_Raw = COVID_Raw.set_index('Date')
COVID_Raw[['Tested_Cum']] = COVID_Raw[['Tested_Raw']].cumsum()
COVID_Raw[['Tested_Delta']] = COVID_Raw[['Tested_Raw']].pct_change()
COVID_Raw[['Positive_Cum']] = COVID_Raw[['Positive_Raw']].cumsum()
COVID_Raw[['Positive_Delta']] = COVID_Raw[['Positive_Raw']].pct_change()
COVID_Raw[['Recovered_Cum']] = COVID_Raw[['Recovered_Raw']].cumsum()
COVID_Raw[['Recovered_Delta']] = COVID_Raw[['Recovered_Raw']].pct_change()
COVID_Raw[['Died_Cum']] = COVID_Raw[['Died_Raw']].cumsum()
COVID_Raw[['Died_Delta']] = COVID_Raw[['Died_Raw']].pct_change()
COVID_Raw[['Hospitalizations_Cum']] = COVID_Raw[['Hospitalizations_Raw']].cumsum()
COVID_Raw[['Hospitalizations_Delta']] = COVID_Raw[['Hospitalizations_Raw']].pct_change()

COVID_Raw['Tested_Positive_Ratio'] = (COVID_Raw['Positive_Raw'] / COVID_Raw['Tested_Raw']) * 100
COVID_Raw['Active_Infections'] = (COVID_Raw['Positive_Cum'] - (COVID_Raw['Recovered_Cum'] + COVID_Raw['Died_Cum']))

COVID_Raw[['Positive_2D_Mean']] = COVID_Raw[['Positive_Raw']].rolling(2).mean()
COVID_Raw[['Positive_3D_Mean']] = COVID_Raw[['Positive_Raw']].rolling(3).mean()

COVID_Raw = COVID_Raw.fillna(0)

column_order = ['Tested_Raw', 'Tested_Cum', 'Tested_Delta', 'Positive_Raw', 'Positive_Cum', 'Positive_Delta', 'Positive_2D_Mean', 'Positive_3D_Mean', 'Recovered_Raw', 'Recovered_Cum', 'Recovered_Delta', 'Died_Raw', 'Died_Cum', 'Died_Delta', 'Hospitalizations_Raw', 'Hospitalizations_Cum', 'Hospitalizations_Delta', 'Tested_Positive_Ratio', 'Active_Infections']


date = '{:%Y%m%d}'.format(datetime.date.today())
folder = './Graphics/{0}'.format(date)
TDays = '14D'

os.makedirs(folder, 0o755, exist_ok=True)
os.chdir(folder)

# This does not work on bar graphs. See https://github.com/pandas-dev/pandas/issues/1918
tickFormatter = mdates.DateFormatter('%m-%d')

described_data_all = addStats(COVID_Raw).fillna(0)
described_data_L14 = addStats(COVID_Raw.last(TDays)).fillna(0)

with pandas.ExcelWriter('{0}_Kosovo_COVID.xlsx'.format(date)) as writer:
    described_data_L14.to_excel(writer, sheet_name='Statistics (L14D)')
    described_data_all.to_excel(writer, sheet_name='Statistics (All)')
    COVID_Raw.fillna(0).to_excel(writer, sheet_name='Kosovo Raw Data', columns=column_order)

with plt.xkcd():

    deltaFig = COVID_Raw.Tested_Positive_Ratio.plot(title='Kosovo COVID-19 % Positive Tests -L{0} Days'.format(TDays), label='Positive Cases', zorder=10)
    Y = COVID_Raw.Tested_Positive_Ratio.last(TDays).values.reshape(-1, 1)
    X = COVID_Raw.last(TDays).index.map(datetime.datetime.toordinal).values.reshape(-1, 1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    CPDelta_df = COVID_Raw[['Tested_Positive_Ratio']].last(TDays)
    CPDelta_df.insert(0, 'LinReg', Y_pred, True)
    CPDelta_df.insert(0, '5%_Dip_Strong', 5, True)
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Active Infections -{0}'.format(TDays), zorder=10)
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(['5% Diplomacy Strong Measure', 'Projected Regression', '% Positive Tests'], fontsize='small')
    deltaFig.figure.tight_layout()

    deltaFig = COVID_Raw.Positive_Raw.plot(title='Kosovo COVID-19 Cases wLin -All Days', label='Positive Cases', zorder=10)
    Y = COVID_Raw.Positive_Raw.values.reshape(-1, 1)
    X = COVID_Raw.index.map(datetime.datetime.toordinal).values.reshape(-1, 1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    CPDelta_df = COVID_Raw[['Positive_Raw']]
    CPDelta_df.insert(0, 'LinReg', Y_pred, True)
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases wLin -All Days', zorder=10)
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(['Projected Regression', 'Positive Cases'], fontsize='xx-small')
    deltaFig.figure.tight_layout()
    plt.savefig('Kosovo COVID-19 Raw wLinReg -All Days Plot.png', dpi=600)

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
    plt.savefig('Kosovo COVID-19 Raw wLinRegandMean -All Days Plot.png', dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases -All Days Plot.png', dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    deltaFig = CPDelta_df.last(TDays).plot(title='Kosovo COVID-19 Cases -{0} Days'.format(TDays))
    deltaFig.legend(loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases -{0} Days Plot.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Hospitalizations_Raw']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Hospitalizations -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Hospitalizations -All Days Plot.png', dpi=600)

    CPDelta_df = COVID_Raw[['Positive_2D_Mean']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases 2D Mean -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases 2D Mean -All Days Plot.png', dpi=600)
    plt.close('all')

    CPDelta_df = COVID_Raw[['Hospitalizations_Raw']]
    deltaFig = CPDelta_df.last(TDays).plot(title='Kosovo COVID-19 Hospitalizations -{0} Days'.format(TDays))
    deltaFig.legend(loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Hospitalizations -{0} Days Plot.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Positive_2D_Mean']]
    deltaFig = CPDelta_df.last(TDays).plot(title='Kosovo COVID-19 Positive 2D Mean -{0} Days'.format(TDays))
    deltaFig.legend(loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive 2D Mean -{0} Days Plot.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Positive_Ratio']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 % Positive -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive to Tested Ratio -All Days.png', dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Positive_Ratio']].last(TDays)
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 % Positive -{0} Days'.format(TDays))
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive to Tested Ratio -{0}.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Active_Infections']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Active Infections -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections -ALL.png', dpi=600)
    plt.close('all')

    CPDelta_df = COVID_Raw[['Active_Infections']].last(TDays)
    deltaFig = CPDelta_df.plot(title='Kosovo Active Infections -{0} Days'.format(TDays))
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections -{0}.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Active_Infections', 'Positive_Raw']]
    deltaFig = CPDelta_df.plot(title='Kosovo Active Infections vs Positive Ratio -ALL Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections vs Positive -ALL.png', dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw', 'Died_Raw', 'Hospitalizations_Raw']]
    deltaFig = CPDelta_df.last(TDays).plot(title='Kosovo COVID-19 Cases Overall -{0}'.format(TDays))
    deltaFig.legend(fontsize='x-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -{0} Plot.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw']].last(TDays)
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -{0}'.format(TDays))
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive & Tested Cases -{0} Bar.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw']].last(TDays)
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -{0}'.format(TDays))
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive Cases -{0} Bar.png'.format(TDays), dpi=600)
    plt.close('all)')

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -All Days')
    deltaFig.set_xticklabels(ticks, fontsize=8)
    deltaFig.minorticks_off()
    deltaFig.set_xticklabels(ticks, fontsize='xx-small')
    deltaFig.figure.set_size_inches(17, 11)
    deltaFig.legend(['Positive Cases'], fontsize='small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive Cases -ALL Days Bar.png', dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw', 'Tested_Positive_Ratio']].last(TDays)
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -{0}'.format(TDays), logy=True)
    deltaFig.set_xticklabels(ticks)
    deltaFig.set_yticklabels(['0', '0', '1', '10', '100', '1000'])
    deltaFig.legend(fontsize='xx-small', loc='best')
    deltaFig.figure.set_size_inches(17, 11)
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -{0} Bar.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw', 'Recovered_Raw', 'Died_Raw']]
    ticks = CPDelta_df.last(TDays).index.strftime('%m-%d').values
    deltaFig = CPDelta_df.last(TDays).plot.bar(stacked=True, title='Kosovo COVID-19 Cases Overall -{0}'.format(TDays))
    deltaFig.legend(fontsize='xx-small')
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -{0} Days Stacked Bar.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw', 'Recovered_Raw', 'Died_Raw']]
    deltaFig = CPDelta_df.last(TDays).plot.area(stacked=True, title='Kosovo COVID-19 Cases Overall -{0}'.format(TDays))
    deltaFig.legend(fontsize='xx-small')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -{0} Days Area.png'.format(TDays), dpi=600)

    CPDelta_df = COVID_Raw[['Active_Infections', 'Recovered_Cum', 'Died_Cum']]
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot.bar(stacked=True, title='Kosovo COVID-19 POL Chart Overall')
    deltaFig.legend(fontsize='xx-small')
    deltaFig.set_xticklabels(ticks, fontsize='xx-small')
    deltaFig.figure.set_size_inches(17, 11)
    deltaFig.legend(['Active Infection', 'Cumulative Recovered', 'Cumulative Deceased'], fontsize='small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall POL_Cum Stacked Bar.png', dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    CPDelta_df.insert(0, 'Mean_Positive', COVID_Raw['Positive_Raw'].mean(), True)
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases wMean -All Days Plot.png', dpi=600)
    plt.close('all')
