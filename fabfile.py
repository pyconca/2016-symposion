#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import getpass
from StringIO import StringIO
from fabric.api import *
from fabric.contrib.files import exists
from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = os.path.dirname(__file__)
env.user = 'deploy'

@task
def staging():
    env.environment = 'staging'
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = 'staging.cfp.pycon.ca'
    env.root = '/srv/www/pycon.ca/staging.cfp/django'
    env.branch = 'master'

    env.db_name = 'pycon2016_staging'
    env.db_user = 'symposion'
    env.workers = 1
    env.db_pass = getpass.getpass(prompt="Please enter database (%(db_name)s) password for user %(db_user)s: " % env)

    setup_path()


@task
def production():
    env.environment = 'production'
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = 'cfp.pycon.ca'
    env.root = '/srv/www/pycon.ca/cfp/django'
    env.branch = 'master'

    env.db_name = 'pycon2016'
    env.db_user = 'symposion'
    env.workers = 2
    env.db_pass = getpass.getpass(prompt="Please enter database (%(db_name)s) password for user %(db_user)s: " % env)

    setup_path()


def setup_path():
    env.code_root = os.path.join(env.root, 'symposion2016')
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.logs_root = os.path.join(env.root, 'logs')
    env.run_root = os.path.join(env.root, 'run')


@task
def deploy():
    require('environment')

    # Create a directory on a remote server, if it doesn't already exists
    if not exists(env.code_root):
        sudo('mkdir -p %(code_root)s' % env)

    if not exists(env.logs_root):
        sudo('mkdir -p %(logs_root)s' % env)

    if not exists(env.run_root):
        sudo('mkdir -p %(run_root)s' % env)

    # Create a virtualenv, if it doesn't already exists
    if not exists(env.virtualenv_root):
        with cd(env.root):
            sudo('mkdir env')
            sudo('virtualenv env')

    local('git archive --format=tar %(branch)s | gzip > release.tar.gz' % env)
    put('release.tar.gz', env.code_root, use_sudo=True)

    with cd(env.code_root):
        sudo('tar zxf release.tar.gz', pty=True)
        local('rm release.tar.gz')

        # Activate the environment and install requirements
        # run('source %(remote_env_path)s/bin/activate' % env)
        sudo('source %(virtualenv_root)s/bin/activate && pip install --upgrade -r requirements.txt' % env)

        with shell_env(DJANGO_SETTINGS_MODULE='symposion2016.settings.prod',
                       DATABASE_URL='postgres://%(db_user)s:%(db_pass)s@localhost:5432/%(db_name)s' % env,
                       PYTHONPATH='.'):
            # Collect all the static files
            sudo('%(virtualenv_root)s/bin/python manage.py collectstatic --noinput' % env)

            # Give deploy access to logs and run directories
            sudo('chown -R deploy:deploy %(logs_root)s' % env)
            sudo('chown -R deploy:deploy %(run_root)s' % env)

            # Migrate and Update the database
            run('%(virtualenv_root)s/bin/python manage.py migrate --noinput' % env)

        # gunicorn entry script
        put(get_and_render_template('gunicorn_run.sh', env),
            os.path.join(env.run_root, 'gunicorn_run.sh'), use_sudo=True)
        sudo('chmod u+x %(run_root)s/gunicorn_run.sh' % env)

        # put supervisor conf
        put(get_and_render_template('symposion.conf', env),
            '/etc/supervisor/conf.d/symposion_%(environment)s.conf' % env,
            use_sudo=True)

        # restart supervisor
        sudo('supervisorctl reread && supervisorctl update')
        sudo('supervisorctl restart symposion_%(environment)s' % env)


def get_and_render_template(filename, context):
    jinja_env = Environment(loader=FileSystemLoader('scripts'))
    tmpl = jinja_env.get_template(filename)
    return StringIO(tmpl.render(context))
