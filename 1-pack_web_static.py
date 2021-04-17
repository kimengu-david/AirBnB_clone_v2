#!/usr/bin/python3
# generates a .tgz archive from the contents of web_static folder

from datetime import datetime
from fabric.api import local
import os.path


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
