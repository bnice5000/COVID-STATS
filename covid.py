#!/usr/bin/env python
# coding: utf-8

import datetime
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

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
COVID_Raw[['Positive_2D_Mean']] = COVID_Raw[['Positive_Raw']].rolling(2).mean()

COVID_Raw = COVID_Raw.fillna(0)

COVID_Raw['Tested_Positive_Ratio'] = (COVID_Raw['Positive_Raw'] / COVID_Raw['Tested_Raw']) * 100
COVID_Raw['Active_Infections'] = (COVID_Raw['Positive_Cum'] - COVID_Raw['Recovered_Cum'])

COVID_Raw[['Positive_2D_Mean']] = COVID_Raw[['Positive_Raw']].rolling(2).mean()
COVID_Raw[['Positive_3D_Mean']] = COVID_Raw[['Positive_Raw']].rolling(3).mean()

column_order = ['Tested_Raw', 'Tested_Cum', 'Tested_Delta', 'Positive_Raw', 'Positive_Cum', 'Positive_Delta', 'Positive_2D_Mean', 'Positive_3D_Mean', 'Recovered_Raw', 'Recovered_Cum', 'Recovered_Delta', 'Died_Raw', 'Died_Cum', 'Died_Delta', 'Tested_Positive_Ratio', 'Active_Infections']


date = '{:%Y%m%d}'.format(datetime.date.today())
folder = './Graphics/{0}'.format(date)

os.makedirs(folder, 0o755, exist_ok=True)
os.chdir(folder)

# This does not work on bar graphs. See https://github.com/pandas-dev/pandas/issues/1918
tickFormatter = mdates.DateFormatter('%m-%d')

described_data_all = addStats(COVID_Raw).fillna(0)
described_data_l14 = addStats(COVID_Raw.last('14D')).fillna(0)



with pandas.ExcelWriter('{0}_Kosovo_COVID.xlsx'.format(date)) as writer:
    described_data_l14.to_excel(writer, sheet_name='Statistics (L14)')
    described_data_all.to_excel(writer, sheet_name='Statistics (All)')
    COVID_Raw.fillna(0).to_excel(writer, sheet_name='Kosovo Raw Data', columns=column_order)

with plt.xkcd():

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Cases -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases -All Days Plot.png', dpi=900)

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    deltaFig = CPDelta_df.last('14D').plot(title='Kosovo COVID-19 Cases -L14 Days')
    deltaFig.legend(loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases -L14 Days Plot.png', dpi=900)

    CPDelta_df = COVID_Raw[['Tested_Positive_Ratio']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 % Positive -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive to Tested Ratio -All Days.png', dpi=900)

    CPDelta_df = COVID_Raw[['Tested_Positive_Ratio']].last('14D')
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 % Positive -L14 Days')
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive to Tested Ratio -L14.png', dpi=900)

    CPDelta_df = COVID_Raw[['Active_Infections']]
    deltaFig = CPDelta_df.plot(title='Kosovo COVID-19 Active Infections -All Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections -ALL.png', dpi=900)

    CPDelta_df = COVID_Raw[['Active_Infections']].last('14D')
    deltaFig = CPDelta_df.plot(title='Kosovo Active Infections -L14 Days')
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections -L14.png', dpi=900)

    CPDelta_df = COVID_Raw[['Active_Infections', 'Positive_Raw']]
    deltaFig = CPDelta_df.plot(title='Kosovo Active Infections vs Positive Ratio -ALL Days')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.legend(fontsize='xx-small', loc='upper left')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Active Infections vs Positive -ALL.png', dpi=900)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw', 'Died_Raw']]
    deltaFig = CPDelta_df.last('14D').plot(title='Kosovo COVID-19 Cases Overall -Last 14 Days')
    deltaFig.legend(fontsize='x-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -Last 14 Days Plot.png', dpi=900)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw', 'Died_Raw']]
    deltaFig = CPDelta_df.last('7D').plot(title='Kosovo COVID-19 Cases Overall -Last 7 Days')
    deltaFig.legend(fontsize='x-small')
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -Last 7 Days Plot.png', dpi=900)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw']].last('14D')
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -Last 14 Days')
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive & Tested Cases -Last 14 Days Bar.png', dpi=900)

    CPDelta_df = COVID_Raw[['Positive_Raw']].last('14D')
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -Last 14 Days')
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive Cases -Last 14 Days Bar.png', dpi=900)

    CPDelta_df = COVID_Raw[['Positive_Raw']]
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -All Days')
    deltaFig.set_xticklabels(ticks, fontsize=8)
    deltaFig.minorticks_off()
    deltaFig.figure.set_size_inches(11, 8.5)
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Positive Cases -ALL Days Bar.png', dpi=600)

    CPDelta_df = COVID_Raw[['Tested_Raw', 'Positive_Raw', 'Tested_Positive_Ratio']].last('14D')
    ticks = CPDelta_df.index.strftime('%m-%d').values
    deltaFig = CPDelta_df.plot(kind='bar', title='Kosovo COVID-19 Cases -Last 14 Days', logy=True)
    deltaFig.set_xticklabels(ticks)
    deltaFig.set_yticklabels(['0', '0', '1', '10', '100', '1000'])
    deltaFig.legend(fontsize='xx-small', loc='best')
    deltaFig.figure.set_size_inches(11, 8.5)
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -Last 14 Days Bar.png', dpi=600)

    CPDelta_df = COVID_Raw[['Positive_Raw', 'Recovered_Raw', 'Died_Raw']]
    ticks = CPDelta_df.last('14D').index.strftime('%m-%d').values
    deltaFig = CPDelta_df.last('14D').plot.bar(stacked=True, title='Kosovo COVID-19 Cases Overall -Last 14 Days')
    deltaFig.legend(fontsize='xx-small')
    deltaFig.set_xticklabels(ticks)
    deltaFig.minorticks_off()
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -L14 Days Stacked Bar.png', dpi=900)

    CPDelta_df = COVID_Raw[['Positive_Raw', 'Recovered_Raw', 'Died_Raw']]
    deltaFig = CPDelta_df.last('14D').plot.area(stacked=True, title='Kosovo COVID-19 Cases Overall -Last 14 Days')
    deltaFig.legend(fontsize='xx-small')
    deltaFig.xaxis.set_major_formatter(tickFormatter)
    deltaFig.figure.tight_layout()
    deltaFig.figure.savefig('Kosovo COVID-19 Cases Overall -L14 Days Area.png', dpi=900)
