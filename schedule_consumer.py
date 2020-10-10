# Python modules
import json
import mmap
import sys
import schedule
import time
import traceback

# 3rd party modules
import posix_ipc

# Utils for this demo
from services import utils

import general_controller

SHARED_MEMORY_PREFIX = "SHARED_MEMORY"
SCHEDULE_INTERVAL = 0.1
PY_MAJOR_VERSION = sys.version_info[0]
params = utils.read_params()
SHM_SIZE = params["SHM_SIZE"]


def consume_job(shared_memory_name_keys):
    for name_key in shared_memory_name_keys:
        try:
            # print("try to read... " + name_key)
            # Create the shared memory and the semaphore.
            memory = posix_ipc.SharedMemory(params[name_key], posix_ipc.O_CREAT, size=params["SHM_SIZE"])

            # MMap the shared memory
            mapfile = mmap.mmap(memory.fd, memory.size)

            # Once I've mmapped the file descriptor, I can close it without
            # interfering with the mmap.
            memory.close_fd()
            row_data=utils.read_from_memory(mapfile)
            data = json.loads(row_data)
            general_controller.on_service_is_up(name_key, data)
        except:
            general_controller.on_service_is_down(name_key)
            traceback.print_exc()


shared_memory_keys = utils.prefix_search(params, SHARED_MEMORY_PREFIX)
schedule.every(SCHEDULE_INTERVAL).seconds.do(consume_job, shared_memory_keys)

while True:
    schedule.run_pending()
    time.sleep(SCHEDULE_INTERVAL)
