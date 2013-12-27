[![Build Status](https://travis-ci.org/willm/DDEXUI.png?branch=master)](https://travis-ci.org/willm/DDEXUI)

#DDEXUI

DDEXUI provides a user interface for supplying digital music in a [ddex](http://ddex.net/) compliant way. It aims to abstract the complexities of ddex for ease of use by smaller independent labels and artists.

DDEXUI is currently in development, but parts of the ddex spec have already been covered.

requires python3.3.

To start the program run:

`
python metadata_form.py
`

### Installing dependencies

#### Linux

Assuming you have pip3 installed:

`
pip install -r requirements.txt
`

#### Windows

install pip3:

`
pip install -r requirements.txt

\#install of pillow and lxml will fail. I haven't yet managed to install lxml on windows, but it is only a dependency on the tests

easy_install Pillow
`
