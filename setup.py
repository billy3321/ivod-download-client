from setuptools import setup

setup(name='ivod_downloader',
      version='0.1',
      install_requires=["youtube-dl>=2014.09.25", "BeautifulSoup>=3.2.1"],
      scripts=[
          'scripts/ivod_downloader.py',
          'scripts/ivod_single_downloader.py',
          'scripts/ivod_schedule_download_web.py'],
      packages=['ivod'],
      test_suite='tests.function_test')
