from services import utils


def on_service_is_down(name_key):
    print(name_key + " is down")


def on_service_is_up(name_key, data):
    if name_key == 'SHARED_MEMORY_NAME_MOVEMENT_SENSOR':
        print("MOVEMENT_SENSOR: " + data['US-distance'])
        if data['crashed']:
            utils.buzzers(True)
        else:
            utils.buzzers(False)
    if name_key == 'SHARED_MEMORY_NAME_ACOUSTIC_SENSOR':
        print("ACOUSTIC_SENSOR")
        if data['Falling']:
            utils.buzzers(True)
        else:
            utils.buzzers(False)
    if name_key == 'SHARED_MEMORY_NAME_DEPTH_CAMERA':
        print("DEPTH_CAMERA")
