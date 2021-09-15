# migr8t0r
## Purpose
Project is a simple workflow tool to do an export from a Database (MySQL) to Couchbase. It's intended to run 
as a script.

### Requirements
The script leverages the cbimport tool, which it is assumed that it is available on the executing host. 
It's also assumed there is enough storage to export the data from the source database.
Assumed login permissions exist to export data, as welll as Couchbase permissions to drop the target bucket.

##### Blah Blah Blah I want to go now
Assuming all components required are installed, you can run the init.sh script. You will most likely need to make it executable 'chmod +x ./init.sh' Then just run init.sh. 

During testing found that it takes a while for the mysql environment to get setup. So there's a 5 minute delay to address that. If it fails you can run python3 main.py to kick off the migration script.

#### Process 
1. Create a file system of data and schema (for tracking purposes)
2. Export each table into it's own CSV file
3. Drop the target bucket (if it exists)
4. Create a target bucket (i.e. db on the Couchbase server)
5. Iterate through each csv file and create a collection under the _default scope

No indexes are analyized at this time.


