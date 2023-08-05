# -*- encoding: utf-8

from datetime import datetime
import json
import itertools
import time

from bs4 import BeautifulSoup, Tag
import requests
from .common import Common


class WorkNotFound(Exception):
    pass


class RestrictedWork(Exception):
    pass


class WorkList(object):

    def __init__(self, username, sess=None):
        self.username = username
        self.work_ids = []
        if sess is None:
            sess = requests.Session()
        self.sess = sess
        self.common = Common()

    def __repr__(self):
        return '%s(username=%r)' % (type(self).__name__, self.username)

    def parseworklist(self, work_list):
        for li in work_list:
            li_id = li['id'].split('_')[1]
            self.work_ids.append(li_id)

    def find_work_ids(self):
        page = 1
        while page < 1000:
            api_url = (f'https://archiveofourown.org/users/{self.username}/works?page={page}')
            req = self.common.recursive_get_data(api_url)
            print(f'Works list page {page}')
            # make sure work can be found
            if req.status_code == 404:
                raise WorkNotFound(f'Unable to find a user with username {self.username}')
            elif req.status_code != 200:
                raise RuntimeError('Unexpected error from AO3 API: %r (%r)' % (
                    req.text, req.status_code))
            if 'This work could have adult content' in req.text:
                # force login to look at this, though theoretically the URL would just have to be modified to add view_adult=true. but i don't want to test this now :P
                raise RestrictedWork('Work ID %s may have adult content')
            if 'This work is only available to registered users' in req.text:
                raise RestrictedWork('Looking at work ID %s requires login')

            soup = BeautifulSoup(req.text, features='html.parser')
            try:
                work_list = soup.find('ol', attrs={'class': 'work'})
                if work_list and work_list.findAll('li'):
                    self.parseworklist(work_list.findAll('li', attrs={'class': 'work'}))
                else:
                    page = 1000
            except AttributeError:
                raise
            page = page + 1


    def json(self, *args, **kwargs):
        """Provide a complete representation of the work in JSON.

        *args and **kwargs are passed directly to `json.dumps()` from the
        standard library.

        """
        data = {
            'work_ids': self.work_ids,
            'username': self.username
        }
        return json.dumps(data, *args, **kwargs)
