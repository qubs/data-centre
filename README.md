# QUBS Data Centre

A web API for accessing live data from the Queen's University Biological Station Climate Data network. The data
retrieved from this API is provided **completely as-is**. It should be made known that there is no quality assurance
or proofreading done to data stored hear and thus readings may be inaccurate.

## Contents

* [Requirements and Technologies](#requirements-and-technologies)
* [Installation](#installation)
* [Available Data](#available-data)

## Requirements and Technologies

Requirements are listed programmatically in the `requirements.txt` file. The API is built on the
[Django REST Framework](http://www.django-rest-framework.org/) and uses [PostgreSQL](https://www.postgresql.org/) for
a database.

## Installation

### Database

Make sure PostgreSQL 9.5 or later is installed on your web server.

### API Server

1. Download the latest release from the [releases page](https://github.com/qubs/climate-data-api/releases) of the
repository.

2. Unzip it to a directory not directly accessible from the web.

3. Enter the directory and create a virtual environment for the API server withg the command `virtualenv env`.

4. Source the virtual environment with `source env/bin/activate`.

5. Download the dependencies with `pip3 install -r requirements.txt`.

### Apache HTTPD

**BE CAREFUL!** The version of `mod_wsgi` shipped with Ubuntu Server 14.04 does not work with the version of Python 3
provided by the OS. It is necessary to [install a newer version](http://askubuntu.com/questions/569550/assertionerror-using-apache2-and-libapache2-mod-wsgi-py3-on-ubuntu-14-04-python/569551#569551)
of `mod_wsgi`.

`WSGIPassAuthorization On`

1. Make sure to follow the steps above (for setting up the API server) first. For this guide, we will assume the
repository has been cloned into `/var/www/example.com` with the repo itself being located in a folder called
`qubs_data_centre`.

2. Create a virtual host file with the following contents in `/etc/apache2/sites-available`:

```apache
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.ca
    
    ServerAdmin someone@example.com
    
    ErrorLog /var/www/example.com/logs/error.log
    CustomLog /var/www/example.com/logs/access.log combined
    
    Alias /static /var/www/example.com/static
    <Directory /var/www/example.com/static>
        Require all granted
    </Directory>
    
    <Directory /var/www/example.com/qubs_data_centre/qubs_data_centre>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    WSGIDaemonProcess qubs_data_centre processes=1 python-home=/var/www/example.com/qubs_data_centre/env python-path=/var/www/example.com/qubs_data_centre display-name=%{GROUP}
    WSGIProcessGroup qubs_data_centre
    WSGIApplicationGroup %{GLOBAL}
    WSGIScriptAlias / /var/www/example.com/qubs_data_centre/qubs_data_centre/wsgi.py
    WSGIPassAuthorization On
</VirtualHost>
```

3. Enable the site by running `sudo a2ensite example.com`, then running `sudo service apache2 reload`
(if on Ubuntu 14.10 or earlier) or `sudo systemctl reload apache2` (if on Ubuntu 15.04 or later).

4. TODO (upstart/systemd service files)


### NGINX

1. Make sure to follow the steps above (for setting up the API server) first. For this guide, we will assume the
repository has been cloned into `/var/www/example.com` with the repo itself being located in a folder called
`qubs_data_centre`.

2. TODO

## Available Data

Currently, the QUBS Data Centre has APIs for climate data and [Fowler Herbarium](https://fowlerherbarium.ca) specimens.
