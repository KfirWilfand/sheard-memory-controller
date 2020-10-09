#pythom modules
import time
import board
import busio
import adafruit_adxl34x

import mmap
import sys
import hashlib
# 3rd party modules
import posix_ipc
# Utils for this demo
import utils

PY_MAJOR_VERSION = sys.version_info[0]
params = utils.read_params()
adxl = {"X":None ,"Y":None, "Z":None, "Falling":False} #the data that will be saved at the posix shared memory

# Create the shared memory and the semaphore.
memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME_ACOUSTIC_SENSOR"], posix_ipc.O_CREAT,
                                size=params["SHM_SIZE"])
# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)
# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap.
memory.close_fd()

#accelometer initialization
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_freefall_detection(threshold=10, time=10)

while True:
    acceleration = accelerometer.acceleration #getting data from the accelometer
    adxl["X"] = acceleration[0]
    adxl["Y"] = acceleration[1]
    adxl["Z"] = acceleration[2]
    adxl["Falling"] = accelerometer.events["freefall"] #event for free falling, true when adxl sense free fall
    utils.write_to_memory(mapfile, str(adxl))#writing the data as a string at the shared memory location
    #time.sleep(1)