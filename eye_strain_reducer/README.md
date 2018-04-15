A little Python program to respect the 20-20-20 rule and prevent eye strain
===========================================================================

The program turns off the screen of your computer, then turns on it and makes a sound when 20 seconds have passed, with the ability to deactivate the rule if your audio card is busy (useful if you are watching videos).

## Requirements

I wrote it with Python 3.6 and the following packages are required:
-   pygame;
-   sys;
-   subprocess;
-   schedule;
-   time;
-   pacmd.

## Settings:
At the beginning of the file there is three items to adapt the program at your needs:

```python
# SETTINGS:
size = (1920, 1080) # size of your monitor
check_audio = ‘OFF’ # with 'ON' the script doesn't turn off the screen if your audio card is working
duration = 1200 # the time interval in seconds
```

## How it works
Simple execute it from a terminal or create a launcher in this manner:
```bash
python3.6 eye_strain_reducer.py
```
Then it prints in the shell:
*   the time when it starts;
*   the time and the correct action
    * --> OKAY!! (if turns off the screen)
    * --> NO WAY (if check_audio option is ON and if the number of the sink is greater than or equal to 1).

Here is an example:
```
$ python3.6 eye_strain_reducer.py
19:35:11–> Starting…

b’0\\n’
19:55:11–> OKAY!!

b’1\\n’
20:15:34–> NO WAY!!
...
```

More info on my site:
https://rainnic.altervista.org/tag/python
