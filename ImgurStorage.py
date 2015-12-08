import base64
import os
import tempfile

from django.core.exceptions import SuspiciousFileOperation
from django.core.files import File
from django.utils._os import safe_join
import requests

from django.core.files.storage import Storage
from imgurpython import ImgurClient

class ImgurStorage(Storage):
    """
    Uses the Imgur cloud service to store images.
    Great for Heroku
    
    This is just a gist, needs some work.
    """
    client_id = "LOL"
    client_secret = "LOL"
    access_token = "LOL"
    refresh_token = "LOL"

    def upload(self, path):
        return self.client.upload_from_path(path)

    def __init__(self):
        super(ImgurStorage, self).__init__()
        self.client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)

    def _open(self, name, mode='rb'):
        file_url = "http://i.imgur.com/{0}.png".format(name)
        r = requests.get(file_url)
        f = tempfile.NamedTemporaryFile(delete=False)
        for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        f.close()
        return File(f)

    def uploaded_path(self, name):
        try:
            path = safe_join(self.location, name)
        except ValueError:
            raise SuspiciousFileOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)

    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        """
        Saves new content to the file specified by name. The content should be
        a proper File object or any python file-like object, ready to be read
        from the beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        if not hasattr(content, 'chunks'):
            content = File(content)

        content.open()

        data = {
            'image': base64.b64encode(content.read()),
            'type': 'base64',
            'meta': {}
        }
        ret = self.client.make_request('POST', 'upload', data, True)
        content.close()
        return ret["id"]

    def url(self, name):
        return "http://i.imgur.com/{0}.png".format(name)

    def get_valid_name(self, name):
        return name

    def exists(self, name):
        return True
