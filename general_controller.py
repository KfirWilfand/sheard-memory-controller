from services import utils
from threading import Thread, Event
from time import sleep

from services import utils
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

global onStopEvent
onStopEvent = Event()


def buzzers():
    buzzer = TonalBuzzer(15)

    while True:
        buzzer.play("A3")
        time.sleep(1)
        if onStopEvent.is_set():
            buzzer.stop()
            break


def on_service_is_down(name_key):
    print(name_key + " is down")


buzzers_prev_state = False
t = Thread(target=buzzers)

def on_service_is_up(name_key, data):
    if name_key == 'SHARED_MEMORY_NAME_MOVEMENT_SENSOR':
        if data['crashed'] and t.is_alive(): 
            buzzers()
    if name_key == 'SHARED_MEMORY_NAME_ACOUSTIC_SENSOR':
        if data['Falling'] and t.is_alive():
            buzzers()
           
    if name_key == 'SHARED_MEMORY_NAME_DEPTH_CAMERA':
        if data['distance'] < 40:
            buzzers()
