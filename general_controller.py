from services import utils
from threading import Thread, Event
from time import sleep

from services.utils import buzzers

global onStopEvent
onStopEvent = Event()


def on_service_is_down(name_key):
    print(name_key + " is down")


buzzers_prev_state = False
t = Thread(target=buzzers)

def on_service_is_up(name_key, data):
    if name_key == 'SHARED_MEMORY_NAME_MOVEMENT_SENSOR':
        if data['crashed'] and not t.is_alive():
            t.start()
        else:
            onStopEvent.is_set()
            t.join()
    if name_key == 'SHARED_MEMORY_NAME_ACOUSTIC_SENSOR':
        if data['Falling']and not t.is_alive():
            t.start()
        else:
            onStopEvent.is_set()
            t.join()
    if name_key == 'SHARED_MEMORY_NAME_DEPTH_CAMERA':
        print("DEPTH_CAMERA")
