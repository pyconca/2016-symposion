#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists


env.user = 'deploy'
env.path = '/srv/www/pycon.ca/staging.2016/django'
env.remote_env_path = '/srv/www/pycon.ca/staging.2016/django/env'


@hosts(['portland.pynorth.org'])
def deploy():
    # Create a directory on a remote server, if it doesn't already exists
    if not exists(env.path):
        sudo('mkdir -p %(path)s' % env)

    # Create a virtualenv, if it doesn't already exists
    if not exists(env.remote_env_path):
        with cd(env.path):
            sudo('mkdir env')
            sudo('virtualenv env')

    # Sync the remote directory with the current project directory.
    # rsync_project(local_dir='./', remote_dir=env.path,
    #               exclude=['.git', '.idea'])

    local('git archive --format=tar api | gzip > release.tar.gz')
    put('release.tar.gz', env.path, use_sudo=True)

    with cd(env.path):
        sudo('tar zxf release.tar.gz', pty=True)
        local('rm release.tar.gz')

        # Activate the environment and install requirements
        run('source %(remote_env_path)s/bin/activate' % env)
        run('pip install --upgrade -r %(path)s/requirements.txt' % env)

        with shell_env(DJANGO_SETTINGS_MODULE='symposion2016.settings.prod',
                       DATABASE_URL='postgres://symposion:MaG4pInClEdbk5S2yvcP@localhost:5432/pycon2016'):
            # Collect all the static files
            sudo('python manage.py collectstatic --noinput')

            # Migrate and Update the database
            run('python manage.py migrate sites --noinput')
            run('python manage.py migrate auth --noinput')
            run('python manage.py migrate --noinput')

    # Restart the nginx server
    # run('service nginx restart')


def upload_tar_from_git():
    """ Create an archive from the current Git master branch and upload it """
    # require('release', provided_by=[deploy, setup])
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    run('mkdir -p %(path)s/releases/%(release)s' % env, pty=True)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)