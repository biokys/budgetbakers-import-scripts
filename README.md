# Custom scripts for integration with BudgetBakers app.
This repository serves for community maintenance of scripts that will integrate BudgetBakers app with other 3rd party apps, banks etc. Feel free to implement custom script for your favourite bank and send PR.

Scripts are independent on programming language. It is only required that scripts can run natively on Linux (x64) machine.

You can inspire yourself by looking at [example custom script](https://github.com/biokys/budgetbakers-import-scripts/tree/master/scripts/fioBank) that integrates FIO Bank with our system using their API.


## Script structure

### Input
Required parameters are sent to script using named params as it is common for other scripts (e.g. `--token TOKEN` etc.). Script may define input parameters that it needs for it's run (such as token to API etc.) and retrieves one additional parameter `--lastRunDate` which is, surprisingly, date of last successful script run (this parameter won't be available if script is run for the first time).

### Output
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

In case of error script should output info message to `stderr` and return non-zero return code (e.g. `1`).

