genuuml
=======

Generate PlantUML script from python class.

:License: MIT

Getting started
---------------

This command `gunuuml` outputs PlantUML source from python module path.

Just type below command after install::

    shell> genuuml http.client.HTTPConnection
    class http.client.HTTPConnection as "HTTPConnection" {
      +auto_open
      +debuglevel
      +default_port
      +response_class

      +close()
      +connect()
      +endheaders()
      +getresponse()
      +putheader()
      +putrequest()
      +request()
      +send()
      +set_debuglevel()
      +set_tunnel()
    }

    http.client.HTTPConnection -up-|> builtins.object

    class builtins.object as "object" {
    }

Install
-------

for user::

    shell> pip install git+https://github.com/boarnasia/genuuml#egg=genuuml

for developmet::

    shell> git clone ..
    shell> cd genuuml
    shell> virtualenv .venv
    shell> source .venv/bin/activate
    shell> pip install -e .

Usege
-----

usage: genuuml [-h] target_class

positional arguments:
  target_class  Class name in python package. ex: scrapy.spiders.CrawlSpider

-h, --hep       show this help message and exit

Other tools that I referred
---------------------------

- `py2uml <https://github.com/Ivesvdf/py2uml>`_
- `py-puml-tools <https://github.com/deadbok/py-puml-tools>`_
- `genclass.py@gist <https://gist.github.com/stereocat/d6dd2caf60923c6334c6>`_
