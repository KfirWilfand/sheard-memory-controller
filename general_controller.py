import posix_ipc
import utils
import mmap

from schedule_consumer import SHM_SIZE


def on_service_is_down(name_key):
    print(name_key + " is down")
    return None


def on_service_is_up(name_key):
    if name_key == 'SHARED_MEMORY_NAME_MOVEMENT_SENSOR':
        print("MOVEMENT_SENSOR")
    if name_key == 'SHARED_MEMORY_NAME_ACOUSTIC_SENSOR':
        print("ACOUSTIC_SENSOR")
    if name_key == 'SHARED_MEMORY_NAME_DEPTH_CAMERA':
        print("DEPTH_CAMERA")
