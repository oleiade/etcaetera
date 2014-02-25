===============================
Etcaetera
===============================

.. image:: https://badge.fury.io/py/etcaetera.png
    :target: http://badge.fury.io/py/etcaetera
    
.. image:: https://travis-ci.org/oleiade/etcaetera.png?branch=master
        :target: https://travis-ci.org/oleiade/etcaetera

.. image:: https://pypip.in/d/etcaetera/badge.png
        :target: https://crate.io/packages/etcaetera?version=latest

What?
=====

Etcaetera helps you loading your application configuration from multiple sources in a simple way.
It exposes a single **Config** object which you add prioritized sources adapters to (env, files, cmdline, modules...).
Once you call ``load`` method over it: You're done. Your settings are loaded from your adapters in order, and your
all configuration is stored in the **Config** object.
You're done.


Why?
====

Managing a large application configuration sources can be a pain in the neck.
Command line, files, system environment, modules, a lot of mixed sources can provide you with the settings you seek.
They are all accessed in different ways, and establishing a merging strategy of these differents sources can sometimes look like impossible.
Etcaetera provides you a simple and unified way to handle all the complexity in a single place.

Installation
============

With pip
--------

.. code-block:: bash

    pip install etcaetera

With setuptools
---------------

.. code-block:: bash

    git clone git@github.com:oleiade/etcaetera
    cd etcaetera
    python setup.py install


Usage
=====

A real world example worths it all

.. code-block:: python

    from etcaetera.config import Config
    from etcaetera.adapters import Defaults, Overrides, Env, File

    # Let's create a new configuration object
    config = Config()

    # And create a bunch of adapters
    env_adapter = Env(keys=["MY_FIRST_SETTING", "MY_SECOND_SETTING"])
    yaml_file_adapter = File('/etc/my_yaml_settings.yaml')
    json_file_adapter = File('/etc/my_json_settings.json')
    overrides = Overrides({"MY_FIRST_SETTING": "my forced value"})

    # Let's register them
    config.register([env_adapter, yaml_file_adapter, json_file_adapter, overrides])

    # Load configuration
    config.load()


    # And that's it
    print config
    {
        "MY_FIRST_SETTING": "my forced value",
        "MY_SECOND_SETTING": "my second value",
        "FIRST_YAML_SETTING": "first yaml setting value found in yaml settings",
        "FIRST_JSON_SETTING": "first json setting value found in json settings",
        ...
    }


Adapters
--------

Adapters are interfaces to configuration sources. They load settings from their custom source type,
and expose them as a normalized dict to *Config* objects.

Right now, etcaetera provides the following adapters:
    * *Defaults*: sets some default settings
    * *Overrides*: overrides the config settings values
    * *Env*: extracts configuration values from system environment
    * *File*: extracts configuration values from a file. Accepted format are: json, yaml, python module file (see *File adapter* section for more details)

In a close future, etcaetera may provide adapters for:
    * *Module*: would load settings from a $PYTHONPATH module. Upper cased locals would then be matched
    * *File* ini format support: would load settings from an ini file

Defaults adapter
~~~~~~~~~~~~~~~~

Defaults adapter provides your configuration object with default values.
It will always be evaluated first when ``Config.load`` method is called.
You can whether provide defaults values to *Config* as a *Defaults* object
or as a dictionary.

.. code-block:: python

    from etcaetera.adapter import Defaults

    # Defaults adapter provides default configuration settings
    defaults = Defaults({"ABC": "123"})
    config = Config(defaults)

    print config
    {
        "ABC": "123"
    }

Overrides adapter
~~~~~~~~~~~~~~~~~

Overrides adapter will override *Config* object values with it's own.
It will always be evaluated last when ``Config.load`` method is called.

.. code-block:: python

    from etcaetera.adapter import Overrides

    # Overrides adapter helps you setting overriding configuration settings.
    # When registered over a Config objects, it will always be evaluated last.
    # Use it if you wish to force some config values.
    overrides_adapter = Overrides({"USER": "overrided value"})
    config = Config({
        "USER": "default_value",
        "FIRST_SETTING": "first setting value"
    })

    config.register(overrides_default)
    config.load()

    print config
    {
        "USER": "overrided user",
        "FIRST_SETTING": "first setting value"
    }



Env adapter
~~~~~~~~~~~

Env adapter will load settings from your system environement.
It should be provided with a list of keys to fetch. If you don't provide
it yourself, the *Config* object it's registered to will automatically
provide it's own.

.. code-block:: python

    from etcaetera.adapter import Env

    # You can provide keys to be fetched by the adapter at construction
    env = Env(keys=["USER", "PATH"])

    # Or whenever you call load over it. They will be merged
    # with those provided at initialization.
    env.load(keys=["PWD"])

    print env.data
    {
        "USER": "user extracted from environment",
        "PATH": "path extracted from environment",
        "PWD": "pwd extracted from environment"
    }

File adapter
~~~~~~~~~~~~

File adapter will load configuration settings from a file.
Supported formats are json, yaml and python module files. Every key-value pairs
stored in the pointed file will be load in the *Config* object it is registered to.

.. code-block:: python

    from etcaetera.adapter import File

    # File adapter awaits on a file path at construction.
    # All you've gotta do then, is letting the magic happen
    file = File('/my/json/file.json')
    file.load()

    print file.data
    {
        "FIRST_SETTING": "first json file extracted setting",
        "SECOND_SETTING": "second json file extracted setting"
    }


Contribute
==========

Please read the `<Contributing >`_ instructions

For the lazy, here's a sum up:

1. Found a bug? Wanna add a feature? Check for open issues or open a fresh issue to start a discussion about it.
2. Fork the repository, and start making your changes
3. Write some tests showing you fixed the actual bug or your feature works as expected
4. Fasten your seatbelt, and send a pull request to the *develop* branch.


* Free software: MIT license
* Documentation: http://etcaetera.rtfd.org.
