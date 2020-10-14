# Python modules
import time
import mmap
import sys
import hashlib
import json

# GPIO modules
from gpiozero import DistanceSensor
from time import sleep

# 3rd party modules
import posix_ipc

# Utils for this demo
import sys

import utils

# shared memory
PY_MAJOR_VERSION = sys.version_info[0]
params = utils.read_params()
# Create the shared memory and the semaphore.
memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME_MOVEMENT_SENSOR"], posix_ipc.O_CREAT,
                                size=params["SHM_SIZE"])

# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)

# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap.
memory.close_fd()
# US sensor
us_sensor = {"US-distance": "None", "crashed": "False"}  # the data that will be saved at the posix shared memory
crahed_dist = 5
sensor = DistanceSensor(echo=18, trigger=17)  # declaration of the sensor as a DistanceSensor object

while True:
    # print('Distance: ', sensor.distance * 100)
    us_sensor["US-distance"] = sensor.distance * 100  # getting the distance in cm.

    if us_sensor["US-distance"] <= crahed_dist:  # if the measured distace equal or less than the crahed_dist
        # than the "crahed" flag is raised
        us_sensor["crashed"] = True

    else:
        us_sensor["crashed"] = False

    utils.write_to_memory(mapfile, json.dumps(us_sensor))  # writing the data as a string at the shared memory location
    # sleep(0.1)
