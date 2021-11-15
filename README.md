# Jungle Devs - Django Challenge #001

## Usage

### Development
```
$ cd app
$ pip install -r requirements.txt
$ cp .env.example .env
$ cp app/local_settings.example.py app/local_settings.py
```
Set your environment variables in the *.env* file and your local config in the *local_settings.py* file.
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
Navigate to http://localhost:8000/
 
### Production with Docker
```
$ cp app/.env.example app/.env
$ cp app/.env.db.example app/.env.db
```
Set your environment variables in the *app/.env* file and your database variables in *app/.env.db* file.
```
$ docker compose up -d --build
$ docker compose exec web python manage.py migrate
```
## Docs

The API documentation is located in `/docs/`
