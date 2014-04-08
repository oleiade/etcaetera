.. _guide:

======
How to
======


.. _installation:

Installation
============

With pip
--------

.. code-block:: bash

    $ pip install etcaetera

With setuptools
---------------

.. code-block:: bash

    $ git clone git@github.com:oleiade/etcaetera
    $ cd etcaetera
    $ python setup.py install


.. _usage:

Usage
=====

.. _dive:

Dive
----

A real world example is worth a thousand words

.. code-block:: python

    >>> from etcaetera.config import Config
    >>> from etcaetera.adapters import Defaults, Module, Overrides, Env, File

    # Let's create a new configuration object
    >>> config = Config()

    # And create a bunch of adapters
    >>> env_adapter = Env("MY_FIRST_SETTING", "MY_SECOND_SETTING")
    >>> python_file_adapter = File('/etc/my/python/settings.py')
    >>> json_file_adapter = File('/etc/my_json_settings.json')
    >>> module_adapter = Module(os)
    >>> overrides = Overrides({"MY_FIRST_SETTING": "my forced value"})

    # Let's register them
    >>> config.register(env_adapter, python_file_adapter, json_file_adapter, module_adapter, overrides)

    # Load configuration
    >>> config.load()


    # And that's it
    >>> print config
    {
        "MY_FIRST_SETTING": "my forced value",
        "MY_SECOND_SETTING": "my second value",
        "FIRST_YAML_SETTING": "first yaml setting value found in yaml settings",
        "FIRST_JSON_SETTING": "first json setting value found in json settings",
        ...
    }


.. _config_object:

Config object
-------------

The config object is the central place for your whole application settings. It loads your adapters in the order you've registered them, and updates itself using it's data.
Furthermore you can attach sub config objects to it, in order to keep a clean configuration hierarchy.


Please note that **Defaults** adapter will always be loaded first, and **Overrides** will always be loaded last.

.. code-block:: python

    >>> from etcaetera.config import Config
    >>> from etcaetera.adapters import Defaults, Module, Overrides, Env, File

    # Let's create a new configuration object
    >>> config = Config()

    # And create a bunch of adapters
    >>> env_adapter = Env("MY_FIRST_SETTING", "MY_SECOND_SETTING")
    >>> python_file_adapter = File('/etc/my/python/settings.py')
    >>> json_file_adapter = File('/etc/my_json_settings.json')
    >>> module_adapter = Module(os)
    >>> overrides = Overrides({"MY_FIRST_SETTING": "my forced value"})

    # Let's register them
    >>> config.register(env_adapter, python_file_adapter, json_file_adapter, module_adapter, overrides)

    # Load configuration
    >>> config.load()


    # And that's it
    >>> print config
    {
        "MY_FIRST_SETTING": "my forced value",
        "MY_SECOND_SETTING": "my second value",
        "FIRST_YAML_SETTING": "first yaml setting value found in yaml settings",
        "FIRST_JSON_SETTING": "first json setting value found in json settings",
        ...
    }

    # If you need a certain hierarchy for your configuration
    # Config objects supports sub configs. Here's an example of
    # how to add an "aws" subconfig
    >>> aws_config = Config()  # Create a config obj
    >>> aws_env = Env("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY")
    >>> aws_config.register(aws_env)  # Register an env adapter on to it
    >>> config.add_subconfig('aws', aws_config)
    >>> config.aws
    {
        "AWS_ACCESS_KEY_ID": "128u09ijod019jhd182o1290d81",
        "AWS_SECRET_ACCESS_KEY": "qoiejdn0182hern1d098uj12podij1029udaiwjJBIU09u0oimJHKI"
    }


.. _adapters:

Adapters
--------

Adapters are the interfaces with configuration sources. They load settings from their custom source type,
and they expose them as a normalized dict to *Config* objects.

Right now, etcaetera provides the following adapters:
    * *Defaults*: sets some default settings
    * *Overrides*: overrides the config settings values
    * *Env*: extracts configuration values from system environment
    * *File*: extracts configuration values from a file. Accepted format are: json, yaml, python module file (see *File adapter* section for more details)
    * *Module*: extracts configuration values from a python module. Like in django, only uppercased variables will be matched

In a close future, etcaetera may provide adapters for:
    * *Argv* argparse format support: would load settings from an argparser parser attributes
    * *File* ini format support: would load settings from an ini file

Cool features you should know about:
    * You can provide a *formatter* to your adapters so the imported keys will be automatically modified. Example ``Env("USER", etcaetera.formatters.lowercased)`` will import the ``$USER`` environment variable as ``user`` when ``.load()`` is called. 

.. _defaults:

Defaults adapter
~~~~~~~~~~~~~~~~

Defaults adapter provides your configuration object with default values.
It will always be evaluated first when ``Config.load`` method is called.
You can whether provide defaults values to *Config* as a *Defaults* object
or as a dictionary.

