#pythom modules
import time
import random
import json
import mmap
import sys
import hashlib
# 3rd party modules
import posix_ipc
# Utils for this demo
import utils

PY_MAJOR_VERSION = sys.version_info[0]
params = utils.read_params()
fake_content = {"name":"None" ,"type":"None" ,"distance": 43 ,"size": 12} 

# Create the shared memory and the semaphore.
memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME_DEPTH_CAMERA"], posix_ipc.O_CREAT,
                                size=params["SHM_SIZE"])
# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)
# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap.
memory.close_fd()

while True:
    fake_distance = random.randint(0,120)
    fake_size = random.randint(0,120)
    fake_content['distance'] = fake_distance
    fake_content['size'] = fake_size
    utils.write_to_memory(mapfile, json.dumps(fake_content))#writing the data as a string at the shared memory location
    #time.sleep(1)