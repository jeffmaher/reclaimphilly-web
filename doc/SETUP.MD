Setup Reclaim Cities Web
====

To get the project up and running for development, do the following.

Python Setup
====

1. Install Python 2.7.x and setup your PATH to reference the Python binaries
1. Install PIP package manager: `easy_install pip`
1. Install Virtualenv: `pip install virtualenv`

Project Setup
====
1. Navigate into the project (reclaimphilly-web)
1. `virtualenv env` 
1. `source env/bin/active`
1. `pip install -r requirements.txt`
1. `cd site`
1. `python manage.py syncdb`
