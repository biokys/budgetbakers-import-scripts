# Custom scripts for integration with BudgetBakers app.
This repository serves for community maintenance of scripts that will integrate BudgetBakers app with other 3rd party apps, banks etc. Feel free to implement custom script for your favourite bank and send PR.

Scripts are independent on programming language. It is only required that scripts can run natively on Linux (x64) machine.

You can inspire yourself by looking at [example custom script](https://github.com/biokys/budgetbakers-import-scripts/tree/master/scripts/fioBank) that integrates FIO Bank with our system using their API.


## Script structure

### Input
Required parameters are sent to script using named params as it is common for other scripts (e.g. `--token TOKEN` etc.). Script may define input parameters that it needs for it's run (such as token to API etc.) and retrieves one additional parameter `--lastRunDate` which is, surprisingly, date of last successful script run (this parameter won't be available if script is run for the first time).

### Output

#### Successful
Script should return output as JSON string by printing it to `stdout` and exiting with return code `0`. So far two types of output are supported. One which returns list of records which will be added to Budgetbakers app:
```
	[{
		'amount': 123.45,               # required decimal
		'date': '2015-10-16T15:28:19Z', # ISO8601 with time and zone
		'note': 'Some note',            # optional string
		'currency': 'USD'               # optional ISO4217 currency code
	}]
```
or one which returns closing amount of bank account. In this case one record will be generated in application which will align amount in app with amount returned from script:
```
	{
		'amount': 123.45,               # required decimal
		'currency': 'USD'               # optional ISO4217 currency code
	}
```


#### Error

In case of error script should output info message to `stderr` and return non-zero return code (e.g. `1`).

Info message has following format:
```
	{
		'statusCode': 1,									# <0;127> return code of script
		'fields': {												# (empty) map of fields with error description
			'token': 'Invalid token'				# {fieldName (from params) -> Error description}
		},
		'description': 'Inaccessible API'	# General error descriptions - when error is not in fields
	}
```

So far there are defined following return codes on which BudgetBakers system reacts differently:
 * `ERR_GENERAL = 1` - Something bad happened - developers should be notified (e.g. API is not accessible, unexpected response from server, ...)
 * `ERR_RECOVERABLE = 2` - Failed to retrieve data, try later (e.g. when Bank API can be accessed only once in some time window e.g. once per hour and script is called more often)
 * `ERR_INVALID_PARAM = 20` - Invalid parameter value sent to script - user will be notified (e.g. invalid API token)
