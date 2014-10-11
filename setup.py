from setuptools import setup

setup(name='twly-ivod-dl',
      version='0.2',
      install_requires=["youtube-dl>=2014.09.25", "BeautifulSoup>=3.2.1"],
      scripts=[
          'scripts/twly-ivod-dl',
          'scripts/twly-ivod-meeting-dl',
          'scripts/twly-ivod-dl-web'],
      packages=['ivod'],
      test_suite='tests.function_test')
