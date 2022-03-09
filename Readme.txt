eddit settings.py in docker_ui for database settings
source docker/bin/activate
pip install docker
pip install django
pip install djangorestframework
python3 manage.py makemigration
python3 manage.py migrate
python3 manage.py runserver


usage:


http://127.0.0.1:8000/api/
