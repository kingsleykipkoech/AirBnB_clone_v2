#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from datetime import datetime
from fabric.api import env, local, put, run, runs_once
import os

env.hosts = ['54.157.32.137', '54.89.246.137']


@runs_once
def do_pack():
    """Generates a .tgz archive from the contents of web_static folder.

    Returns:
        Archive path if successfully generated, otherwise None.
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        now = datetime.now()
        archive_name = "web_static_{}.tgz".format(
            now.strftime("%Y%m%d%H%M%S")
        )
        archive_path = "versions/{}".format(archive_name)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        True if all operations were successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_name = archive_filename.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(archive_name)

        put(archive_path, "/tmp/{}".format(archive_filename))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))
        run("rm /tmp/{}".format(archive_filename))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to web servers.

    Returns:
        True if deployment was successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
