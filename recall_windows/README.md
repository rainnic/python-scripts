A Python script to store and load your preferred desktop layout
===============================================================

It takes care of saving in a text file the layout of your favorite applications with their position and size in the correct workspace and uploading them whenever you need them, for example when you start your PC or when you switch from one use to another.

## Requirements

Python 3.6 and the following packages:
- subprocess;
- os;
- sys;
- time.

On Ubuntu and its derivatives 
- wmctrl (sudo apt install wmctrl).

## How it works
Simple execute it from a terminal or create a launcher in this manner:
```bash
recall_windows -read nomefile
recall_windows -run  nomefile
```
- read option serves to save the placements in a file called $HOME/.windowlist or $HOME/.nomefile
- run option serves to load and store the placements saved in $HOME/.windowlist or $HOME/.nomefile

More info on my site:
[Python on Rainnic](https://rainnic.altervista.org/tag/python)
