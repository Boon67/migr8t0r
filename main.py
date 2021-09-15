#!/usr/bin/env python
import mysql.connector
import csv
import os
import shutil
import couch
from pathlib import Path

SRC_HOST='localhost'
SRC_USERNAME='root'
SRC_PASSWORD='password'
SRC_DBNAME='sportsdb'

DEST_HOST='localhost'
DEST_USERNAME='Administrator'
DEST_PASSWORD='password'
DEST_DBNAME='sportsdb'

db_admin=couch.Admin()
datadir = 'db_data'
schemadir = 'db_schema'

###Helper for getting file paths based upon where the script is instantiated
def absoluteFilePaths(directory):
  for dirpath,_,filenames in os.walk(directory):
    for f in filenames:
      yield os.path.abspath(os.path.join(dirpath, f))

#Setup the file system
if os.path.exists(schemadir):
    shutil.rmtree(schemadir)
os.makedirs(schemadir)

db_admin.createBucket(DEST_USERNAME, DEST_PASSWORD, DEST_HOST, DEST_DBNAME, True)

print ('Starting Export....')
db = mysql.connector.connect(
  host=SRC_HOST,
  user=SRC_USERNAME,
  password=SRC_PASSWORD,
  db=SRC_DBNAME
)
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

cur.execute("SHOW TABLES")
tables = []
for row in cur.fetchall():
    tables.append(row[0])

for t in tables:    
    # CREATE TABLES STATEMENTS
    cur.execute("SHOW CREATE TABLE `{}`".format(t))
    temptxt = '{}.txt'.format(t)

    with open(schemadir + '/' + temptxt, 'w', newline='') as txtfile:
        txtfile.write(cur.fetchone()[1])                   # ONE RECORD FETCH
    txtfile.close()

    # SELECT STATEMENTS
    cur.execute("SELECT * FROM `{}`".format(t))
    tempcsv = '{}.csv'.format(t)

    with open(datadir + '/' + tempcsv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])   # COLUMN HEADERS
        for row in cur.fetchall():        
            writer.writerow(row)
    csvfile.close()

cur.close()
db.close()

print('Export Complete.')


### Couchbase Magic here. Requires cbimport to be on the path of the environment where this is executing
print ('Starting Import....')
fileList=absoluteFilePaths(datadir)
for filename in fileList:
  print(filename)
  with open(filename) as f:
      lines = f.read() ##Assume the sample file has 3 lines
      idField = lines.split(',', 1)[0]
  #Appears cbImport does not create the collections when importing
  db_admin.createCollection(DEST_USERNAME, DEST_PASSWORD, DEST_HOST, DEST_DBNAME, '_default', Path(filename).stem)
  cmd='cbimport csv -c couchbase://' + DEST_HOST + ' -u ' + DEST_USERNAME + ' -p ' + DEST_PASSWORD + ' -b ' + DEST_DBNAME + '  -d file://' + filename  + ' -g key::%' + idField + '% -t 4 --scope-collection-exp _default.'+ Path(filename).stem
  print(cmd)
  os.system(cmd)
print ('Import Complete....')