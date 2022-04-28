# SSA web application
#### S - Stargardzkie; S - Środowisko; A - Airsoftowe

Application designed to organise environmental matters.

[![Python Version](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.0.4-brightgreen.svg)](https://djangoproject.com)
[![PostgreSQL Version](https://img.shields.io/badge/postgresql-14.2-brightgreen.svg)](https://www.postgresql.org)
[![Bootstrap Version](https://img.shields.io/badge/bootstrap-5.0-brightgreen.svg)](https://getbootstrap.com)

### Running project locally

First, clone the repository to your local machine:

```
git clone git@github.com:mefiuea/ssa.git
or
https://github.com/mefiuea/ssa.git
```

Install the requirements:

```
pip install -r requirements.txt
or 
pipenv install -r path/to/requirements.txt
```

Set all environment variables. 
Go to the env folder, then create an .env file and copy the contents of the .env-default file into it. 
Once this is done, fill the .env file with the appropriate data. 
In the terminal, load the environment variables from this file with the command:

```
source env/.env
```

Change DEBUG mode in settings.py:

```
DEBUG = True
```

Apply the migrations:

```
python manage.py migrate
```

Finally, run the development server:

```
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

!!This code is under development!!
