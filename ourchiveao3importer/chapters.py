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
            title = h3_tag.find('a')
            if str(title.next_sibling) and str(title.next_sibling).strip():
                title = title.next_sibling.strip(':').strip()
            else:
                title = str(title.contents[0])
        else:
            title = 'Chapter One'
        summary_tag = chapter_tag.find('div', attrs={'id': 'summary'})
        if summary_tag:
            summary = ''
            summary_all = summary_tag.findAll('p')
            for line in summary_all:
                summary = f'{summary}{line}'
        else:
            summary = ''
        notes_tag = chapter_tag.find('div', attrs={'id': 'notes'})
        if notes_tag:
            notes = ''
            notes_all = notes_tag.find('blockquote', attrs={'class': 'userstuff'}).findChildren()
            for line in notes_all:
                if '(See the end of the chapter' in f'{line}':
                    continue
                notes = f'{notes}{line}'
        else:
            notes = ''
        end_notes_tag = chapter_tag.find('div', id=lambda x: x and x.endswith('endnotes'))
        if end_notes_tag:
            end_notes = ''
            end_notes_all = end_notes_tag.find('blockquote', attrs={'class': 'userstuff'}).findChildren()
            for line in end_notes_all:
                end_notes = f'{end_notes}{line}'
        else:
            end_notes = ''
        contents = chapter_tag.find('div', attrs={'role': 'article'})
        content = ''
        if contents:
            for line in contents:
                line_str = f'{line}'
                if line_str == '\n' or 'end cache' in line_str.strip():
                    continue
                if '<h3 class="landmark heading" id="work">' in line_str:
                    continue
                content = f'{content}{line_str}'
        return {"title": title, "content": content, "summary": summary, "notes": notes, "end_notes": end_notes}

    def get_end_notes(self, soup):
        work_end_notes = soup.find('div', id='work_endnotes')
        end_notes = ''
        if work_end_notes:
            end_notes_all = work_end_notes.find('blockquote', attrs={'class': 'userstuff'}).findChildren()
            for line in end_notes_all:
                end_notes = f'{end_notes}{line}'
        self.chapter_content[-1]['end_notes'] = f"{self.chapter_content[-1]['end_notes']}{end_notes}"

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
        multi_chapter = soup.findAll('div', id=lambda x: x and x.startswith('chapter-'))
        if not multi_chapter:
            chapter = soup.find('div', attrs={'id': 'workskin'})
            if chapter is None:
                print(f"Chapter cannot be found for ID {self.id}")
                return
            self.chapter_content.append(self.parsechapter(chapter))
        else:
            count = 1
            for chapter_tag in multi_chapter:
                if chapter_tag is None:
                    print(f"Chapter cannot be found for ID {self.id}")
                    continue
                try:
                    if chapter_tag.findAll('p'):
                        self.chapter_content.append(self.parsechapter(chapter_tag))
                        count += 1
                except AttributeError:
                    raise
        if len(self.chapter_content) > 0:
            self.get_end_notes(soup)


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
