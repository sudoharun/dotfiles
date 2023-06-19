#!/usr/bin/python3
# coding: utf-8
# License: The MIT License
# Author: Alexander Lutsai <sl_ru@live.com>
# Year: 2021
# Description: This launches script that draws menu to choose, mount and unmount drives from ranger file manager

from ranger.api.commands import Command
import tempfile
import os


class mount(Command):
    """:mount

    Show menu to mount and unmount
    """
    def execute(self):
        """ Show menu to mount and unmount """
        (f, p) = tempfile.mkstemp()
        os.close(f)
        self.fm.execute_console(
            f"shell python3 {os.path.dirname(os.path.realpath(__file__))}/menu.py {p}"
        )
        with open(p, 'r') as f:
            d = f.readline()
            if os.path.exists(d):
                self.fm.cd(d)
        os.remove(p)
