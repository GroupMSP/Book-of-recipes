import os
import uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class FilePathGenerator:
    def __init__(self, to=''):
        self.to = to

    def __call__(self, instance, filename):
        extension = os.path.splitext(filename)[1]
        uuid_filename = str(uuid.uuid4()) + extension
        path = os.path.join(
            self.to, uuid_filename[:4], uuid_filename)
        return path