#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Author:   lambdalisue (lambdalisue@hashnote.net)
# URL:      http://hashnote.net/
# License:  MIT license
# Created:  2013-03-21
#
import os
import time
import codecs
from watchdog.observers import Observer
from compiler.jinja2_compiler import Jinja2CompileHandler

def watch_and_compile(
        source_directory,
        destination_directory=None,
        context={},
        watch=False,
        verbose=True,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        case_sensitive=False):

    event_handler = Jinja2CompileHandler(
        source_directory=source_directory,
        destination_directory=destination_directory,
        context=context,
        patterns=patterns,
        ignore_patterns=ignore_patterns,
        ignore_directories=ignore_directories,
        case_sensitive=case_sensitive)

    if verbose:
        print
        print "Compile Jinja2 HTML template files"
        print "============================================================="
        print "  IN:  %s" % source_directory
        print "  OUT: %s" % destination_directory
        print "  INCLUDE: %s" % patterns
        print "  EXCLUDE: %s" % ignore_patterns
        print "  CASE SENSITIVE: %s" % case_sensitive
        print

    # create directory
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    # do first compile
    event_handler.compile_path(os.path.abspath(source_directory))

    if watch:
        observer = Observer()
        observer.schedule(
            event_handler,
            path=event_handler.source_directory,
            recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def main():
    if os.path.exists('boil.yaml'):
        # Load settings from Yaml
        import yaml
        args = yaml.load(codecs.open('boil.yaml', 'rb', 'utf-8').read())
        def setdef(name, value):
            if name not in args:
                args[name] = value
        setdef('source_directory', '.')
        setdef('destination_directory', 'www')
        setdef('verbose', True)
        setdef('patterns', None)
        setdef('ignore_patterns', None)
        setdef('ignore_directories', False)
        setdef('case_sensitive', False)
        setdef('context', {})
        setdef('watch', False)
    else:
        import argparse
        parser = argparse.ArgumentParser(
            description="Compile Jinja2 HTML templates.")
        parser.add_argument('source_directory', default=".",
                help="a source directory")
        parser.add_argument('destination_directory', default="www",
                help="a destination directory")
        parser.add_argument('-q', '--quite', default=True, action="store_false",
                dest="verbose",
                help="do not print")
        parser.add_argument('-p', '--patterns', nargs="*",
                help="a list of filename patterns which will be included")
        parser.add_argument('-i', '--ignore-patterns', metavar="PATTERNS", nargs="*",
                help="a list of filename patterns which will be excluded")
        parser.add_argument('--ignore-directories', type=bool, default=False,
                help="`True` if directories should be ignored; `False` otherwise")
        parser.add_argument('--case-sensitive', type=bool, default=False,
                help="`True` if path name should be matched sensitive to case; "
                    "`False` otherwise")
        parser.add_argument('--context', nargs="*", default={},
                help="KEY=VALUE type contexts which will be used in template")
        parser.add_argument('-w', '--watch', default=False, action="store_true",
                help="watch file changes")

        args = parser.parse_args()
        args = args.__dict__

        import yaml
        data = yaml.safe_dump(args, encoding='utf-8', allow_unicode=True)
        with codecs.open('boil.yaml', 'wb', 'utf-8') as f:
            f.write(data)

    watch_and_compile(**args)

if __name__ == '__main__':
    main()