.. code-block:: python

    >>> from etcaetera.adapter import Defaults

    # Defaults adapter provides default configuration settings
    >>> defaults = Defaults({"ABC": "123"})
    >>> config = Config(defaults)

    >>> print config
    {
        "ABC": "123"
    }


.. _overrides:

Overrides adapter
~~~~~~~~~~~~~~~~~

The Overrides adapter overrides *Config* object values with it's own values.
It will always be evaluated last when the ``Config.load`` method is called.

.. code-block:: python

    >>> from etcaetera.adapter import Overrides

    # The Overrides adapter helps you set overriding configuration settings.
    # When registered over a Config objects, it will always be evaluated last.
    # Use it if you wish to force some config values.
    >>> overrides_adapter = Overrides({"USER": "overrided value"})
    >>> config = Config({
        "USER": "default_value",
        "FIRST_SETTING": "first setting value"
    })

    >>> config.register(overrides_default)
    >>> config.load()

    >>> print config
    {
        "USER": "overrided user",
        "FIRST_SETTING": "first setting value"
    }


.. _env:

Env adapter
~~~~~~~~~~~

Env adapter loads configuration variables values from system environment.
You can whether provide it a list of keys to be fetched from environment. Or you can pass it a *environment variables name to adapter destination name* ``**mappings`` dict.
Moreover, as adapters support nested keys through the ``.`` separator you can map any env var to a nested adapter destination.

.. code-block:: python

    >>> from etcaetera.adapter import Env

    # You can provide keys to be fetched by the adapter at construction
    # as keys
    >>> env = Env("USER", "PATH")
    >>> env.load()
    >>> print env.data
    {
        "USER": "user extracted from environment",
        "PATH": "path extracted from environment",
        "PWD": "pwd extracted from environment"
    }

    # alternatively pass it as env var names to adapter var 
    # names dict
    >>> os.environ["SOURCE"], os.environ["OTHER_SOURCE"]
    ("my first value", "my second value")
    >>> env = Env({"SOURCE": "DEST", "OTHER_SOURCE": "TEST"})
    >>> env.load()
    >>> print env.data
    {
        "DEST": "my first value",
        "TEST": "my second value"
    }

    # Adapters support nested destination too
    >>> env = Env({"MY.USER": "USER"})
    >>> env.load()
    >>> print env.data
    {
        "MY": {
            "USER": "oleiade",
        }
    }

.. _file:

File adapter
~~~~~~~~~~~~

The File adapter will load the configuration settings from a file.
Supported formats are json, yaml and python module files. Every key-value pairs
stored in the pointed file will be loaded in the *Config* object it is registered to.


Python module files
```````````````````

The Python module files should be in the same format as the Django settings files. Only uppercased variables
will be loaded. Any python data structures can be used.

*Here's an example*

*Given the following settings.py file*

.. code-block:: bash

    $ cat /my/settings.py
    FIRST_SETTING = 123
    SECOND_SETTING = "this is the second value"
    THIRD_SETTING = {"easy as": "do re mi"}
    ignored_value = "this will be ignore"

*File adapter output will look like this*:

.. code-block:: python

    >>> from etcaetera.adapter import File

    >>> file = File('/my/settings.py')
    >>> file.load()

    >>> print file.data
    {
        "FIRST_SETTING": 123,
        "SECOND_SETTING": "this is the second value",
        "THIRD_SETTING": {"easy as": "do re mi"}
    }

Serialized files (aka json and yaml)
````````````````````````````````````

*Given the following json file content*:

.. code-block:: bash

    $ cat /my/json/file.json
    {
        "FIRST_SETTING": "first json file extracted setting",
        "SECOND_SETTING": "second json file extracted setting"
    }

*The File adapter output will look like this*:

.. code-block:: python

    >>> from etcaetera.adapter import File

    # The File adapter awaits on a file path at construction.
    # All you have to do then, is to let the magic happen
    >>> file = File('/my/json/file.json')
    >>> file.load()

    >>> print file.data
    {
        "FIRST_SETTING": "first json file extracted setting",
        "SECOND_SETTING": "second json file extracted setting"
    }


.. _module:

Module adapter
~~~~~~~~~~~~~~

The Module adapter will load settings from a python module. It emulates the django
settings module loading behavior, so that every uppercased locals of the module is matched.

**Given a mymodule.settings module looking this**:

.. code-block:: python

    MY_FIRST_SETTING = 123
    MY_SECOND_SETTING = "abc"

**Loaded module data will look like this**:

.. code-block:: python

    >>> from etcaetera.adapter import Module

    # It will extract all of the module's uppercased local variables
    >>> module = Module(mymodule.settings)
    >>> module.load()

    >>> print module.data
    {
        MY_FIRST_SETTING = 123
        MY_SECOND_SETTING = "abc"
    }

