.PHONY: runserver m mm mmm sm shell test superuser loaddata i18n

.DEFAULT_GOAL := runserver

runserver:
	python manage.py runserver

# migrate
m:
	python manage.py migrate

# makemigrations
mm:
	python manage.py makemigrations

# makemigrations + migrate
mmm: mm m

# showmigrations
sm:
	python manage.py showmigrations

shell:
	python manage.py shell_plus

test:
	python manage.py test

superuser:
	python manage.py createsuperuser --email=admin@gmail.com --name="Mack AS"

loaddata:
	python manage.py loaddata fixtures/db.json

i18n:
	django-admin makemessages --all --ignore=env
