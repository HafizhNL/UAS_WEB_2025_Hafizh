Topic: Search Flight

1. lilbrary required
- pip install python-dotenv 
- pip install python-decouple
- pip install Django
- pip install django-cors-headers
- pip install djangorestframework
- pip install amadeus

2. template API token
```
AMADEUS_API_KEY = "isi api key"
AMADEUS_API_SECRET = "isi api secret"
AMADEUS_HOSTNAME = "test" 
```

3. django setup
```
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```

4. run the server
```
py manage.py runserver
```
