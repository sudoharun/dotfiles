# ranger-archives

This is a plugin for [ranger](https://ranger.github.io) file manager that makes it much easier to compress and extract archives. It depends on archivers/compression programs such as `tar`, `zip`, `7z`, etc. It also supports and prioritizes parallelized versions of compression programs (like `pbzip2`, `pigz`, `pixz`, etc).

[![asciicast](https://asciinema.org/a/ii764wsN8rWZfMCwVlnJAWcPM.svg)](https://asciinema.org/a/ii764wsN8rWZfMCwVlnJAWcPM)

## Installation

Clone this repo into ranger plugins folder. In Linux, it is typically located here: `~/.config/ranger/plugins`.

```bash
cd ~/.config/ranger/plugins
git clone https://github.com/maximtrp/ranger-archives.git
```

## Usage

The following commands are available:

* `:extract [DIRECTORY]`: extracting files to a current or specified directory (optional).
* `:extract_raw [FLAGS]`: extracting files with specific flags (optional).
* `:extract_to_dirs [FLAGS]`: extracting each archive to a separate directory. E.g.: `1.zip` to dir `1`, `2.zip` to dir `2`, etc.
* `:compress [FLAGS] [FILENAME.EXT]`: compressing selected/marked files/directories to an archive. If an archive filename is not specified, it will be named after a parent dir.

## Examples

### Extraction

#### Basic

Select an archive and type:

```
:extract some_dir
```

Or even just:

```
:extract
```

#### Using flags

This is an example of extracting a zip archive to a directory `dirname` and escaping all non-ASCII Unicode chars:

```
:extract_raw -U -d dirname
```

### Compression

#### Basic

Select a file or a folder (or multiple files and folder) in *ranger* and enter:

```
:compress files.zip
```

or (use quotation marks with filenames containing spaces)

```
:compress "my important files.zip"
```

#### Using flags 

`zip` archiver provides a flag for better compression ratio `-9` (just like `gzip` and many others).
We can just add it before an archive filename:

```
:compress -9 file.zip
```

The other flags can be used likewise.

## Shortcuts

You can also add these lines to `~/.config/ranger/rc.conf` to use these keyboard shortcuts (`ec`, `ex`):

```
map ex extract
map ec compress
```
