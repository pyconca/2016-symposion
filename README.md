PyCon Setup
===========

ToDo
----

- [+] setup deployment
- [ ] setup `noreply` email

Dev quickstart
--------------

1. Clone the repo
2. `cd 2016-symposion`
3. Create virtualenv (ex. `mkvirtualenv pycon_symposion`)
4. Activate virtualenv
5. Install requirements: `pip install --upgrade -r requirements.txt`
6. `python manage.py collectstatic`
7. `python manage.py migrate`
8. `python manage.py runserver`

NOTE: default development settings module is `symposion2016.settings.dev`

Deployment
----------

Have database password handy and run:

    fab <environment> deploy -i <path/to/pub_key>

Environments:

+ `staging`
+ `production` (to come)

Symposion docs
--------------

[Base Project](https://github.com/pinax/pinax-project-symposion)
[Symposion Project](https://github.com/pinax/symposion)
[Docs](https://symposion.readthedocs.io/en/latest/)
