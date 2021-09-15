# migr8t0r
## Purpose
Project is a simple workflow tool to do an export from a Database (MySQL) to Couchbase. It's intended to run 
as a script.

### Requirements
The script leverages the cbimport tool, which it is assumed that it is available on the executing host. 
It's also assumed there is enough storage to export the data from the source database.
Assumed login permissions exist to export data, as welll as Couchbase permissions to drop the target bucket.

#### Process 
1. Create a file system of data and schema (for tracking purposes)
1. Export each table into it's own CSV file
3. Drop the target bucket (if it exists)
2. Create a target bucket (i.e. db on the Couchbase server)
3. Iterate through each csv file and create a collection under the _default scope

No indexes are analyized at this time.
