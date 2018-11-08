genuuml
=======

PlantUML generator from python script

Supprot for python 3.6 or higher

:License: MIT

Getting started
---------------

`gunuuml` outputs text from python module path according to subcommands.

Just type below command after install::

    shell> genuuml in-plant-uml --print-full-arguments http.client.HTTPConnection
    @startuml

    hide empty members

    class builtins.object as "object"{
    }

    class http.client.HTTPConnection as "HTTPConnection"{
    +auto_open
    +debuglevel
    +default_port
    +response_class
    +__init__(self, host, port, timeout, source_address)
    +close(self)
    +connect(self)
    +endheaders(self, message_body, *, encode_chunked)
    +getresponse(self)
    +putheader(self, header, *values)
    +putrequest(self, method, url, skip_host, skip_accept_encoding)
    +request(self, method, url, body, headers, *, encode_chunked)
    +send(self, data)
    +set_debuglevel(self, level)
    +set_tunnel(self, host, port, headers)
    }

    http.client.HTTPConnection -up-|> builtins.object

    @enduml   @enduml

    shell> genuuml as-ascii-tree http.client.HTTPConnection
    builtins.object
    └── http.client.HTTPConnection

Install
-------

for use::

    shell> pip install git+https://github.com/boarnasia/genuuml#egg=genuuml

for developmet::

    shell> git clone git@github.com:boarnasia/genuuml.git
    shell> cd genuuml
    shell> virtualenv .venv
    shell> source .venv/bin/activate
    shell> pip install -e .[dev]

Usege
-----

::

    Usage: genuuml [OPTIONS] COMMAND [ARGS]...

    Print given classes information in PlantUML format or Ascii Tree format.

    Subcommands can be invoked by giving correct name or a partial name
    included in command name.

    Example:

        `in-plnat-uml` Correct command name is OK
        `in-ascii-tree` Correct command name is OK
        `in-p` A part of command name is also OK
        `in-` A part of command name matching more than one command is NG

    All subcommands receive CLASS_PATHS arguments.  CLASS_PATHS can be
    accepted that are class or module path, and those can be mixed.  When
    module path was given, it would be replaced into class paths defined in
    the module.

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    in-ascii-tree  Print in Ascii Tree format.
    in-plant-uml   Print in PlantUML format.

Utility commands for developer
------------------------------

`pytest` - run test
`pytest --cov=genuuml` - run test with coverage report
`pytest --pep8` - run check PEP8 compliance
`mypy` - run static type checker

Other tools that I know
-----------------------

- `genUML <https://github.com/jose-caballero/genUML>`_
- `py2uml <https://github.com/Ivesvdf/py2uml>`_
- `py-puml-tools <https://github.com/deadbok/py-puml-tools>`_
- `genclass.py@gist <https://gist.github.com/stereocat/d6dd2caf60923c6334c6>`_
- `plantuml-code-generator <https://github.com/bafolts/plantuml-code-generator>`_

