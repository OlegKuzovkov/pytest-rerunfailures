from setuptools import setup

setup(name='pytest-rerunfailures',
      version='0.03',
      description='py.test plugin to re-run tests to eliminate flakey failures',
      author='Leah Klearman',
      author_email='lklrmn@gmail.com',
      url='https://github.com/klrmn/pytest-rerunfailures',
      install_requires=['pytest>=2.2.3'],
      py_modules=['rerunfailures.plugin'],
      entry_points={'pytest11': ['pytest_rerunfailures = rerunfailures.plugin']},
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='py.test pytest qa',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'])
