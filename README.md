# COVID-STATS

This is Open Source data about COVID-19 cases in Kosovo. The scripts used in this program should be run as follows:
`ipython covid.py`

If you would like to run it using the invoke system, the following command will kick off the process:
`invoke build push --tag release`

***I have removed all of the MacOS specific code. This should work on any computer now. On Windows, I would highly recomoend using Scientific Python instead of trying to roll your own.***

# Defining Terms

## Date
`Date` is an ISO 8601 formatted date that represents the date that the data was reported

## Tested
`Tested_Raw` is the reported data of how many people were tested using the WHO standard testing methodology.
`Tested_Cum` is the cumulative is a running total of all of the values.
`Tested_Delta` calculates percentage change between the current and a prior element.

## Positive
`Positive_Raw` is the reported data of how many people who had a positive test result using the WHO standard testing methodology.
`Positive_Cum` is the cumulative is a running total of all of the values.
`Positive_Delta` calculates percentage change between the current and a prior element.

## Recovered
`Recovered_Raw` is the reported data of how many people had two negative tests 24 hours apart using the WHO standard testing methodology.
`Recovered_Cum` is the cumulative is a running total of all of the values.
`Recovered_Delta` calculates percentage change between the current and a prior element.

## Tested
`Died_Raw` is the reported data of how many people who had a cessation of life functions due to COVID-19.
`Died_Cum` is the cumulative is a running total of all of the values.
`Died_Delta` calculates percentage change between the current and a prior element.

## Calculated Elements
`Tested_Positive_Ratio` is  `(Positive_Raw / Tested_Raw) * 100`
`Active_Infections` is  `Recovered_Cum - Positive_Cum`

# Just the Facts

If you would just like to see the results of the scripts, I make a [release](https://github.com/bnice5000/COVID-STATS/releases) almost every weekday.

# Note about the data

We have been entering the data daily. At some point before 2020-05-19 the data was retrospectively modified. It an effort to maintain transparency, we have the old data file, the new data file, along with a diff file of the changes. If the data diverges again we will use the same process to maintain transparency.
