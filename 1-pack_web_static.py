#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static folder."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of web_static folder.

    Returns:
        Archive path if successfully generated, otherwise None.
    """
    local("mkdir -p versions")

    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year,
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        str(now.hour).zfill(2),
        str(now.minute).zfill(2),
        str(now.second).zfill(2)
    )
    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to {}".format(archive_path))

    cmd = "tar -cvzf {} web_static".format(archive_path)
    result = local(cmd, capture=False)

    if os.path.exists(archive_path):
        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    else:
        return None
