#!/usr/bin/python3
# Fabric script that distributes an archive to web servers
from fabric.api import env, put, run
import os

env.hosts = ['54.157.32.137', '54.89.246.137']


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
        archive_name = archive_filename.replace(".tgz", "")
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
