"""
decorator extension for 'nose'.

Allows you to decorate functions, classes, and methods with attributes
without modifying the actual source code.  Particularly useful in
conjunction with the 'attrib' extension package.
"""

import sys
err = sys.stderr

import logging
import os
from nose.plugins.base import Plugin

log = logging.getLogger(__name__)


class Decorator(Plugin):
    score = 99999

    def __init__(self):
        Plugin.__init__(self)

    def add_options(self, parser, env=os.environ):
        parser.add_option("--decorator-file",
                          action="store",
                          dest="decorator_file",
                          default=None,
                          help="Apply attributes in this file to matching functions, classes, and methods")

    def configure(self, options, config):
        self.conf = config

        ### configure logging

        logger = logging.getLogger(__name__)
        logger.propagate = 0

        handler = logging.StreamHandler(err)
        logger.addHandler(handler)

        lvl = logging.WARNING
        if options.verbosity >= 5:
            lvl = 0
        elif options.verbosity >= 4:
            lvl = logging.DEBUG
        elif options.verbosity >= 3:
            lvl = logging.INFO
        logger.setLevel(lvl)

        ### enable plugin & save decorator file name, if given.

        if options.decorator_file:
            self.enabled = True
            self.decorator_file = options.decorator_file

    def begin(self):
        """
        Called before any tests are run.
        """

        filename = self.decorator_file

        fp = open(filename)

        curtains = {}
        for line in fp:

            # skip empty lines or lines with comments ('#')
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # parse attributes...
            name, attribs = line.split(':')
            name = name.strip()
            attribs = [a.strip() for a in attribs.split(',')]

            # ...and store 'em.
            l = curtains.get(name, [])
            l.extend(attribs)
            curtains[name] = l

        # save the attributes in 'self.curtains'.
        self.curtains = curtains

    ######

    def wantClass(self, cls):
        """
        wantClass -- attach matching attributes to the class.
        """
        fullname = '%s.%s' % (cls.__module__, cls.__name__,)
        self._attach_attributes(fullname, cls)

        # indicate no preferences re running this test...
        return None

    def wantMethod(self, method):
        """
        wantMethod -- attach matching attributes to this method.
        """
        if hasattr(method, 'im_class'):
            klass = method.im_class.__name__
        else:
            klass = method.__self__.__class__.__name__
        fullname = '%s.%s.%s' % (method.__module__, klass, method.__name__)

        self._attach_attributes(fullname, method)

        # indicate no preference re running this test...
        return None

    def wantFunction(self, func):
        """
        wantFunction -- attach matching attributes to this function.
        """
        fullname = '%s.%s' % (func.__module__,
                              func.__name__)

        self._attach_attributes(fullname, func)

        # indicate no preferences re running this test.
        return None

    def _attach_attributes(self, fullname, obj):
        """
        Attach attributes matching 'fullname' to the object 'obj'.
        """
        attribs = self.curtains.get(fullname, [])
        log.info('_attach_attributes: %s, %s' % (fullname, attribs,))
        for a in attribs:
            try:
                key, val = a.split("=")
            except ValueError:
                key, val = (a, True)
            try:
                obj.__dict__[key] = val
            except TypeError:
                setattr(obj, key, val)
