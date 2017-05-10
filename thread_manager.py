from queue import Queue
import threading


class ThreadManager(object):
    def __init__(self):
        self.queue = Queue()
        self._lock = threading.Lock()

    def worker(self):
        while True:
            job = self.queue.get()
            # TODO: Process the job
            self.queue.task_done()

    def process_job(self, funct, *args):
        pass

    @staticmethod
    def start_single_thread(funct, args: tuple):
        """
        Starts a single thread to process a job, and halts the main thread until the separate thread
        is finished.
        :param funct: A function delegate
        :param args: Arguments of the function
        :return: None
        """
        t = threading.Thread(target=funct, args=args)
        t.daemon = True
        t.start()
        t.join()

    def peek(self):
        """
        Returns the first readily available element in the queue.
        :return: ELement in the queue
        """
        return self.queue.get()
