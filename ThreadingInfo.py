# I'm not explaining what threads are. It's a simple mechanic used everywhere. But I will talk about some basics and locking threads

# https://docs.python.org/3/library/threading.html
# Under "Thread objects", "Lock objects", and "Using locks, conditions, and semaphores in the with statement"

#--------------------------------#
# How to create and start a thread:

import threading
import time

def functionThread(): # Function for the thread to use
    print("Hello world!")

thread = threading.Thread(target=functionThread) # Creating a Thread class
# Tuples and keyword arguments can be accepted to the function (args & kwargs)

thread.start() # Starts the thread

#--------------------------------#
# Thread locking mechanics:
lock = threading.Lock() # Creating a Lock class

def threadA():
    lock.acquire() # Acquires the lock
    print("threadA is using this lock for 3 seconds")
    time.sleep(3)
    lock.release() # Releases the lock

def threadB():
    lock.acquire(blocking=True, timeout=-1) # Waits until the lock is unlocked to continue
    print("threadB is now using this lock")
    lock.release()

tA = threading.Thread(target=threadA)
tB = threading.Thread(target=threadB)
tA.start()
time.sleep(0.5)
tB.start()


time.sleep(10)
def threadA():
    lock.acquire()
    print("threadA is using this lock for 3 seconds")
    time.sleep(3)
    lock.release()

def threadB():
    while True:
        if lock.acquire(blocking=False): # If the lock is unlocked it acquires the lock, and returns True. Else it returns false and moves on
            print("threadB is now using this lock")
            lock.release()
            break
        else:
            print("threadB: GIVE ME MY LOCK")
            time.sleep(0.5)

tA = threading.Thread(target=threadA)
tB = threading.Thread(target=threadB)
tA.start()
time.sleep(0.5)
tB.start()

# The 'timeout' kwarg means after a period of time, the acquire will return False and move on;
# If it is set to a negative value, no timeout will happen, demonstrated in it's default value '-1';
# It will only work when the 'blocking' kwarg is set to True. Else something bad will happen, but I haven't tested that nor have any intentions to whatsoever

# You can use 'return' and 'sys.exit()' to exit a thread,
# And '_thread.exit()' can also be used when using the '_thread' library. It is the exact same as 'sys_exit()'

# Using 'with {lock}:' acquires the lock with the defaults, and as the 'finally:' clause it releases the lock;
# This is safer because it releases the lock no matter what, for example in the event of an Error

def threadC():
    with lock:
        print("I'm using the lock with a 'with' clause")
threading.Thread(target=threadC).start() # You can create a Thread class and start it in the same line


#===============================#


# I'll be using the depreciated '_thread' library for micropython. It's nearly the same as 'threading'
# https://docs.python.org/3.5/library/_thread.html#module-_thread

import _thread

_thread.start_new_thread(lambda: print("Hello world!"), ()) # Start a thread, 'args' is not optional, but 'kwargs' is. Just add empty parentheses to satisfy the parameter
lock = _thread.allocate_lock() # Creating a LockType class

def threadFunction():
    lock.acquire(waitflag=1, timeout=-1) # 'timeout' works the same
    # 'waitflag=1' = 'blocking=True'
    # 'waitflag=0' = 'blocking=False'
    time.sleep(3)
    lock.release() # Works the same

_thread.start_new_thread(threadFunction, ()) # Starts immediately, it does not return anything

# The 'with' clause doesn't exist in the '_thread' library.
# In micropython, you cannot use the 'timeout' parameter. It will simple ignore it;
# Nor can you use the '_thread.TIMEOUT_MAX' method, it doesn't exist on the micropython _thread library.

lockStatus = lock.locked() # Checks if the lock is acquired - 'True', or released 'False'. Works for both 'threading' and '_thread'
print(lockStatus)
