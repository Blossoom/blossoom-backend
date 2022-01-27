# Blossoom back-end API 🌸

<a href="https://blossoom-api.herokuapp.com//">![Blossoom](https://img.shields.io/badge/Blossoom-API-9cf?style=for-the-badge)</a>

Blossom is a constructive and inclusive social media network that links artists to each other. 



## Install && Run

Make sure you have **Python 3.x** installed and **the latest version of pip** *installed* before running these steps.

- Clone the repository using the following command && **cd** to the cloned repo

```bash
$ git clone git@github.com:Blossoom/blossoom-backend.git
```

- Create and activate a virtual environment

```bash
# Use this on Linux and Mac
$ python -m venv env
$ source env/bin/activate
```

- Install requirements

```bash
$ pip install -r requirements.txt
```

- Run migrations then create a super user

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

- To run tests

```bash
$ python manage.py test 
```

- To run the development server

```bash
$ python manage.py runserver
```

> admin panel will be on `localhost:8000/admin` or `127.0.0.1:8000/admin`
>
> Root api endpoints will be on (localhost OR 127.0.0.1):8000/api/v1/
