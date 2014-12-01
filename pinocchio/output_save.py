"""
A nose plugin that saves test stdout into files.  Useful for situations where
lots of tests are breaking and you don't want to have to scroll through a
bunch of output to find individual test output.
"""

import sys
stderr = sys.stderr

import nose.case

import logging
import os
from nose.plugins.base import Plugin
import string

try:
    from StringIO import StringIO as p_StringO
except:
    from io import StringIO as p_StringO

import traceback

def write_test_output(test, output, dirname, prefix=''):
    testname = calc_testname(test)

    filename = '%s%s.txt' % (prefix, testname,)
    if dirname:
        filename = os.path.join(dirname, filename)

    fp = open(filename, 'w')
    fp.write(output)
    fp.close()

log = logging.getLogger(__name__)

# Based on code from http://stackoverflow.com/a/295146/28275
valid_chars = frozenset("-_.()%s%s" % (string.ascii_letters, string.digits))
def sanitize_filename(name):
    return ''.join(c for c in name if c in valid_chars)

def calc_testname(test):
    # For errors at module-level nose passes a context instead of a test case.
    if isinstance(test, nose.suite.ContextSuite):
        name = test.context.__name__
    else:
        name = str(test)
    if ' ' in name:
        name = name.split(' ')[1]

    return sanitize_filename(name)

def get_stdout():
    if isinstance(sys.stdout, p_StringO):
        return sys.stdout.getvalue()
    return None

class OutputSave(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.testname = None

    def add_options(self, parser, env=os.environ):
        env_opt = 'NOSE_WITH_%s' % self.name.upper()
        env_opt.replace('-', '_')
        parser.add_option("--with-%s" % self.name,
                          action="store_true",
                          dest=self.enableOpt,
                          default=env.get(env_opt),
                          help="Enable plugin %s: %s [%s]" %
                          (self.__class__.__name__, self.help(), env_opt))

        parser.add_option('--omit-success-output',
                          action="store_true",
                          dest="omit_success_output",
                          help = 'do not save output from successful tests',
                          default=False)

        parser.add_option('--save-directory',
                          action="store",
                          dest="save_directory",
                          help="save output files to this directory",
                          default='')

    def configure(self, options, config):
        self.conf = config
        config.capture = False

        if hasattr(options, self.enableOpt):
            self.enabled = getattr(options, self.enableOpt)

        if hasattr(options, 'omit_success_output'):
            self.omit_success = getattr(options, 'omit_success_output')

        if hasattr(options, 'save_directory',):
            self.save_directory = getattr(options, 'save_directory')
            self.save_directory = os.path.abspath(self.save_directory)

            try:
                os.makedirs(self.save_directory)
            except OSError:
                pass

    def addError(self, test, err):
        exception_text = traceback.format_exception(*err)
        exception_text = "".join(exception_text)

        capt = get_stdout()
        if capt is None:
            capt = exception_text
        else:
            capt += exception_text

        write_test_output(test, capt, self.save_directory, prefix='error-')

    def addFailure(self, test, err):
        exception_text = traceback.format_exception(*err)
        exception_text = "".join(exception_text)

        capt = get_stdout()
        if capt is None:
            capt = exception_text
        else:
            capt += exception_text

        write_test_output(test, capt, self.save_directory,
                          prefix='failure-')

    def addSuccess(self, test):
        capt = get_stdout()
        if capt is None:
            capt = ""

        if not self.omit_success:
            write_test_output(test, capt, self.save_directory,
                              prefix='success-')
