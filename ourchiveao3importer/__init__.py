# -*- encoding: utf-8

import requests
from .works import Work
from .chapters import Chapters
from .work_list import WorkList

__version__ = "0.1.0"
__author__ = 'Elena, ladyofthelog, alexwlchan'


class OurchiveAo3Importer(object):
    """A scraper for the Archive of Our Own (AO3)."""

    def __init__(self):
        self.user = None
        self.session = requests.Session()

    def __repr__(self):
        return '%s()' % (type(self).__name__)

    def work(self, id):
        """Look up a work that's been posted to AO3.
        :param id: the work ID.  In the URL to a work, this is the number.
            e.g. the work ID of http://archiveofourown.org/works/1234 is 1234.
        """
        return Work(id=id, sess=self.session)

    def chapters(self, id):
        return Chapters(id=id,sess=self.session)

    def work_list(self, username):
        return WorkList(username=username, sess=self.session)
