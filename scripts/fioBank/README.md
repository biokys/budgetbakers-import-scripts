# FIO Bank export script
This script serves for exporting payment records from FIO Bank API. For script usage see `--help`.

## Preparing environment
Script requires `python3` environment with some packages installed (see `requirements.txt`). It's good practice to create local environment just for this script so other scripts are not affected about different package versions etc. You can create environment by running `./prepareEnv.sh` and then activate it using `source env/bin/activate`.

## FIO Bank API
FIO bank allows to call their API only once per 30s window. If API is called more times the HTTP error 409 is returned. API also supports only date (not time) interval for limiting search results. When `fromDate == toDate` all records for given day are returned. This may lead to duplicate records in BudgetBakers database therefore this script does not return any records if `fromDate == toDate`. This "feature" will cause that todays records will appear in system only tomorrow.

FIO Bank API has no proper way for detecting invalid API token. The behavior is that after 30s timeout server responds with HTTP 500 error. Custom script solves this issue by waiting `REQUEST_TIMEOUT` seconds and then checking whether root URL is accessible. 
