PyCon Setup
===========

ToDo
----

- [x] setup deployment
- [ ] setup `noreply` email

Building `site.css`
-------------------

1. Install [`nvm`](https://github.com/creationix/nvm).
2. Install a version of NodeJS via `nvm`.

   ```
   $ source ~/.nvm/nvm.sh  # or where ever you installed nvm.sh
   $ nvm install <VERSION>
   ```

3. Install the dependencies:

   ```
   $ npm install -g less uglify-js
   ```

4. Build `site.css` (from the project root):

   ```
   $ make site.css
   ```

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

Development Environment Setup
-----------------------------

You will need the following:

* Python 2.7
* pip
* virutalenvwrapper

Start by cloning the repository:

```
$ git clone git@github.com:pyconca/2016-symposion.git 2016-symposion
$ cd 2016-symposion
```

Create a python virtual environment:

```
$ mkvirtualenv pycon_symposion
(pycon_symposion) ~/2016-symposion $
```

The `(pycon_symposion)` prefix indicates that a virtual environment called "pycon_symposion" is being used. Next, check that you have the correct version of Python:

```
(pycon_symposion) ~/2016-symposion $ python --version
Python 2.7.12
(pycon_symposion) ~/2016-symposion $ pip --version
pip 8.0.2 from /Users/.../site-packages (python 2.7)
```

Make sure that postgres development package is installed

```
# aptitude install postgresql-server-dev-9.5
```

Install the project requirements:


```
(pycon_symposion) ~/2016-symposion $ pip install --upgrade -r requirements.txt
```

Collect the static assets:

```
(pycon_symposion) ~/2016-symposion $ python manage.py collectstatic
```

Create the database:

```
(pycon_symposion) ~/2016-symposion $ python manage.py migrate
```

Run the project:

```
(pycon_symposion) ~/2016-symposion $ python manage.py runserver
```

### Extra/Optional PyConCA Custom Symposion

Clone the symposion repository in a new directory:

```
(pycon_symposion) ~/2016-symposion $ cd ..
(pycon_symposion) $ git clone git@github.com:pyconca/symposion.git symposion
(pycon_symposion) ~/symposion $ cd ~/symposion
```

Next replace the GitHub version of symposion with your local copy:

```
(pycon_symposion) ~/symposion $ python setup.py develop
```

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
