from fabric.api import env, sudo, run, cd, local, put, prefix, roles, execute, task
from fabric.api import settings as fab_settings

from geonodes import GEONODE_INSTANCES as GN


def _build_env(target):
    if target in GN:
        GNT = GN[target]
        e = {
            'user': GNT['user'],
            'hosts': [GNT['host']],
            'host_string': GNT['host'],
            'key_filename': GNT['ident'],
        }
        return e
    else:
        print "Could not initialize environment for target {t}.".format(t=target)
        return None


def _run_task(task, args=None, kwargs=None):
    from fabfile import targets
    if targets:
        for target in targets:
            env = _build_env(target)
            if env:
                with fab_settings(** env):
                    _run_task_core(task, args, kwargs)
    else:
        _run_task_core(task, args, kwargs)


def _run_task_core(task, args, kwargs):
    if task:
        if args:
            task(* args)
        elif kwargs:
            task(** kwargs)
        else:
            task()


def _cron_command(f, u, c, filename):
    template = 'echo "{f} {u} {c}" > /etc/cron.d/{filename}'
    cmd = template.format(f=f, u=u, c=c, filename=filename)
    return cmd


def _load_template(filename)
    data = None
    with open ('templates/'+filename, "r") as f:
        data = f.read()
    return data


def _request_input(question, value, required):
    if value:
        return value
    else:
        print question+":",
        if required:
            value = None
            while not value:
                value = raw_input()
                if not value:
                    print "Value required.  Please try again.  Ctrl+C to cancel."
                    print question+":",
            return value
        else:
            return raw_input()


def _request_continue():
    print "Continue (y/n)?",
    confirm = raw_input()
    return confirm and confirm.lower() == "y"


def _append_to_file(lines, filename):
    print "Appending to file..."
    print ""
    sudo("echo '' >> {f}".format(f=filename))
    for line in lines:
        t = "echo '{line}' >> {f}"
        c = t.format(line=line.replace('"','\"'), f=filename)
        sudo(c)
