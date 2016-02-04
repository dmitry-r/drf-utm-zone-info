import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Location from where we import countries. Shouldn't be written to at runtime.
polyfile_location = settings.OSMAXX_CONVERSION_SERVICE.get('COUNTRIES_POLYFILE_LOCATION') \
    or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'polyfiles')


class CountryInternalStorage(FileSystemStorage):
    """
    country storage which doesn't expose files to the outside world.

    Shouldn't be used outside the country module.

    It saves all data to a `data` subdirectory in the country module.
    """
    def __init__(self, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        super().__init__(
            location=polyfile_location,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode
        )
