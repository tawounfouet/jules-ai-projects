
Implemented a real-time chat prototype using Django Channels. 
Features include:
- User authentication (signup/login)
- Multiple chat rooms
- Real-time messaging
- Message persistence
- Typing indicators
- Admin interface for managing rooms

Technical stack: Django 5/6, Channels 4, Daphne, SQLite, Vanilla JS.


```sh
python3.11 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install django channels daphne

pip freeze > requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver


python manage.py createsuperuser

```