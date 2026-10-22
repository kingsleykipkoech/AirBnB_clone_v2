#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from fabric.api import env
from os.path import exists

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['54.157.32.137', '54.89.246.137']


def deploy():
    """Creates and distributes an archive to web servers.

    Returns:
        True if deployment was successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
