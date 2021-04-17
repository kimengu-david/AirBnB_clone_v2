#!/usr/bin/python3
# Creates and distributes an archive to a web server.

from datetime import datetime
from fabric.api import local
import os.path
from fabric.api import put
from fabric.api import run
from fabric.api import env

env.hosts = ["ubuntu@34.73.36.236", "ubuntu@35.231.173.232"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.
        Returns false If the file doesn't exist at
        archive_path or an error occurs
        Otherwise returns True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    file_name_with_ext = archive_path.split("/")[-1]
    file_name_no_ext = file_name_with_ext.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_name_with_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(file_name_no_ext)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(file_name_no_ext)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file_name_with_ext, file_name_no_ext)).failed is True:
        return False
    if run("rm -r /tmp/{}".format(file_name_with_ext)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/"
           .format(file_name_no_ext, file_name_no_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(file_name_no_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(file_name_no_ext)).failed is True:
        return False
    print("New version deployed!")
    return True

def do_pack():
    """Create a tgz archive from web_static directory."""
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_file = "versions/web_static_{}.tgz".format(date_time)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archive_file)).failed is True:
        return None
    return archive_file

def deploy():
    """Creates an archive, then distributes it to a web server."""
    archive_file = do_pack()
    if archive_file is None:
        return False
    return do_deploy(archive_file)
