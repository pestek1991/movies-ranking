virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

cd portal

python manage.py migrate
python manage.py runserver

===
Celery
==


celery -A portal worker

