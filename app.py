from flask import Flask
from flask_ask import Ask, statement, question
from unipv.skills.professor import get_professor_email, get_professor_courses, get_professors_that_take_a_course,\
    get_professor_office, get_professor_lab, get_professor_office_hour
from unipv.skills.activity import is_unipv_open, next_hope, schedule, menu, exams_schedule,calendar_activity
from unipv.db_manager.users_manager import check_active_user, add_user_db, change_user_db, remove_user, change_year

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def home():
    return 'Hi! I am UNIPV'

@ask.intent('isUNIPVOpen')
def unipv_open(week_day):
    return statement(is_unipv_open(week_day))


@ask.intent('EmailProfessor')
def email_professor(professor):
    return statement(get_professor_email(professor))


@ask.intent('ProfessorOffice')
def email_professor(professor):
    return statement(get_professor_office(professor))


@ask.intent('ProfessorLab')
def email_professor(professor):
    return statement(get_professor_lab(professor))


@ask.intent('ProfessorOfficeHour')
def email_professor(professor):
    return statement(get_professor_office_hour(professor))


@ask.intent('ProfessorCourses')
def professor_courses(professor):
    return statement(get_professor_courses(professor))


@ask.intent('WhoAreProfessorsOfCourse')
def who_takes_the_course(course):
    return statement(get_professors_that_take_a_course(course))

@ask.intent('UNIPVopens')
def opening_closing_time():
	speech_text = "L'universita apre alle 7:30 e chiude alle 20"
	return statement(speech_text)
	
@ask.intent('NextExam')
def next_exam(exam):
	return statement(next_hope(exam))
	
@ask.intent('DaySchedule')
def day_schedule(day,year,course):
	_, year, flag = check_active_user()
	if flag:
		return statement(schedule(day,year,course))
	else:
		return statement('Al momento non è presente un utente attivo, riapri la skill e configuralo')
	
@ask.intent('RoomTimeSchedule')
def room_time_schedule(day,year,course):
	_, year, flag = check_active_user()
	if flag:
		return statement(schedule(day,year,course))
	else:
		return statement('Al momento non è presente un utente attivo, riapri la skill e configuralo')
	
@ask.intent('CourseFromTime')
def course_from_time_schedule(day,year,time):
	_, year, flag = check_active_user()
	if flag:
		return statement(schedule(day,year,time=time))
	else:
		return statement('Al momento non è presente un utente attivo, riapri la skill e configuralo')

@ask.intent('CanteenMenu')
def canteen_menu_schedule(day):
	return statement(menu(day))
	
@ask.intent('ExamsSchedule')
def course_exams_schedule(exam):	
	return statement(exams_schedule(exam))
	
@ask.intent('AddUser')
def add_user(name,year):
	if add_user_db(name,year):
		speech_text = f'{name} aggiunto con successo al {year} anno, adesso puoi utilizzare la skill UNIPV'	
		return statement(speech_text)
	else:
		speech_text = "Impossibile aggiungere l'utente con il nome indicato, indica un altro nome e il tuo anno di corso"
		return question(speech_text)

@ask.intent('ChangeUser')
def change_user(name):
	if change_user_db(name):
		speech_text = f'Accesso a {name} avvenuto con successo, adesso puoi utilizzare la skill UNIPV'	
		return statement(speech_text)
	else:
		speech_text = f'Non è presente un utente con il nome {name}, indica un altro nome oppure registrati indicando il nome e il tuo anno di corso'
		return question(speech_text)

@ask.intent('Calendar')
def calendar(day_number,month):
	return(statement(calendar_activity(day_number,month)))

@ask.intent('RemoveUser')
def remove_user_from_db(name):
	if remove_user(name):
		speech_text = f"L'utente {name} è stato rimosso con successo"	
		return statement(speech_text)
	else:
		speech_text = f"Impossibile rimuvere l'utente {name} in quanto è inesistente"	
		return statement(speech_text)

@ask.intent('ChangeYear')
def update_user_in_db(name,year):
	if change_year(name, year):
		speech_text = f"L'utente {name} è stato aggiunto al {year} anno"	
		return statement(speech_text)
	else:
		speech_text = f"Impossibile aggiornare l'anno dell'utente {name}"	
		return statement(speech_text)
		
@ask.launch
def start():
	user, year, flag = check_active_user()
	if not flag:
		speech_text = 'Per effettuare il primo accesso devi dirmi il tuo nome e il tuo anno di corso oppure se sei già registrato rispondi con "cambia utente in" seguito dal tuo nome'
		return question(speech_text)
	speech_text = f'Bentornato {user}, in cosa posso esserti utile?'
	return question(speech_text)

if __name__ == '__main__': 
	app.run()
