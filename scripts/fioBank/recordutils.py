
#
# Note prefixes for record categorization
#
# Buy record
PREF_BUY = 'Nákup: '
# Withdrawal record
PREF_WTH = 'Výběr z bankomatu: '

#
# Record flags
#
FLAG_WITHDRAWAL = 'WITHDRAWAL'


def isBuyRecNote(note):
	'''
	Check if record is of 'buy' type
	'''
	return note.startswith(PREF_BUY)


def isWithdrawalRecNote(note):
	'''
	Check if record is of 'withdraval' type
	'''
	return note.startswith(PREF_WTH)


def getNote(transaction):
	'''
	Get record note
	'''
	return '' if transaction['column16'] is None else transaction['column16']['value']


def stripNoteInfo(note: str):
	'''
	Strip useless info from record note
	'''
	if isBuyRecNote(note):
		note = note[len(PREF_BUY):]
		note = note.split(', dne')[0]
	elif isWithdrawalRecNote(note):
		note = note[len(PREF_WTH):]
		note = note.split(', dne')[0]

	return note


def getSanitizedNote(transaction):
	'''
	Get only required info from note, transform cases etc.
	'''
	def toTitleCase(s: str):
		return s if len(s) < 3 or any([ x.islower() for x in s ]) else s.title()

	note = stripNoteInfo(getNote(transaction))
	note = " ".join([ toTitleCase(w) for w in note.split() ])

	return note


def getAmount(transaction):
	return transaction['column1']['value']


def getDate(transaction):
	'''
	Get transaction date
	'''
	#2015-10-16+0200 => 2015-10-16T00:00:00+0200
	d = transaction['column0']['value']
	return d[:10] + 'T00:00:00.000' + d[10:]


def getRecordFlags(transaction):
	'''
	Record flags e.g. is withdraval etc.
	'''
	flags = []
	note = getNote(transaction)

	if isWithdrawalRecNote(note):
		flags.append(FLAG_WITHDRAWAL)

	return flags
