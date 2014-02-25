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
