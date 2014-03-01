ba-server
=========

A Python telnet server for displaying ASCII animation.

* [Homepage (Chinese Only)](http://www.sshz.org/projects/general/baserver/)

You can use `telnet kuroneko.nekotachi.sshz.org` to test it out. Demo video is at [here](http://www.bilibili.tv/video/av364018/).

## How to Write Plugins?

1. Create a new .py file including the following attributes: `line` for number of lines on screen, `col` for number of characters in each line, `author` for any information to be displayed when user chooses it, `frame` for the framerate (frames/second) and `data` being a list of all the frames.
2. `data` in plugins can be compressed using `tools/ba_data_convert.py`. Put the .py file for the new plugin in the same folder and rename it as `ba_data.py`. Run `ba_data_convert.py` and it will write a compressed list `data` to stdout.
3. Put the new .py file in the folder `plugins` and add it to `plugin_list` and `plugin_code` in `plugins/__init__.py`, being respectively the display name and name of .py file of the plugin.

It is suggested to compile the plugins to .pyc before deploying to the server to reduce file size. The .pyc files included in this repo is compiled using Python 2.7.6.