# Python modules
import time
import mmap
import sys
import schedule
import time
import hashlib

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils

SHARED_MEMORY_PREFIX = "SHARED_MEMORY"
SCHEDULE_INTERVAL = 0.1
PY_MAJOR_VERSION = sys.version_info[0]
params = utils.read_params()


def consume_job(shared_memory_name_key):
    print("I'm working..." + shared_memory_name_key)
    # Create the shared memory and the semaphore.
    memory = posix_ipc.SharedMemory(params[shared_memory_name_key])

    # MMap the shared memory
    mapfile = mmap.mmap(memory.fd, memory.size)

    # Once I've mmapped the file descriptor, I can close it without
    # interfering with the mmap.
    memory.close_fd()

    s = utils.read_from_memory(mapfile)
    print(s)


shared_memory_keys = utils.prefix_search(params, SHARED_MEMORY_PREFIX)

for name_key in shared_memory_keys:
    print(name_key)
    schedule.every(SCHEDULE_INTERVAL).seconds.do(consume_job, name_key)

while True:
    schedule.run_pending()
    time.sleep(SCHEDULE_INTERVAL)
