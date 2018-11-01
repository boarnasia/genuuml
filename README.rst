genuuml
=======

Generate PlantUML script from python class.

Only test for python 3.6 on Mac

:License: MIT

Getting started
---------------

This command `gunuuml` outputs PlantUML source from python module path.

Just type below command after install::

    shell> genuuml http.client.HTTPConnection
    class http.client.HTTPConnection as "HTTPConnection" {
      +auto_open
      +close
      +connect
      +debuglevel
      +default_port
      +endheaders
      +getresponse
      +putheader
      +putrequest
      +request
      +response_class
      +send
      +set_debuglevel
      +set_tunnel

      +__init__(self, host, port=None, timeout=<object>, source_address=None)
      +close(self)
      +connect(self)
      +endheaders(self, message_body=None, *, encode_chunked=False)
      +getresponse(self)
      +putheader(self, header, *values)
      +putrequest(self, method, url, skip_host=False, skip_accept_encoding=False)
      +request(self, method, url, body=None, headers={}, *, encode_chunked=False)
      +send(self, data)
      +set_debuglevel(self, level)
      +set_tunnel(self, host, port=None, headers=None)
    }

    http.client.HTTPConnection -up-|> builtins.object

    class builtins.object as "object" {
    }

Install
-------

for use::

    shell> pip install git+https://github.com/boarnasia/genuuml#egg=genuuml

for developmet::

    shell> git clone git@github.com:boarnasia/genuuml.git
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

- `genUML <https://github.com/jose-caballero/genUML>`_
- `py2uml <https://github.com/Ivesvdf/py2uml>`_
- `py-puml-tools <https://github.com/deadbok/py-puml-tools>`_
- `genclass.py@gist <https://gist.github.com/stereocat/d6dd2caf60923c6334c6>`_

