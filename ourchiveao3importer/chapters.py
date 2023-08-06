# -*- encoding: utf-8

from datetime import datetime
import json
import itertools
import time

from bs4 import BeautifulSoup, Tag
import requests
from common import Common


class WorkNotFound(Exception):
    pass


class RestrictedWork(Exception):
    pass


class Chapters(object):

    def __init__(self, id, sess=None):
        self.id = id
        self.chapter_content = []
        self.common = Common()

    def __repr__(self):
        return '%s(id=%r)' % (type(self).__name__, self.id)

    def parsechapter(self, chapter_tag):
        h3_tag = chapter_tag.find('h3', attrs={'class': 'title'})
        if h3_tag:
            title = str(h3_tag.find('a').contents[0])
        else:
            title = 'Chapter One'
        contents = chapter_tag.find('div', attrs={'role': 'article'})
        content = ''
        if contents:
            contents = contents.findAll('p')
            if contents:
                for line in contents:
                    content = f'{content}{line}'

        return {"title": title, "content": content}

    def chapter_contents(self):
        api_url = ('https://archiveofourown.org/works/%s?view_full_work=true&view_adult=true' % self.id)
        req = self.common.recursive_get_data(api_url)

        # make sure work can be found
        if req.status_code == 404:
            raise WorkNotFound('Unable to find a work with id %r' % self.id)
        elif req.status_code != 200:
            raise RuntimeError('Unexpected error from AO3 API: %r (%r)' % (
                req.text, req.statuscode))
        if 'This work could have adult content' in req.text:
            print(req.text)
            # force login to look at this, though theoretically the URL would just have to be modified to add view_adult=true. but i don't want to test this now :P
            raise RestrictedWork('Work ID %s may have adult content')
        if 'This work is only available to registered users' in req.text:
            raise RestrictedWork('Looking at work ID %s requires login')
        soup = BeautifulSoup(req.text, features='html.parser')
        multi_chapter = soup.findAll('div', attrs={'class': 'chapter'})
        if not multi_chapter:
            chapter = soup.find('div', attrs={'id': 'workskin'})
            if chapter is None:
                print(f"Chapter cannot be found for ID {self.id}")
                return
            self.chapter_content.append(self.parsechapter(chapter))
        else:
            for chapter_tag in multi_chapter:
                if chapter_tag is None:
                    print(f"Chapter cannot be found for ID {self.id}")
                    continue
                try:
                    if chapter_tag.findAll('p'):
                        self.chapter_content.append(self.parsechapter(chapter_tag))
                except AttributeError:
                    raise


    def json(self, *args, **kwargs):
        """Provide a complete representation of the work in JSON.

        *args and **kwargs are passed directly to `json.dumps()` from the
        standard library.

        """
        data = {
            'id': self.id,
            'content': self.chapter_content
        }
        return json.dumps(data, *args, **kwargs)

    def __dict__(self):
        data = {
            'id': self.id,
            'content': self.chapter_content
        }
        return data
