import os, glob
from fabric.api import env, sudo, run, cd, local, put, prefix, roles, execute, task
from fabric.api import settings as fab_settings
from fabric.context_managers import settings, hide
from fabric.contrib.files import sed
from subprocess import Popen, PIPE
import datetime

from utils import _build_env, _run_task, _cron_command

global targets
targets = ()

PATH_ACTIVATE = "/var/lib/geonode/bin/activate"
PATH_MANAGEPY_VN = "/var/lib/geonode"
PATH_MANAGEPY_GS = "/var/lib/geonode/rogue_geonode"

PATH_DNA_JSON = "/opt/chef-run/dna.json"

PATH_LS_GS = "/var/lib/geonode/rogue_geonode/geoshape/local_settings.py"

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

## GeoSever

@task
def restart_geoserver(*args):
    return _run_task(_restart_geoserver, args=args)


@task
def cron_restart_geoserver(frequency):
    return _run_task(_cron_restart_geoserver, args=[frequency])


## Vanilla

@task
def updatelayers_vanilla(*args):
    return _run_task(_updatelayers_vanilla, args=args)


## GeoSHAPE


@task
def provision_geoshape(*args):
    """
    Provision a GeoSHAPE instance

    Runs `cybergis-scripts-rogue.sh prod provision`
    """

    return _run_task(_provision_geoshape, args=args)


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


@task 
def importlayers_geoshape(local):
    """
    Import local files into a GeoSHAPE instance

    Puts via SFTP local files into the remote's /opt/drop folder and then
    runs importlayers on all of them.
    """

    return _run_task(_importlayers_geoshape, args=[local])


@task
def addgmail_geoshape(username, password):
    """
    Adds server GMail to GeoSHAPE instance

    Adds GMail settings to vim /var/lib/geonode/rogue_geonode/geoshape/local_settings.py

    """

    address = username+'@gmail.com'
    host = 'smtp.gmail.com'
    return _run_task(_addemail_geoshape, args=[address, password, host])


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


def _cron_restart_geoserver(frequency):
    cmd = _cron_command(f=frequency, u ='root', c='/etc/init.d/tomcat7 restart', filename='geoserver_restart')
    print cmd
    sudo(cmd)


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
    sudo('cat '+PATH_DNA_JSON)
    sudo('tail -n 20 /var/log/kern.log')


def _updatelayers_vanilla():
    _updatelayers(PATH_MANAGEPY_VN, PATH_ACTIVATE)


def _updatelayers_geoshape():
    _updatelayers(PATH_MANAGEPY_GS, PATH_ACTIVATE)


def _updatelayers(current_directory, activate):
    with cd(current_directory):
        t = "source {a}; python manage.py updatelayers"
        c = t.format(a=activate)
        sudo(c)

def _importlayers_geoshape(local):
    if local:
        drop = "/opt/drop"
        sudo("[ -d {d} ] || mkdir {d}".format(d=drop))
        remote_files = put(local, drop, mode='0444', use_sudo=True)
        if remote_files:
            _importlayers(PATH_MANAGEPY_GS, PATH_ACTIVATE, remote_files)
        else:
            print "Not files uploaded"
    else:
        print "No local files specified"

def _importlayers(current_directory, activate, files):
    with cd(current_directory):
        t = "source {a}; python manage.py importlayers {paths}"
        c = t.format(a=activate, paths=(" ".join(files)))
        sudo(c)


def _provision_geoshape():
    sudo('cat '+PATH_DNA_JSON)
    sudo("cybergis-scripts-rogue.sh prod provision")


def _addemail_geoshape(address, password, host):
    data = None
    with open ('templates/settings_email.py', "r") as f:
        data = f.read()
        data = data.replace("{{address}}", address)
        data = data.replace("{{password}}", password)
        data = data.replace("{{host}}", host)

    sudo("echo '' >> {ls}".format(ls=PATH_LS_GS)) 
    for line in data.split("\n"):
        t = "echo '{line}' >> {ls}"
        c = t.format(line=line.replace('"','\"'), ls=PATH_LS_GS)
        sudo(c)
