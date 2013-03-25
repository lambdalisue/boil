#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Author:   lambdalisue (lambdalisue@hashnote.net)
# URL:      http://hashnote.net/
# License:  MIT license
# Created:  2013-03-21
#
import os
import shutil
from pathtools.patterns import match_path
from watchdog.tricks import Trick


class FileCompileHandler(Trick):
    def __init__(self, verbose=True, *args, **kwargs):
        super(FileCompileHandler, self).__init__(*args, **kwargs)
        self.verbose = verbose

    def is_valid(self, path):
        return match_path(path,
                included_patterns=self.patterns,
                excluded_patterns=self.ignore_patterns,
                case_sensitive=self.case_sensitive)

    def output_path(self, path):
        raise NotImplementedError

    def compile_file(self, filename):
        raise NotImplementedError

    def compile_path(self, path):
        if os.path.isdir(path):
            for filename in os.listdir(path):
                self.compile_path(os.path.join(path, filename))
        elif self.is_valid(path):
            self.compile_file(path)

    def on_created(self, event):
        if not event.is_directory:
            self.compile_path(event.src_path)
        else:
            os.mkdir(self.output_path(event.src_path))

    def on_modified(self, event):
        if not event.is_directory:
            self.compile_path(event.src_path)

    def on_moved(self, event):
        self.on_deleted(event)
        self.compile_path(event.dest_path)

    def on_deleted(self, event):
        to_delete_path = self.output_path(event.src_path)
        if event.is_directory:
            shutil.rmtree(to_delete_path)
        else:
            os.remove(to_delete_path)
        if self.verbose:
            print "Deleted: " + to_delete_path

