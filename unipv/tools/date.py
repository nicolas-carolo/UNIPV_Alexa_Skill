import datetime

def get_day_number(day):
	days_ita = {'lunedì':0, 'martedì':1, 'mercoledì':2, 'giovedì':3, 'venerdì':4, 'sabato':5, 'domenica':6}
	day = str(day).lower()
	if day == 'oggi':
		return datetime.datetime.today().weekday()
	elif day == 'domani':
		day = datetime.datetime.today().weekday()+1
		if day > 6:
			day = 0
		return day
	else:
		return days_ita[day]


def get_month_number(month):
	months_ita = {'gennaio': '01', 'febbraio': '02', 'marzo': '03', 'aprile': '04', 'maggio': '05', 'giugno': '06', 'luglio': '07', 'agosto': '08', 'settembre': '09', 'ottobre': '10', 'novembre': '11', 'dicembre': '12'}
	month = month.lower()
	return months_ita[month]
