from unipv.db_manager.models import Exam, Schedule, Menu, Calendar
from unipv.db_manager.session_manager import start_session
from unipv.db_manager.result_set import queryset2list
from sqlalchemy import func, and_, or_
from unipv.tools.date import get_day_number, get_month_number
import datetime

def is_unipv_open(week_day):
	days_ita = {'0':'lunedì', '1':'martedì', '2':'mercoledì', '3':'giovedì', '4':'venerdì', '5':'sabato', '6':'domenica'}
	week_day = str(week_day).lower()
	if week_day == 'oggi':
		week_day = days_ita[str(datetime.datetime.today().weekday())]
	if week_day == 'domani':
		week_day = days_ita[str(datetime.datetime.today().weekday()+1)]
	if week_day == 'sabato' or week_day == 'domenica':
		speech_text = "È chiusa!"
	elif week_day in ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì']:
		speech_text = "È aperta!"
	else:
		speech_text = "L'Università di Pavia è aperta dal lunedì al venerdì"
	return speech_text
	
def next_hope(exam):
	months_ita = {'01':'gennaio', '02':'febbraio', '03':'marzo', '04':'aprile', '05':'maggio', '06':'domenica', '07':'luglio', '08':'agosto', '09':'settembre', '10':'ottobre', '11':'novembre', '12':'dicembre'}
	if exam is None:
		return "Mi dispiace, non so rispondere alla tua domanda"
	exam_result = get_next_chance(exam)
	if exam_result is None:
		return "Sei spacciato"
	date = str(exam_result.date)
	year,month,day = date.split("-")
	speech_text = f'Il prossimo esame di {exam_result.course_name} sarà in data {int(day)} {months_ita[month]} {year} in aula {exam_result.room} alle {exam_result.time}'
	return speech_text

def exams_schedule(exam):
	months_ita = {'01':'gennaio', '02':'febbraio', '03':'marzo', '04':'aprile', '05':'maggio', '06':'domenica', '07':'luglio', '08':'agosto', '09':'settembre', '10':'ottobre', '11':'novembre', '12':'dicembre'}
	if exam is None:
		return "Mi dispiace, non so rispondere alla tua domanda"
	exams_results = get_exams_schedule(exam)
	if exams_results is None:
		return "Sei spacciato"
	speech_text =f'I prossimi appelli di {exams_results[0].course_name} si terranno in data:'
	for exam_result in exams_results:
		date = str(exam_result.date)
		year,month,day = date.split("-")
		speech_text = f'{speech_text} {int(day)} {months_ita[month]} {year} in aula {exam_result.room} alle {exam_result.time}... '
	return speech_text

def get_next_chance(exam):
	exam = str(exam).lower()
	date = datetime.datetime.now().date().isoformat()
	session = start_session()
	queryset = session.query(func.min(Exam.date)).filter(and_(Exam.date>date, or_(Exam.short == exam, Exam.course_name == exam )))
	date = queryset2list(queryset)[0][0]
	queryset = session.query(Exam).filter(Exam.date == date)
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)[0]
	else:
		return None	

def get_exams_schedule(exam):
	exam = str(exam).lower()
	date = datetime.datetime.now().date().isoformat()
	session = start_session()
	queryset = session.query(Exam).filter(and_(Exam.date>date, or_(Exam.short == exam, Exam.course_name == exam )))
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)
	else:
		return None	

def schedule(day, year, course=None, time=None):
	days_ita = {'0':'lunedì', '1':'martedì', '2':'mercoledì', '3':'giovedì', '4':'venerdì', '5':'sabato', '6':'domenica'}
	if course is None and day is None and time is None:
		return "Riformula la domanda"
	if course is None and time is None:
		results = get_day_schedule(day,year)
		if results is None:
			return "Sei libero"
		speech_text = f'{day} hai:'
		for course in results:
			speech_text = f'{speech_text} {course.course} alle {course.time} in aula {course.room}... '
	elif day is None and time is None:
		results = get_course_schedule(course,year)
		if results is None:
			return "Il corso non è attivo questo semestre o non è presente nel tuo piano di studi"
		speech_text = f'{results[0].course} si terrà:'
		for course in results:
			speech_text = f'{speech_text} {days_ita[course.day]} alle {course.time} in aula {course.room}... '
	elif time is None:
		result = get_room_and_time_schedule(day, course,year)
		if result is None:
			return "Il corso non si svolgerà nel giorno indicato"
		speech_text = f'{result.course} si terrà in aula {result.room} alle {result.time}'
	else:
		result = get_schedule_from_time(day, time,year)
		if result is None:
			return "Non è presente alcun corso a quell'ora"
		speech_text = f'Alle {result.time} si terrà il corso di {result.course} in aula {result.room}'
	return speech_text
	
def get_day_schedule(day,year):
	day = get_day_number(day)
	if day < 5:
		session = start_session()
		queryset = session.query(Schedule).filter(and_(Schedule.day == day, Schedule.year == year))
		session.close()
		if queryset2list(queryset).__len__() > 0:
			return queryset2list(queryset)
		else:
			return None
	return None	
	
def get_course_schedule(course, year):
	course = str(course).lower()
	session = start_session()
	queryset = session.query(Schedule).filter(and_(Schedule.year == year, or_(Schedule.course == course, Schedule.alias == course)))
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)
	else:
		return None
		
def get_room_and_time_schedule(day, course, year):
	course = str(course).lower()
	session = start_session()
	queryset = session.query(Schedule).filter(and_(Schedule.day == get_day_number(day), Schedule.year == year, or_(Schedule.course == course, Schedule.alias == course)))
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)[0]
	else:
		return None
		
def get_schedule_from_time(day, time, year):
	day = get_day_number(day)
	session = start_session()
	queryset = session.query(Schedule).filter(and_(Schedule.time == time, Schedule.day == day, Schedule.year == year))
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)[0]
	else:
		return None

def menu(day):
	result = get_menu(day)
	if result is None:
		return "La mensa è chiusa nel giorno indicato"
	if not day is None:
		speech_text = f'{day} la mensa offre come primo: {result.first}, per secondo: {result.second} con contorno di: {result.side}'
	else:
		speech_text = f'Oggi la mensa offre come primo: {result.first}, per secondo: {result.second} con contorno di: {result.side}'
	return speech_text

def get_menu(day):
	if day is None:
		day = 'oggi'
	day = get_day_number(day)
	session = start_session()
	queryset = session.query(Menu).filter(Menu.day == day)
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)[0]
	else:
		return None

def calendar_activity(day, month):
	activity = get_calendar_activity(day, month)
	if activity is None:
		return 'Il giorno indicato non è presente nel calendario'
	return f"Nel giorno indicato c'è in programma: {activity}"
		
def get_calendar_activity(day, month):
	date = datetime.datetime.now().date().isoformat()
	year,current_month,_ = date.split("-")
	current_month_number = int(current_month)
	month_number = int(get_month_number(month))
	if current_month_number > month_number:
		year = str(int(year)+1)
	if int(day) < 10:
		day = f'0{day}'
	date = f'{year}-{get_month_number(month)}-{day}'
	session = start_session()
	queryset = session.query(Calendar.activity).filter(and_(Calendar.start <= date, date <= Calendar.end))
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return queryset2list(queryset)[0][0]
	else:
		return None
