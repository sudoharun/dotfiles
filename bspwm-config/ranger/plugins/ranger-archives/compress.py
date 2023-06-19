import os.path
from re import search
from ranger.api.commands import Command
from ranger.core.loader import CommandLoader
from .archives_utils import parse_escape_args, get_compression_command


class compress(Command):
    def execute(self):
        """ Compress marked files to current directory """
        cwd = self.fm.thisdir
        marked_files = cwd.get_selection()
        files_num = len(marked_files)

        if not marked_files:
            return

        # Preparing names of archived files
        filenames = [os.path.relpath(f.path, cwd.path) for f in marked_files]

        # Parsing arguments
        flags = parse_escape_args(self.line.strip())[1:]
        archive_name = None

        if flags:
            flags_last = flags.pop()

            if search(r".*?\.\w+", flags_last) is None:
                flags += [flags_last]
            else:
                archive_name = flags_last

        if not archive_name:
            archive_name = f'{os.path.basename(self.fm.thisdir.path)}.zip'

        # Preparing command for archiver
        archive_name = archive_name.strip("'")
        command = get_compression_command(archive_name, flags, filenames)

        # Making description line
        files_num_str = f'{files_num} objects' if files_num > 1 else '1 object'
        descr = f"Compressing {files_num_str} -> {os.path.basename(archive_name)}"

        # Creating archive
        obj = CommandLoader(args=command, descr=descr, read=True)

        def refresh(_):
            _cwd = self.fm.get_directory(cwd.path)
            _cwd.load_content()

        obj.signal_bind('after', refresh)
        self.fm.loader.add(obj)

    def tab(self, tabnum):
        """ Complete with current folder name """

        extension = ['.7z', '.zip', '.tar.gz', '.tar.bz2', '.tar.xz']
        return [
            f'compress {os.path.basename(self.fm.thisdir.path)}{ext}'
            for ext in extension
        ]
