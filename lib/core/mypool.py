import threading
import types
from multiprocessing import Process, Manager, Queue, util
import os

INIT = "INIT"
RUN = "RUN"
CLOSE = "CLOSE"
TERMINATE = "TERMINATE"


class Pool:
    def __init__(self, processes=None, initializer=None, initargs=()):
        self._taskqueue = Queue(maxsize=80)
        self._pool = []
        if processes is None:
            processes = os.cpu_count() or 1
        if processes < 1:
            raise ValueError("Number of processes must be at least 1")
        if initializer is not None and not callable(initializer):
            raise TypeError('initializer must be a callable')

        self._processes = processes
        self._state = CLOSE

        for _ in range(self._processes):
            p = Process(target=self._handle_tasks())
            self._pool.append(p)
            p.start()

    def apply_async(self, func, args=(), kwds=None, callback=None):
        if kwds is None:
            kwds = {}
        print(1)
        self._state = RUN
        if self._state != CLOSE:
            self._taskqueue.put([(func, args, kwds, callback)], None)

    def _handle_tasks(self):
        while True:
            try:
                func, args, kwds, callback = self._taskqueue.get(block=True, timeout=2)[0]
                print(func)
                result = func(*args, **kwds)
                if callback is not None:
                    callback(result)
            except Exception:
                print(self._state)
                if self._state == CLOSE:
                    break

    def close(self):
        util.debug('closing pool')
        if self._state == RUN:
            self._state = CLOSE

    def join(self):
        util.debug('joining pool')
        if self._state == RUN:
            raise ValueError("Pool is still running")
        elif self._state not in (CLOSE, TERMINATE):
            raise ValueError("In unknown state")
        for p in self._pool:
            p.join()


class ApplyResult(object):

    def __init__(self, pool, callback, error_callback):
        self._pool = pool
        self._event = threading.Event()
        self._job = next(job_counter)
        self._cache = pool._cache
        self._callback = callback
        self._error_callback = error_callback
        self._cache[self._job] = self

    def ready(self):
        return self._event.is_set()

    def successful(self):
        if not self.ready():
            raise ValueError("{0!r} not ready".format(self))
        return self._success

    def wait(self, timeout=None):
        self._event.wait(timeout)

    def get(self, timeout=None):
        self.wait(timeout)
        if not self.ready():
            raise TimeoutError
        if self._success:
            return self._value
        else:
            raise self._value

    def _set(self, i, obj):
        self._success, self._value = obj
        if self._callback and self._success:
            self._callback(self._value)
        if self._error_callback and not self._success:
            self._error_callback(self._value)
        self._event.set()
        del self._cache[self._job]
        self._pool = None

    __class_getitem__ = classmethod(types.GenericAlias)


AsyncResult = ApplyResult  # create alias -- see #17805
