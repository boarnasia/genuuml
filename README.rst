genuuml
=======

Print given class information in PlantUML format or Ascii Tree format.

Only test for python 3.6 on Mac

:License: MIT

Getting started
---------------

`gunuuml` outputs text from python module path according to subcommands.

Just type below command after install::

    shell> genuuml as-plant-uml http.client.HTTPConnection
    @startuml

    hide empty members

    class builtins.object as "object"{
    }

    class http.client.HTTPConnection as "HTTPConnection"{
    +auto_open
    +debuglevel
    ..(omit)..
    +send(data)
    +set_debuglevel(level)
    +set_tunnel(host, port, headers)
    }

    http.client.HTTPConnection -up-|> builtins.object

    @enduml

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

Usage: genuuml [OPTIONS] COMMAND [ARGS]...

  Print given class information in PlantUML format or Ascii Tree format.

  Subcommands can be invoked by giving correct name or a partial name
  included in command name.

  Example:

      `as-plnat-uml` Correct command name is OK
      `as-ascii-tree` Correct command name is OK
      `as-p` A part of command name is also OK
      `as-` A part of command name matching more than one command is NG

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  as-ascii-tree  Print in Ascii Tree format.
  as-plant-uml   Print in PlantUML format.

Utility commands for developer
------------------------------

`pytest` - run test with coverage report

Other tools that I know
-----------------------

- `genUML <https://github.com/jose-caballero/genUML>`_
- `py2uml <https://github.com/Ivesvdf/py2uml>`_
- `py-puml-tools <https://github.com/deadbok/py-puml-tools>`_
- `genclass.py@gist <https://gist.github.com/stereocat/d6dd2caf60923c6334c6>`_
- `plantuml-code-generator <https://github.com/bafolts/plantuml-code-generator>`_

