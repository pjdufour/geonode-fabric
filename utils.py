from fabric.api import settings as fab_settings

from geonodes import GEONODE_INSTANCES as GN


def _build_env(target):
    GNT = GN[target]
    e = {
        'user': GNT['user'],
        'hosts': [GNT['host']],
        'host_string': GNT['host'],
        'key_filename': GNT['ident'],
    }
    return e


def _run_task(task, args):
    from fabfile import targets
    if targets:
        for target in targets:
            with fab_settings(** _build_env(target)):
                task(* args)
    else:
        task(* args)
