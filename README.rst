
``geocamUtilWeb`` is a set of utilities used by Django web apps in the
GeoCam Share app collection.  It includes the following utilities.

MultiSettings
~~~~~~~~~~~~~

A settings container object built out of an ordered list of child
settings objects.  When you request the value of an attribute, it
returns the value found in the first child that defines that attribute.

We typically use ``MultiSettings`` when apps extend Django settings by
defining new app-specific variables.  For example, if you have an app
``geocamAwesome`` you can put the following in
``geocamAwesome/defaultSettings.py``::

  GEOCAM_AWESOME_ENABLED = True

and in ``geocamAwesome/__init__.py``::

  import django.conf.settings
  from geocamUtil.MultiSettings import MultiSettings
  from geocamAwesome import defaultSettings
  
  settings = MultiSettings(django.conf.settings, defaultSettings)

then you can run::

  $ ./manage.py shell
  >>> from geocamAwesome import settings
  >>> settings.GEOCAM_AWESOME_ENABLED
  True

but if a site administrator adds this line to their site-level
``settings.py``::

  GEOCAM_AWESOME_ENABLED = False

you would see::

  $ ./manage.py shell
  >>> from geocamAwesome import settings
  >>> settings.GEOCAM_AWESOME_ENABLED
  False

The advantage of this approach is that site administrators don't need to
add all of your app's extended settings to their ``settings.py`` file if
they like the defaults, but they can override any setting in a uniform
way.

Actually, ``MultiSettings`` does not depend on Django at all.  It will
work with any kind of child container object as long as its fields can
be accessed using dot notation.

models.UuidField
~~~~~~~~~~~~~~~~

A Django model field that stores a `universally unique identifier`_.
When you first save a model with a ``UuidField``, if the UUID value is
not already set, it is automatically populated with a random (or "type
4") UUID encoded as a ``CharField`` in the standard UUID display format,
which is a series of hex digits separated by hyphens.

.. _universally unique identifier: XXX

You might want to use a ``UuidField`` if you have multiple instances of
your Django app on different hosts and you need to identify the same
object across instances.  We typically do *not* use a ``UuidField`` as the
primary key for a model to avoid a performance penalty.

forms.UuidField
~~~~~~~~~~~~~~~

A Django form field corresponding to the same-name model field.
Validates that the user entered a sequence of hex digits separated by
hyphens.

models.ExtrasField
~~~~~~~~~~~~~~~~~~

A Django model field for storing extra schema-free data.  You can get
and set arbitrary properties on the extra field, which can be comprised
of strings, numbers, dictionaries, arrays, booleans, and ``None``.
These properties are stored in a database ``TextField`` as a
JSON-encoded set of key-value pairs.

.. o  __BEGIN_LICENSE__
.. o  Copyright (C) 2008-2010 United States Government as represented by
.. o  the Administrator of the National Aeronautics and Space Administration.
.. o  All Rights Reserved.
.. o  __END_LICENSE__