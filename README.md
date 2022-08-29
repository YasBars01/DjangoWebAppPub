# DjangoWebAppPub

Created using Corey Schafer's Tutorial:

https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

## Setup
git clone https://github.com/YasBars01/DjangoWebAppPub.git

pip install -r requirements

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

## If you want to start from scratch
1. delete db.sqlite3
2. delete media > profile_pics
3. delete blog > migrations > 0001_initial.py
4. delete users > migrations > 0001_initial.py
5. pip install -r requirements
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver
