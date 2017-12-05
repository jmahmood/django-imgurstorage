# django-imgurstorage
Store your Django image files on Imgur

You cannot store uploaded image files directly on Heroku due to the ephemeral file system; this can cause problems with your Django models if they have file / image fields.

The normal advice is to use S3 or Bucketeer to store your files; both of those are probably better solutions than this (piggybacking on Imgur's API).

You should be able to use it with the following snippet.

```python
from ImgurStorage import ImgurStorage

image_storage = ImgurStorage()

class Car(models.Model):
    ...
    photo = models.ImageField(storage=image_storage)
```
