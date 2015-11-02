# FIO Bank export script
This script serves for exporting payment records from FIO Bank API. For script usage see `--help`.

## Usage
Script takes two these params:

 * `--token` -- personal token for accessing FIO Bank API.
 * `--initRunDate` -- from when to start fetching bank records
 * `--lastRunDate` -- date and time of last record fetched using this script - hint fo retching only new records

 ## Script result
 Script returns following error codes in case of any error as described in main README:

  * `ERR_EARLY_CALL` -- if API is called with same API key more times in 30s interval
  * `ERR_SERVICE_UNAVAILABLE` -- if API is not accessible at the moment
  * `ERR_INVALID_PARAM` -- if any parameter sent to script is malformed (e.g. wrong API key)
  * `ERR_GENERAL` -- if script got unknown response from server of failed to parse response body

 In case of success script acts as described in main README


## Caveats

### Preparing environment
Script requires `python3` environment with some packages installed (see `requirements.txt`). It's good practice to create local environment just for this script so other scripts are not affected about different package versions etc. You can create environment by running `./prepareEnv.sh` and then activate it using `source env/bin/activate`.

### FIO Bank API
FIO bank allows to call their API only once per 30s window. If API is called more times the HTTP error 409 is returned. API also supports only date (not time) interval for limiting search results. When `fromDate == toDate` all records for given day are returned. This may lead to duplicate records in BudgetBakers database therefore this script does not return any records if `fromDate == toDate`. This "feature" will cause that todays records will appear in system only tomorrow.

FIO Bank API has no proper way for detecting invalid API token. The behavior is that after 30s timeout server responds with HTTP 500 error. Custom script solves this issue by waiting `REQUEST_TIMEOUT` seconds and then checking whether root URL is accessible.
