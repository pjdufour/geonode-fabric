import os, glob
from fabric.api import env, sudo, run, cd, local, put, prefix, roles, execute, task
from fabric.api import settings as fab_settings
from fabric.context_managers import settings, hide
from fabric.contrib.files import sed
from subprocess import Popen, PIPE
import datetime

from utils import _build_env, _run_task

global targets
targets = ()

#############################################################
# The Public API
@task
def gn(*args):
    """
    Load GeoNode settings from geonodes.py

    Imports GeoNode settings from a geonodes.py file
    in the same directory
    """
    global targets
    targets = args


@task
def host_type(*args):
    return _run_task(_host_type, args=args)


@task
def lsb_release(*args):
    return _run_task(_lsb_release, args=args)


@task
def restart_geoserver(*args):
    return _run_task(_restart_geoserver, args=args)


@task
def restart_geoshape(*args):
    """
    Restart GeoSHAPE instance, including Django, GeoServer, and RabbitMQ

    Calls ./stop_geonode and ./start_geonode,
    restarts tomcat7, and resets RabbitMQ
    """

    return _run_task(_restart_geoshape, args=args)


@task
def inspect_geoshape(*args):
    return _run_task(_inspect_geoshape, args=args)


@task
def updatelayers_geoshape(*args):
    return _run_task(_updatelayers_geoshape, args=args)


#############################################################
# The Private API

def _host_type():
    run('uname -s')


def _lsb_release():
    run('lsb_release -c')


def _host_type():
    run('uname -s')


def _restart_geoserver():
    sudo('/etc/init.d/tomcat7 restart')


def _restart_apache2():
    sudo('/etc/init.d/apache2 restart')


def _restart_nginx():
    sudo('/etc/init.d/nginx restart')


def _restart_rabbitmq():
    sudo('rabbitmqctl stop_app')
    sudo('rabbitmqctl reset')
    sudo('rabbitmqctl start_app')


def _restart_geoshape():
    with cd("/var/lib/geonode/rogue_geonode/scripts"):
        sudo('./stop_geonode.sh')
        sudo('./start_geonode.sh')

    _restart_geoserver()
    _restart_rabbitmq()


def _inspect_geoshape():
    sudo('lsb_release -c')
    sudo('cat /opt/chef-run/dna.json')
    sudo('tail -n 20 /var/log/kern.log')


def _updatelayers_geoshape():
    with cd("/var/lib/geonode/rogue_geonode"):
        sudo('source /var/lib/geonode/bin/activate; python manage.py updatelayers')
