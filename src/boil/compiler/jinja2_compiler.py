#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Author:   lambdalisue (lambdalisue@hashnote.net)
# URL:      http://hashnote.net/
# License:  MIT license
# Created:  2013-03-21
#
import os
import codecs
from jinja2 import Environment, FileSystemLoader
from boil.compiler.base import FileCompileHandler
from boil import console

def relpath(path, root):
    if path.startswith(root):
        path = path[len(root)+1:]
    return path


class Jinja2CompileHandler(FileCompileHandler):
    def __init__(self,
                 source_directory='.',
                 destination_directory=None,
                 context={},
                 *args, **kwargs):
        super(Jinja2CompileHandler, self).__init__(*args, **kwargs)

        self.source_directory = os.path.abspath(source_directory)
        if destination_directory is not None:
            self.destination_directory = os.path.abspath(destination_directory)
        else:
            self.destination_directory = self.source_directory
        self.context = context
        # create Jinja2 env
        self.env = Environment(
                loader=FileSystemLoader(self.source_directory))

    def is_valid(self, path):
        path = relpath(path, self.source_directory)
        return super(Jinja2CompileHandler, self).is_valid(path)

    def output_path(self, path):
        if self.source_directory == self.destination_directory:
            root, ext = os.path.splitext(self.source_directory)
            return root + ".compiled" + ext
        return path.replace(self.source_directory, self.destination_directory)

    def compile_file(self, path):
        # Jinja2 engine require relative path from root
        src = relpath(path, self.source_directory)
        dst = self.output_path(path)
        try:
            # render HTML template file
            template = self.env.get_template(src)
            rendered = template.render(**self.context)
            # save file
            with codecs.open(dst, 'w', 'utf-8') as f:
                f.write(rendered)
            if self.verbose:
                print console.GREEN, "[HTML] Compile: ", console.CLEAR,
                print src, "=>", dst, console.CLEAR
        except e:
            if self.verbose:
                print console.RED, "[HTML] Failed: ", console.CLEAR,
                print src, "=>", dst
                print e



