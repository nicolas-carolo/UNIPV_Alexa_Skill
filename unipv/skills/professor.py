from unipv.db_manager.models import Professor, Course
from unipv.db_manager.session_manager import start_session
from unipv.db_manager.result_set import queryset2list
from unipv.tools.words import reverse_words
from sqlalchemy import or_


def get_professor_email(professor):
    if professor is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    professor_result = get_professor(professor)
    if professor_result is not None:
        email = professor_result.email
        if professor_result.gender == 'male':
            title = 'del professor '
        else:
            title = 'della professoressa '
        return "L'indirizzo email " + title + professor.title() + " è " + email
    else:
        return "Mi dispiace, non so rispondere alla tua domanda"


def get_professor_courses(professor):
    if professor is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    professor_result = get_professor(professor)
    if professor_result is not None:
        if professor_result.gender == 'male':
            title = 'il professor '
        else:
            title = 'la professoressa '
        full_name_professor = professor_result.full_name
        session = start_session()
        queryset = session.query(Course).filter(Course.professor == full_name_professor)
        courses_list = queryset2list(queryset)
        session.close()
        if courses_list.__len__() == 0:
            return "Attualmente " + title + full_name_professor.title() + " non tiene nessun corso"
        elif courses_list.__len__() == 1:
            return "Attualmente " + title + full_name_professor.title() + " tiene il corso di " + str(courses_list[0].course_name).title()
        else:
            speech_text = "Attualmente " + title + full_name_professor.title() + " tiene i corsi di "
            for course in courses_list:
                if (courses_list.index(course) + 1) == courses_list.__len__():
                    speech_text = speech_text + " e di " + str(course.course_name).title()
                else:
                    speech_text = speech_text + str(course.course_name).title() + ", "
            return speech_text
    else:
        return "Mi dispiace, non so rispondere alla tua domanda"


def get_professors_that_take_a_course(course):
    print(course)
    if course is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    course = str(course).lower()
    session = start_session()
    queryset = session.query(Course).filter(or_(Course.alias == course))
    courses_list = queryset2list(queryset)
    session.close()
    if courses_list.__len__() == 0:
        return "Nessun professore tiene il corso di " + course.title()
    elif courses_list.__len__() == 1:
        professor = get_professor(courses_list[0].professor)
        if professor.gender == 'male':
            title = 'dal professor '
        else:
            title = 'dalla professoressa '
        return "Il corso di " + str(courses_list[0].course_name).title() + " è tenuto " + title + str(professor.full_name).title()
    else:
        speech_text = "Il corso di " + str(courses_list[0].course_name).title() + " è tenuto dai professori "
        for course in courses_list:
            if (courses_list.index(course) + 1) == courses_list.__len__():
                speech_text = speech_text + " e " + str(course.professor).title()
            else:
                speech_text = speech_text + str(course.professor).title() + ", "
        return speech_text


def get_professor_office(professor):
    if professor is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    professor_result = get_professor(professor)
    if professor_result is not None:
        office = professor_result.office
        if professor_result.gender == 'male':
            title = 'del professor '
        else:
            title = 'della professoressa '
        office_words_list = str(office).split()
        if office_words_list[0] == "laboratorio":
            return "L'ufficio " + title + str(professor_result.full_name).title() + " si trova nel " + str(office).title()
        elif office_words_list[0] == "piano":
            return "L'ufficio " + title + str(professor_result.full_name).title() + " si trova al " + str(office).title()
        elif office == 'non disponibile':
            return "Nessuna informazione disponibile sull'ufficio " + title + str(professor_result.full_name).title()
        else:
            return "L'ufficio " + title + str(professor_result.full_name).title() + " è il " + str(office).title()
    else:
        return "Mi dispiace, non so rispondere alla tua domanda"


def get_professor_office_hour(professor):
    if professor is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    professor_result = get_professor(professor)
    if professor_result is not None:
        office = professor_result.office
        office_hour = professor_result.office_hour
        if professor_result.gender == 'male':
            title = 'Il professor '
        else:
            title = 'La professoressa '
        office_words_list = str(office).split()
        if office_words_list[0] == "laboratorio":
            office_string = " presso il suo ufficio nel " + str(office).title()
        elif office_words_list[0] == "piano":
            office_string = " presso il suo ufficio al " + str(office).title()
        elif office_hour == 'non disponibile':
            if professor_result.gender == 'male':
                title = 'del professor '
            else:
                title = 'della professoressa '
            return "Nessuna informazione disponibile sull'orario di ricevimento " + title + str(professor_result.full_name).title()
        else:
            office_string = " presso il suo ufficio " + str(office).title()
        return title + str(professor_result.full_name).title() + " riceve " + office_hour + office_string
    else:
        return "Mi dispiace, non so rispondere alla tua domanda"


def get_professor_lab(professor):
    if professor is None:
        return "Mi dispiace, non so rispondere alla tua domanda"
    professor_result = get_professor(professor)
    if professor_result is not None:
        lab = professor_result.lab
        if professor_result.gender == 'male':
            title = 'del professor '
        else:
            title = 'della professoressa '
        if lab == 'non disponibile':
            return "Nessuna informazione disponibile sul laboratorio " + title + str(professor_result.full_name).title()
        else:
            return "Il laboratorio " + title + str(professor_result.full_name).title() + " è il " + str(lab).title()
    else:
        return "Mi dispiace, non so rispondere alla tua domanda"


def get_professor(professor):
    professor = str(professor).lower()
    session = start_session()
    queryset = session.query(Professor).filter(or_(Professor.surname == professor, Professor.full_name == professor,
                                                   Professor.full_name == reverse_words(professor)))
    session.close()
    if queryset2list(queryset).__len__() > 0:
        return queryset2list(queryset)[0]
    else:
        return None
