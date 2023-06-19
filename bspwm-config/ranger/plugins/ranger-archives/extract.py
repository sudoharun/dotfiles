import os
import pathlib
from ranger.api.commands import Command
from ranger.core.loader import CommandLoader
from .archives_utils import parse_escape_args, get_decompression_command


class extract(Command):
    def execute(self):
        """Extract copied files to current directory or directory
        specified in a command line
        """
        cwd = self.fm.thisdir
        files = cwd.get_selection()
        cwd = self.fm.thisdir

        if not files:
            return

        def refresh(_):
            _cwd = self.fm.get_directory(cwd.path)
            _cwd.load_content()

        dirname = " ".join(self.line.strip().split()[1:])
        self.fm.copy_buffer.clear()
        self.fm.cut_buffer = False

        for file in files:
            descr = f"Extracting: {os.path.basename(file.path)}"
            command = get_decompression_command(file.path, [], dirname)
            obj = CommandLoader(args=command, descr=descr, read=True)
            obj.signal_bind('after', refresh)
            self.fm.loader.add(obj)


class extract_raw(Command):
    def execute(self):
        """Extract copied files to current directory or directory
        specified in a command line
        """
        cwd = self.fm.thisdir
        files = cwd.get_selection()
        cwd = self.fm.thisdir

        if not files:
            return

        def refresh(_):
            _cwd = self.fm.get_directory(cwd.path)
            _cwd.load_content()

        flags = parse_escape_args(self.line.strip())[1:]
        self.fm.copy_buffer.clear()
        self.fm.cut_buffer = False

        for file in files:
            descr = f"Extracting: {os.path.basename(file.path)}"
            command = get_decompression_command(file.path, flags.copy())
            obj = CommandLoader(args=command, descr=descr, read=True)
            obj.signal_bind('after', refresh)
            self.fm.loader.add(obj)


class extract_to_dirs(Command):
    def execute(self):
        """Extract copied files to a subdirectories"""
        cwd = self.fm.thisdir
        files = cwd.get_selection()
        cwd = self.fm.thisdir

        if not files:
            return

        def refresh(_):
            _cwd = self.fm.get_directory(cwd.path)
            _cwd.load_content()

        flags = parse_escape_args(self.line.strip())[1:]
        self.fm.copy_buffer.clear()
        self.fm.cut_buffer = False

        for file in files:
            descr = f"Extracting: {os.path.basename(file.path)}"
            dirname = pathlib.Path(file.path).stem
            command = get_decompression_command(file.path, flags.copy(), dirname)
            obj = CommandLoader(args=command, descr=descr, read=True)
            obj.signal_bind('after', refresh)
            self.fm.loader.add(obj)
