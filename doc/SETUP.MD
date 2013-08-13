Setup Reclaim Cities Web
====

To get the project up and running for development, do the following. 

Note: Sincere apologizes to Windows developers -- these are very Mac/Linux/Unix centric instructions. We'll get Windows instructions up in the future, however, being a developer, you're probably smart enough to figure out where to go from here based on the below directions.

Python Setup
====

1. Install Python 2.7.x and setup your PATH to reference the Python binaries
2. Install PIP package manager: `[sudo] easy_install pip`
3. Install Virtualenv: `[sudo] pip install virtualenv`

Project Setup
====
1. Navigate into the project (the root of the cloned files)
2. `cd site`
2. `virtualenv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `cd site`
6. `python manage.py syncdb` (this will walk you through creating an admin user)

Add Texas A&M API Key
====
1. Go to `http://geoservices.tamu.edu/` to apply for an API key.
2. Add your API key to `(project root)/site/reclaimcities/settings/settings.py` in the `TAMU_GEOCODING_API_KEY` setting.