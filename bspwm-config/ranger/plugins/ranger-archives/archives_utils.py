from shlex import split, quote
from shutil import which
from re import search
from typing import Union, Tuple, List
from os import makedirs


def parse_escape_args(args: str = "") -> List[str]:
    """Parses and escapes arguments"""
    return list(map(quote, split(args)))


def find_binaries(
        binaries: List[str]) -> Union[Tuple[str, str], Tuple[None, None]]:
    """Finds archivers binaries in PATH"""
    res = list(filter(
        lambda x: x[1] is not None,
        zip(binaries, map(which, binaries))))
    return res[0] if res else (None, None)


def get_compression_command(
        archive_name: str,
        flags: List[str],
        files: List[str]) -> List[str]:
    """Returns compression command"""
    if search(r"\.(tar\.|t)bz[2]*$", archive_name) is not None:
        # Matches:
        # .tar.bz2
        # .tar.bz
        # .tbz2
        # .tbz
        bins = ["pbzip2", "lbzip2", "bzip2"]
        binary, binary_path = find_binaries(bins)

        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.bz[2]*$", archive_name) is not None:
        # Matches:
        # .bz2
        # .bz
        bins = ["pbzip2", "lbzip2", "bzip2"]
        binary, binary_path = find_binaries(bins)
        flags_mod = flags + ['-k']

        if binary:
            command = [binary_path, *flags_mod, *files]
            return command

    elif search(r"\.(tar\.(gz|z)|t(g|a)z)$", archive_name) is not None:
        # Matches:
        # .tar.gz
        # .tar.z
        # .tgz
        # .taz
        bins = ["pigz", "gzip"]
        binary, binary_path = find_binaries(bins)

        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.g*z$", archive_name) is not None:
        # Matches:
        # .gz
        # .z
        bins = ["pigz", "gzip"]
        binary, binary_path = find_binaries(bins)
        flags_mod = flags + ['-k']

        if binary:
            command = [binary_path, *flags_mod, *files]
            return command

    elif search(r"\.tar\.lz4$", archive_name) is not None:
        bins = ["lz4"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.lz4$", archive_name) is not None:
        bins = ["lz4"]
        binary, binary_path = find_binaries(bins)
        if binary:
            if len(files) > 1:
                flags_mod = flags + ['-m']
                # multiple files imply automatic output names
                command = [binary_path, *flags_mod, *files]
            else:
                command = [binary_path, *flags, *files, archive_name]
            return command

    elif search(r"\.tar\.lrz$", archive_name) is not None:
        bins = ["lrzip"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.lrz$", archive_name) is not None:
        bins = ["lrzip"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = [binary_path, *flags, *files]
            return command

    elif search(r"\.tar\.lz$", archive_name) is not None:
        bins = ["plzip", "lzip"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.lz$", archive_name) is not None:
        bins = ["plzip", "lzip"]
        binary, binary_path = find_binaries(bins)
        if binary:
            flags_mod = flags + ['-k']
            command = [binary_path, *flags_mod, *files]
            return command

    elif search(r"\.(tar\.lzop|tzo)$", archive_name) is not None:
        # Matches:
        # .tar.lzop
        # .tzo
        bins = ["lzop"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.lzop$", archive_name) is not None:
        # Matches:
        # .lzop
        bins = ["lzop"]
        binary, binary_path = find_binaries(bins)
        if binary:
            if len(files) > 1:
                command = [binary_path, *flags, *files]
            else:
                command = [binary_path, *flags, '-o', archive_name, *files]
            return command

    elif search(r"\.(tar\.(xz|lzma)|t(xz|lz))$", archive_name) is not None:
        # Matches:
        # .tar.xz
        # .tar.lzma
        # .txz
        # .tlz
        bins = ["pixz", "xz"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.(xz|lzma)$", archive_name) is not None:
        # Matches:
        # .xz
        # .lzma
        bins = ["pixz", "xz"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = [binary_path, *flags, *files]
            return command

    elif search(r"\.tar\.zst$", archive_name) is not None:
        bins = ["zstd"]
        binary, binary_path = find_binaries(bins)
        if binary:
            command = ["tar", "-cf", archive_name, "--use-compress-program", binary_path, *flags, *files]
            return command

    elif search(r"\.7z$", archive_name) is not None:
        bins = ["7z"]
        binary, binary_path = find_binaries(bins)
        flags_mod = flags + ["-r"]  # enable recursion into subdirs
        if binary:
            command = [binary, "a", *flags_mod, archive_name, *files]
            return command

    elif search(r"\.rar$", archive_name) is not None:
        bins = ["rar"]
        binary, binary_path = find_binaries(bins)
        flags_mod = flags
        if binary:
            command = [binary_path, "a", *flags_mod, archive_name, *files]
            return command

    elif search(r"\.zip$", archive_name) is not None:
        bins = ["zip", "7z"]
        binary, binary_path = find_binaries(bins)
        flags_mod = flags + ["-r"]  # enable recursion into subdirs

        if binary == 'zip':
            command = [binary_path, *flags_mod, archive_name, *files]
            return command
        elif binary == '7z':
            command = [binary_path, "a", *flags_mod, archive_name, *files]
            return command

    elif search(r"\.zpaq$", archive_name) is not None:
        bins = ["zpaq"]
        binary, binary_path = find_binaries(bins)

        if binary:
            command = [binary_path, "a", archive_name, *files, *flags]
            return command

    elif search(r"\.l(zh|ha)$", archive_name) is not None:
        # Matches:
        # .lzh
        # .lha
        bins = ["lha"]
        binary, binary_path = find_binaries(bins)

        if binary:
            command = [binary_path, "c", *flags, archive_name, *files]
            return command

    # elif search(r"\.cpio$", archive_name) is not None:
    #     bins = ["cpio"]

    elif search(r"\.tar$", archive_name) is not None:
        bins = ["tar", "7z"]
        binary, binary_path = find_binaries(bins)

        if binary == "tar":
            command = [binary_path, "-cf", *flags, archive_name, *files]
            return command
        elif binary == "7z":
            command = [binary_path, "a", *flags, archive_name, *files]
            return command

    fallback_command = ["zip", "-r", f"{archive_name}.zip"] + files
    return fallback_command


def get_decompression_command(
        archive_name: str,
        flags: list,
        to_dir: str = None) -> List[str]:
    """Returns decompression command"""
    tar_full = r"\.tar\.(bz2*|g*z|lz(4|ma)|lr*z|lzop|xz|zst)$"
    tar_short = r"\.t(a|b|g|l|x)z2*"

    if to_dir:
        makedirs(to_dir, exist_ok=True)

    if search(tar_full, archive_name) is not None or\
            search(tar_short, archive_name) is not None:
        # Matches all supported tarballs
        bins = ["tar"]
        binary, binary_path = find_binaries(bins)

        if binary:
            if to_dir:
                flags += ['-C', to_dir]
            command = [binary_path, "-xf", archive_name, *flags]
            return command

    elif search(r"\.7z$", archive_name) is not None:
        bins = ["7z"]
        binary, binary_path = find_binaries(bins)
        if binary:
            if to_dir:
                flags += ['-o{}'.format(to_dir)]
            command = [binary, "x", *flags, archive_name]
            return command

    elif search(r"\.rar$", archive_name) is not None:
        bins = ["7z", "unrar", "rar"]
        binary, binary_path = find_binaries(bins)

        if binary == 'rar' or binary == 'unrar':
            command = [binary_path, "x", *flags, archive_name]
            if to_dir:
                command += [to_dir]
            return command
        elif binary == '7z':
            if to_dir:
                flags += ['-o{}'.format(to_dir)]
            command = [binary_path, "x", *flags, archive_name]
            return command

    elif search(r"\.zip$", archive_name) is not None:
        bins = ["7z", "unzip"]
        binary, binary_path = find_binaries(bins)

        if binary == 'unzip':
            command = [binary_path, *flags, archive_name]
            if to_dir:
                command += ['-d', to_dir]
            return command
        elif binary == '7z':
            if to_dir:
                flags += ['-o{}'.format(to_dir)]
            command = [binary_path, "x", *flags, archive_name]
            return command

    elif search(r"\.zpaq$", archive_name) is not None:
        bins = ["zpaq"]
        binary, binary_path = find_binaries(bins)

        if binary:
            command = [binary_path, "x", archive_name, *flags]
            return command

    elif search(r"\.l(zh|ha)$", archive_name) is not None:
        # Matches:
        # .lzh
        # .lha
        bins = ["lha"]
        binary, binary_path = find_binaries(bins)

        if binary:
            if to_dir:
                flags += ['w={}'.format(to_dir)]
            command = [binary_path, "x", *flags, archive_name]
            return command

    elif search(r"\.tar$", archive_name) is not None:
        bins = ["tar", "7z"]
        binary, binary_path = find_binaries(bins)

        if binary == "tar":
            if to_dir:
                flags += ['-C', to_dir]
            command = [binary_path, "-xf", *flags, archive_name]
            return command
        elif binary == "7z":
            if to_dir:
                flags += ['-o{}'.format(to_dir)]
            command = [binary_path, "x", *flags, archive_name]
            return command

    elif search(r"\.deb$", archive_name) is not None:
        # Matches:
        # .deb
        bins = ["ar"]
        binary, binary_path = find_binaries(bins)

        if binary:
            if to_dir:
                flags += ['--output={}'.format(to_dir)]
            command = [binary_path, "xv", *flags, archive_name]
            return command

    fallback_command = ["7z", "x", archive_name] +\
        (['-o{}'.format(to_dir)] if to_dir else [])
    return fallback_command
