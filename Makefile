mig:
	./manage.py makemigrations
	./manage.py migrate

runserver:
	./manage.py runserver

run_bot:
	./manage.py runbot

messages:
	django-admin makemessages -l cyr -l uz -l ru


compile:
	django-admin compilemessages
