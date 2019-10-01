from unipv.db_manager.models import User
from unipv.db_manager.session_manager import start_session
from unipv.db_manager.result_set import queryset2list
from sqlalchemy import and_, or_, update


def add_user_db(name, year):
	if name is None or year is None:
		return False
	name = str(name).lower()
	year = str(year).lower()
	if year == 'primo':
		year = 1
	elif year == 'secondo':
		year = 2
	else:
		return False
	session = start_session()
	queryset = session.query(User).filter(User.name == name)
	session.close()
	if queryset2list(queryset).__len__() > 0:
		session.close()
		return False
	change_user_db(name, False)
	user = User(name = name,year = year,active = True)
	session = start_session()
	session.add(user)
	session.commit()
	session.close()
	return True
	
def check_active_user():
	session = start_session()
	queryset = session.query(User).filter(User.active == True)
	session.close()
	if not queryset2list(queryset).__len__() > 0:
		return None, None, False
	user = queryset2list(queryset)[0]
	return user.name, user.year, True

def change_user_db(name, flag = True):
	name = str(name).lower()
	session = start_session()
	session.query(User).filter(User.active == True).update({"active": False})
	session.commit()
	queryset = session.query(User).filter(User.name == name)
	if not queryset2list(queryset).__len__() > 0:
		session.close()
		return False
	if flag:
		session.query(User).filter(User.name == name).update({'active': True})
		session.commit()
	session.close()
	return True

def remove_user(name):
	if name is None:
		return False
	name = str(name).lower()
	session = start_session()
	queryset = session.query(User).filter(User.name == name)
	if not queryset2list(queryset).__len__() > 0:
		session.close()
		return False
	user = queryset2list(queryset)[0]
	session.delete(user)
	session.commit()
	queryset = session.query(User).filter(User.name == name)
	session.close()
	if queryset2list(queryset).__len__() > 0:
		return False
	return True

def change_year(name, year):
	if name is None and year is None:
		return False
	name = str(name).lower()
	year = str(year).lower()
	if year == 'primo':
		year = 1
	elif year == 'secondo':
		year = 2
	else:
		return False
	session = start_session()
	session.query(User).filter(User.name == name).update({"year": year})
	session.commit()
	queryset = session.query(User.year).filter(User.name == name)
	session.close()
	if int(queryset2list(queryset)[0][0]) == year:
		return True
	return False
