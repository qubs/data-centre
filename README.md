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

### NGINX

TODO

## Available Data

TODO
