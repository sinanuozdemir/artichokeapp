from legion.modules import makePerson, getPerson
import legion.c_4 as c_4
from celery import shared_task, task
from legion.models import Person, EmailAddress
from dashboard.models import Connection
from dashboard.modules import completePerson




@task(queue='default')
def connectEmailToUser(**kwargs):
	user_id = kwargs['user_id']
	validate_first = kwargs.get('validate_first', True)
	verbose = kwargs.get('verbose', True)
	for i in ['validate_first', 'user_id', 'verbose']:
		try:
			del kwargs[i]
		except:
			pass
	try:
		email = kwargs['email'].lower().strip().decode('utf-8')
		del kwargs['email']
	except: return None
	try: e = EmailAddress.objects.get(address__iexact=email)
	except EmailAddress.DoesNotExist: e = None
	if e:
		completePerson(e.person.id)
		connection, new_connection = Connection.objects.get_or_create(person = e.person, user_id = user_id, defaults = kwargs)
		if new_connection:
			Connection.objects.filter(pk = connection.id).update(**kwargs)
		return connection.id
	print "using the c4"
	person_legion = c_4.Scanner(email_to_find = email, validate_first = validate_first, verbose = verbose).ScanForSocialMedias()
	try:
		info = person_legion.information
	except:
		info = person_legion
	person, person_created = makePerson(info)
	connection, new_connection = Connection.objects.get_or_create(person = person, user_id = user_id, defaults = kwargs)
	if new_connection:
		Connection.objects.filter(pk = connection.id).update(**kwargs)
	return connection.id




