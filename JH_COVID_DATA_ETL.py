import datetime
import glob
import os
import pandas
import requests
import sqlite3
import shutil
import zipfile

# Set Variables
PATH = './Output/{0}'.format(datetime.datetime.now().strftime('%Y%m%d'))
EXT = '*.csv'
ZIP = 'jhdata.zip'
SQLF = 'jhdata-{0}.sqlite'.format(datetime.datetime.now().strftime("%Y%m%d"))
dfs = {}

# Create dir if does not exist
if not os.path.exists(PATH):
    os.makedirs(PATH)

# create DB
conn = sqlite3.connect('{0}/{1}'.format(PATH, SQLF))

# Download JH date zip from Github
res = requests.get('https://github.com/CSSEGISandData/COVID-19/archive/master.zip')
res.raise_for_status()
jh_zip_file = open('{0}/{1}'.format(PATH, ZIP), 'wb')
for chunk in res.iter_content(100000):
    jh_zip_file.write(chunk)
jh_zip_file.close()

# unzip file
with zipfile.ZipFile('{0}/{1}'.format(PATH, ZIP), 'r') as zip_ref:
    zip_ref.extractall(PATH)

# Get list of CSV files
file_loc = [file for path, subdir, files in os.walk(PATH) for file in glob.glob(os.path.join(path, EXT))]

# Create dictionary {key:CSV file name, value:CSV Data as DF}
for file in file_loc:
    key = os.path.splitext(os.path.basename(file))[0]
    value = pandas.read_csv(file)
    dfs[key] = value

# Write the DF to the DB
for title, df in dfs.items():
    df.to_sql(title, conn, if_exists='replace', index=False)

# Dump the DB to an SQL file format
with open('{0}/{1}.dump.sql'.format(PATH, SQLF), 'w') as dump:
    for line in conn.iterdump():
        dump.write('{0}\n'.format(line))

# Close the DB
conn.close()

# Delete the zip file
if os.path.isfile('{0}/{1}'.format(PATH, ZIP)):
    os.remove('{0}/{1}'.format(PATH, ZIP))

# Delete the CSV files
try:
    shutil.rmtree('{0}/COVID-19-master'.format(PATH))
except OSError as e:
    print('Error: {0} - {1}.'.format(e.filename, e.strerror))
