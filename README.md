gedit-statusbar-wordcount-plugin
======================

Hard forked from: --> https://github.com/footley/gedit-wordcount-plugin and made updates and improvements.

A gedit plugin which adds a label to the status bar with the active document's word and character count, where a word is defined as `r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*"`.

Installation
------------

1. Create folder `~/.local/share/gedit/plugins` if it does not exist.
2. Copy `wordcount.plugin` and `wordcount.py` to `~/.local/share/gedit/plugins`
3. Activate it from gedit's plugins dialogue.

## Changes from original

- Character counter
- More accurate regex for word boundaries
- Adds debouncing (throttling) to reduce update frequency on fast edits
- Displays both word count and character count
- Adds multiple `try`/`except` blocks to prevent crashes
- Separates tracking of active document and connection ID
- Proper cleanup of timers and connections on deactivation
- Displays user-visible errors in the status bar on failure

## Licences
gedit status bar word count plugin is made available under a [GPL3
license](https://github.com/cybrkyd/gedit-statusbar-wordcount-plugin/blob/main/LICENSE)
