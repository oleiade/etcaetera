.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Etcaetera's documentation!
======================================

What?
-----

Etcaetera helps you loading your application configuration from multiple sources in a simple way.
It exposes a single **Config** object which you add prioritized sources adapters to (*env*, *files*, *cmdline*, *modules*...).

Once you call ``load`` method over it: your settings are loaded from your adapters in order, all your configuration is stored in the **Config** object.

You're **done**.


Why?
----

Managing a large application configuration sources can be a pain in the neck.
Command line, files, system environment, modules, a lot of mixed sources can provide you with the settings you seek.

They are all accessed in different ways, and establishing a merging strategy of these differents sources can sometimes look like impossible.
Etcaetera provides you a simple and unified way to handle all the complexity in a single place.


.. toctree::
   :maxdepth: 4 

   howto
   contributing
   history

