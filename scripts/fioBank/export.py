#!/usr/bin/env python3

import sys, requests, json, argparse, datetime, urllib
import dateutil.parser

#
# Script for importing records from FIO Bank. For usage see --help
#

REQUEST_TIMEOUT = 5 # second

API_URL_BASE='https://www.fio.cz/ib_api/rest'
API_URL = '{base}{uri}'.format(base = API_URL_BASE, uri = '/periods/{token}/{fromDate}/{toDate}/transactions.json')

ERR_GENERAL = 1
ERR_EARLY_CALL = 2
ERR_SERVICE_UNAVAILABLE = 3
ERR_INVALID_PARAM = 20

class BadResponse(Exception):
	pass


# Checks whether API is accessible (true/false)
def isApiAccessible():
	try:
		r = requests.get(API_URL_BASE, timeout = REQUEST_TIMEOUT)
		return True
	except requests.exceptions.Timeout as e:
		return False


# Print error JSON to stderr
# - statusCode: <0;126> number defining script return code
# - fields    : {'errorFieldName': 'error description'}
def exitWith(statusCode: int, fields: dict = None, desc: str = None):
	msg = {
		'statusCode': statusCode,
		'fields': fields if fields is not None else {}
	}
	if desc is not None:
		msg['description'] = desc

	print(json.dumps(msg), file = sys.stderr)
	sys.exit(statusCode)


def toDateStr(dt):
	return datetime.datetime.strftime(dt, '%Y-%m-%d')


# Loads records from bank API. Returns either list of records {'note','amount','date'} or throws BadRecord exception if
# failed to retrieve records because of any error
def loadRecords(token, fromDate: str, toDate: str):
	def getNote(transaction):
		return '' if transaction['column16'] is None else transaction['column16']['value']

	def getAmount(transaction):
		return transaction['column1']['value']

	def getDate(transaction):
		#2015-10-16+0200 => 2015-10-16T00:00:00+0200
		d = transaction['column0']['value']
		return d[:10] + 'T00:00:00.000' + d[10:]

	# If dates are same FIO API returns all records for given day (e.g. 2015-10-16) which may lead to duplicate records
	# if script is run more times per day. Therefore records are fetched only for previous days.
	try:
		r = requests.get(API_URL.format(token = urllib.parse.quote_plus(token), fromDate = fromDate, toDate = toDate), timeout = REQUEST_TIMEOUT)
		if r.status_code == requests.codes.ok:
			records = []

			if fromDate == toDate:
				return records
			try:
				rj = r.json()
				transList = rj['accountStatement']['transactionList']

				# Only if there are transactions
				if transList is not None:
					currency = rj['accountStatement']['info']['currency']
					for transaction in transList['transaction']:
						records.append({
							'note': getNote(transaction),
							'amount': getAmount(transaction),
							'date': getDate(transaction),
							'currency': currency
						})

				return records
			except TypeError as e:
				exitWith(ERR_GENERAL)

		elif r.status_code == 409:
			exitWith(ERR_EARLY_CALL, desc = 'Script called multiple times in 30s window which is forbidden by bank API. Try again later.')

		else:
			exitWith(ERR_GENERAL, desc = 'Failed with code = {0} and text = {1}'.format(r.status_code, r.text))

	except requests.exceptions.Timeout as e:
		# FIO API does not respond to invalid token in a nice way - it timeots for 30s and then returns HTTP500
		# Therefore we'll wait some time and then decide that token is invalid
		if isApiAccessible():
			exitWith(ERR_INVALID_PARAM, {'token': 'Invalid token'})
		else:
			exitWith(ERR_SERVICE_UNAVAILABLE, desc = 'Inaccessible API')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Fio Bank custom script for integration with BudgetBakers app')
	parser.add_argument("--token", dest = "token", metavar = "TOKEN",
		help = "Access token for FIO Bank API")
	parser.add_argument("--lastRunDate", dest = "lastRunDate", metavar = "YYYY-MM-DD'T'HH:mm:ss.SSS'Z",
		help = "Date and time of last successful run as ISO8601 UTC format. If script is run for the first time this parameter won't be available")
	parser.add_argument("--initRunDate", dest = "initRunDate", metavar = "YYYY-MM-DD'T'HH:mm:ss.SSS'Z",
		help = "Date and time from when to start to pull records from API. Used mostly for sript first run when 'lastRunDate' is not available yet")

	args = parser.parse_args()

	token = args.token
	lastRunDate = args.lastRunDate
	initRunDate = args.initRunDate

	# FIO API works only with dates (without time). So always align 'to' time to start of today so messages are not duplicated
	fromDate = dateutil.parser.parse(lastRunDate or initRunDate)
	toDate = datetime.datetime.now()

	print(json.dumps(loadRecords(token, toDateStr(fromDate), toDateStr(toDate))))
	sys.exit(0)
