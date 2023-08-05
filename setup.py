from setuptools import setup

setup(
    name='ourchive-ao3-importer',
    version='0.1.0',
    description='An AO3 downloader, used in Ourchive code, forked from ladyofthelog and alexwlchan.',
    url='https://github.com/c-e-p/ao3importer',
    author='Elena',
    author_email='imperfectelena@protonmail.com',
    license='MIT license',
    packages=['ourchive-ao3-importer'],
    install_requires=['beautifulsoup4==4.12.2',
                      'certifi==2023.5.7',
                      'cffi==1.15.1',
                      'chardet==5.1.0',
                      'charset-normalizer==3.1.0',
                      'colorama==0.4.6',
                      'cryptography==41.0.1',
                      'cssselect==1.2.0',
                      'EbookLib==0.18',
                      'idna==3.4',
                      'loguru==0.6.0',
                      'lxml==4.9.2',
                      'mobi==0.3.3',
                      'pdfminer.six==20221105',
                      'pdfquery==0.4.3',
                      'pycparser==2.21',
                      'pyquery==2.0.0',
                      'requests==2.31.0',
                      'roman==4.1',
                      'six==1.16.0',
                      'soupsieve==2.4.1',
                      'tqdm==4.65.0',
                      'urllib3>=1.25.4',
                      'win32-setctime==1.1.0'],

    classifiers=[
        'Development Status :: 2 - MVP',
        'Intended Audience :: Fans',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
    ],
)
