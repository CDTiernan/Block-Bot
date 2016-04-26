#!python3
import threading
from queue import Queue
import time


class multi():

    def __init__(self):
        # lock to serialize console output
        self.lock = threading.Lock()
        self.q = Queue()
        self.num_worker_threads = 20

    def do_work(self, item):
        time.sleep(.1) # pretend to do some lengthy work.
        # Make sure the whole print completes or threads can mix up output in one line.
        with self.lock:
            print(threading.current_thread().name,item)

    # The worker thread pulls an item from the queue and processes it
    def worker(self):
        while True:
            item = self.q.get()
            self.do_work(item)
            self.q.task_done()

    def run(self):
        t0 = time.time()
        # Create the queue and thread pool.
        for i in range(self.num_worker_threads):
             t = threading.Thread(target=self.worker)
             t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
             t.start()

        # stuff work items on the queue (in this case, just a number).
        start = time.perf_counter()
        for item in range(20):
            self.q.put(item)

        self.q.join()       # block until all tasks are done
        print(time.time()-t0)

if __name__ == '__main__':
    multi().run()

# "Work" took .1 seconds per task.
# 20 tasks serially would be 2 seconds.
# With 4 threads should be about .5 seconds (contrived because non-CPU intensive "work")
