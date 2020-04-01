# pckr
A tool for picking images.

I found a directory of photos on my laptop and wanted a way to quickly filter out those I didn't want to keep. Doing this with Finder/Preview is very slow so I hacked up a quick web-based tool to do it.

## Running it

```bash
$ git clone https://github.com/markdrayton/pckr
$ cd pckr
$ ./pckr.py /path/to/images/dir
```

## Keys

* left/right arrow: previous/next image
* `d`: mark
* `0`: jump to start
* `e`: jump to end
* `j`: jump to arbitrary image

Marked image names are listed for you to do whatever you please with. If you paste it into a shell watch out for spaces and other special characters!

## Warnings

This is clearly not any kind of production software. It's very hacky and likely very wrong.
