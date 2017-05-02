from queue import Queue
import threading


class ThreadManager(object):
    def __init__(self, num_of_workers=1):
        self.queue = Queue()
        self._lock = threading.Lock()
        self.num_of_workers = num_of_workers

    def worker(self):
        while True:
            job = self.queue.get()
            # TODO: Process the job
            self.queue.task_done()

    def process_job(self, funct, *args):
        pass

    def start(self):
        for _ in range(self.num_of_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    @staticmethod
    def start_single_thread(funct, args: tuple):
        t = threading.Thread(target=funct, args=args)
        t.daemon = True
        t.start()
        t.join()

    def stop(self):
        pass

    def add_to_queue(self, job):
        self.queue.put(job)
