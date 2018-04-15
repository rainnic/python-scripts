import pygame, sys
import subprocess
import schedule
import time
from time import localtime, strftime

# SETTINGS:
size = (1920, 1080)   # size of your screen
check_audio = 'OFF'   # with 'ON' the script doesn't turn off the screen if your audio card is busy
duration = 1200       # the time interval in seconds

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def turnoff():
    print("")
    proc = subprocess.Popen('pacmd list-sink-inputs | grep -c "state: RUNNING"', shell="True", stdout=subprocess.PIPE)
    output = proc.stdout.read()
    print (output)
    if ((output == b'0\n') & (check_audio == 'ON')) | (check_audio != 'ON'):
         print (strftime("%H:%M:%S", localtime()) + "--> OKAY!!")
         pygame.init()
         screen = pygame.mouse.set_visible(0)
         screen = pygame.display.set_mode((size),pygame.FULLSCREEN)
         time.sleep( 20 )
         pygame.mixer.music.load('notification.mp3')
         pygame.mixer.music.play(0)
         while pygame.mixer.music.get_busy(): 
             pygame.time.Clock().tick(10)
         pygame.quit()       
    else:
         print (strftime("%H:%M:%S", localtime()) + "--> NO WAY!!")

schedule.every(duration).seconds.do(turnoff)
print (strftime("%H:%M:%S", localtime()) + "--> Starting...")

while 1:
    schedule.run_pending()
    time.sleep(1)
