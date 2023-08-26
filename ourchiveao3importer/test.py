from datetime import datetime, timedelta
from importer import OurchiveAo3Importer
import requests
import json
import time


def main():
    api = OurchiveAo3Importer()
    work_datas = []
    print(f'Starting import: {datetime.now()}')
    work_ids = [118678, 43211055, 33568501]
    '''work_list = api.work_list('impertinence')
    work_list.find_work_ids()
    count = 0'''
    '''for work_id in work_ids:
        work = api.work(id=work_id)
        chapter = api.chapters(id=work_id)
        chapter.chapter_contents()
        chapter_json = chapter.json() if chapter else {}
        work_datas.append({work_id: {'work': work.json(), 'chapters': chapter_json}})'''
    work_id = 33568501
    work = api.work(id=work_id)
    chapter = api.chapters(id=work_id)
    chapter.chapter_contents()
    work_datas.append({work_id: {'work': work.__dict__(), 'chapters': chapter.__dict__()}})
    with open('test_data.json', 'w', encoding='utf-8') as f:
        json.dump(work_datas, f, ensure_ascii=False, indent=4)

    print(f'Finished import: {datetime.now()}')


if __name__ == '__main__':
    main()
