# Django Blog

This is practical homework

## Overview

This web application is an online blog in which users can register, write their own posts, read posts of other authors, create comments and manage their accounts.

The main features that have currently been implemented are:

* There are models for user, posts, and comments.
* Users can view list and detail information of published posts and comments.
* Authorized users (who have the appropriate permissions) can update their profile and post, as well as change the post status (Draft/Publish).
* Admin users can manage the posts and comments (change the status), create new users, posts, comments, etc...

## Quick Start

To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip install -r dev-requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
   to run tests:
   - `tox` run all tests (flake8, black, unittests)
   - `tox -epep8` run flake8 tests
   - `tox -eblack` run black diff tests
   - `tox -etest` run only unittests
   - 
1. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
1. Create a few test objects of each type.
1. In another browser (or use Incognito mode in current browser) open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.
