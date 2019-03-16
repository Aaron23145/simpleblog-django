# Simpleblog

Simpleblog is a very simple CMS built with Django, which makes use of Python. You can see it live here: [Simpleblog in Heroku](https://simpleblog-django.herokuapp.com). It is not designed to be used for real use, because it lacks a little in features, but it can be expanded.

If you want to access to the EditorCP by yourself, you'll need a user that has editor permissions, something that's impossible to get without an account with admin permissions. However, here are some precreated users that are editors:

| User | Password |
| ---- | -------- |
| Editor1 | 59f*Ow23Z |
| Editor2 | L.2fJ8sl1 |
| Editor3 | ds9L?Pz23 |

## Features

- Auth System, which allows creating new users and logging with existing ones.
- Entry System, which allows to the Editors and Administrators to create, delete and edit the entries that will appear in the blog.
- Tag System, which allows to the Editors and Administrators to create, delete and edit tags that will help describing the entries.
- Important Entries System, which allows to the Editors and Administrators to register and unregister entries as important, which will make them appear in a carousel in the blog pages.

## Install

To install this CMS to run it locally, you will need Python 3.7.1 installed at least. It haven't been tested with previous versions, but it could work if the version of Django used supported it. You'll also need pip installed, then, you should create a virtual env or install the requirements globally, with the following command:

```sh
pip install -r dev-requirements.txt
```

Lastly, you have to apply the migrations to set up your database and run the server in debug mode:

```sh
python manage.py migrate
python manage.py runserver
```

You don't need to have installed any database in your computer. It uses SQLite locally.

## Deploying

To deploy this CMS, you will have to set the following environment vars in your server:

| Variable | Value |
| -------- | ----- |
| DJANGO_DEBUG | True |
| DJANGO_SIMPLEBLOG_SECRET_KEY | With a new random secret key. Please, don't use the default secret key because it could derive in security issues. You can generate a new secret key here: [Django Secret Key Generator](https://www.miniwebtool.com/django-secret-key-generator/). |

If you're trying to deploy in Heroku, this should be enough.
