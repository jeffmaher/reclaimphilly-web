Setup Reclaim Cities Web
====

To get the project up and running for development, do the following.

Python Setup
====

1. Install Python 2.7.x and setup your PATH to reference the Python binaries
2. Install PIP package manager: `[sudo] easy_install pip`
3. Install Virtualenv: `[sudo] pip install virtualenv`

Project Setup
====
1. Navigate into the project (reclaimphilly-web)
2. `virtualenv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `cd site`
6. `python manage.py syncdb`

Add Texas A&M API Key
====
1. Go to `http://geoservices.tamu.edu/` to apply for an API key.
2. Add your API key to `reclaimcities/settings/settings.py` in the `TAMU_GEOCODING_API_KEY` setting.
