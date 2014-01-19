from cx_Freeze import setup, Executable
from os import path

executables = [
    Executable('metadata_form.py')
]

includes = [path.abspath('res/favicon.gif')]

setup(name='DDEXUI',
      version='0.1',
      description='A user interface for distributing ddex deliveries',
      executables=executables,
      include=includes
      )
