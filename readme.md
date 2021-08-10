# Trip Helpmate 

## Table of contents
* [Overview](#overview)
* [Features](#features)
* [Preview](#preview)  
* [Installation](#installation)
* [Setup](#setup)

<a name="overview"></a>
## Overview
**Trip Helpmate** is a web application made with Python web framework Django.
This app allows users to manage their holiday trips from checking basic information like airport location or weather to 
organising luggage, plan trip schedule or store photos.

<a name="main features"></a>
## Features

For every user:
- Displaying basic airport and weather info for selected departure and arrival locations,
- Displaying arrival destination's map (Google Map API),
- Personal account creation,
- Contact page.

Additionally, for registered user:
- Personalized profile for: 
  - viewing/changing personal data, 
  - setting own avatar (default avatar is set automatically as user profile is created), 
  - resetting password (with confirmation link sent via email if provided address is valid)
- Saving trips (departure and arrival locations),
- Creating and saving items which can be used in luggage planning,
- Creating trip schedule,
- Storing photos.

App also offers admin interface for simple management.

<a name="preview"></a>
## Preview
Application is operational and fully deployed at https://triphelpmate.herokuapp.com/

## To install, set up and run app locally:
<a name="installation"></a>
### Installation

#### Prerequisites
- [Python](https://www.python.org/) v. 3.6
- [pip](https://pip.pypa.io/en/stable/) v. 20.2.3
- [Django](https://www.djangoproject.com/) v. 3.1.1
- [asgiref](https://github.com/django/asgiref/) v. 3.2.10
- [dj-database-url](https://github.com/kennethreitz/dj-database-url) v. 0.5.0
- [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/en/master/) v. 3.5.1
- [pytz](https://pythonhosted.org/pytz/) v. 2020.1
- [sqlparse](https://github.com/andialbrecht/sqlparse) v. 0.3.1
- [Pillow](https://python-pillow.org/) v. 7.2.0
- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) v. 1.9.2
- [requests](https://docs.python-requests.org/en/master/) v. 2.24.0
- [django_cleanup](https://github.com/un1t/django-cleanup) v. 5.1.0

#### Set up environment variables

For Linux (Windows users should use 'set' command instead of 'export'):
- set the `SECRET_KEY` variable:
  ```bash 
  export SECRET_KEY='enter_your_secret_key_here'
  ```  

- set database credentials:
  ```bash
  export DATABASE_URL='enter_your_database_url_here'
  ``` 

  or setup own database engine, e.g.:
  ```bash
  export DATABASES='{default: {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3",}}'
  ```

- enable Google Maps API:
  ```bash
  export google_maps_api_key='enter_your_api_key_here'
  ```

  How to obtain Google Maps API key: https://developers.google.com/maps/gmp-get-started?hl=pl#create-project
  

- enable weather API:
  ```bash
  export weather_api_key='enter_your_api_key_here'
  ```  

  How to obtain OpenWeather API key: https://openweathermap.org/appid


- enabling recaptcha:
  ```bash
  export GOOGLE_RECAPTCHA_SECRET_KEY='enter_your_secret_key_here'
  export RECAPTCHA_SITE_KEY='enter_your_secret_key_here'
  ```  

  How to obtain Recaptcha keys: https://developers.google.com/recaptcha/docs/invisible


- enabling contact form:
  ```bash
  export EMAIL_HOST_USER='enter_your_email_address_here'
  export EMAIL_HOST_PASSWORD='enter_your_host_password_here'
  ``` 

#### Install required packages
**>>Remember to set up virtual environment!<<**

```bash
pip install -r requirements.txt
```

#### Make database migration
From app's directory run:
```bash
python manage.py migrate
```

<a name="setup"></a>
### Setup

- Set `DEBUG` mode:\
  ON: `export DEBUG='True'`\
  or\
  OFF:`export DEBUG='False'`

- Prepopulate `Airports` model:
  ```bash
  python manage.py loaddata airports.json
  ```

- Run the app:
  ```bash
  python manage.py runserver
  ```






