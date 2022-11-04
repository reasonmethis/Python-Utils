import time
from threading import Timer
from concurrent import futures

#https://stackoverflow.com/questions/12435211/threading-timer-repeat-function-every-n-seconds
class RepeatTimer(Timer):
    '''Usage: 
    timer = RepeatTimer(1, print, 'this message will be printed every 1sec until timer is canceled')
    timer.start()
    time.sleep(5)
    timer.cancel()'''
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

#https://stackoverflow.com/questions/54011552/any-concurrent-futures-timeout-that-actually-works
def run_with_threads_nokill(tmout, func, *args, **kwargs):
    exectr = futures.ThreadPoolExecutor() 
    #can't use the with statement because then shutdown will wait for all futures to finish
    try:
        future = exectr.submit(func, *args, **kwargs)
        res = future.result(timeout=tmout) #will raise TimeoutError if timed out
        return res
    finally:
        exectr.shutdown(wait=False)

def run_with_processes_nokill(tmout, func, *args, **kwargs):
    exectr = futures.ProcessPoolExecutor() 
    #can't use the with statement because then shutdown will wait for all futures to finish
    try:
        future = exectr.submit(func, *args, **kwargs)
        res = future.result(timeout=tmout) #will raise TimeoutError if timed out
        return res
    finally:
        exectr.shutdown(wait=False)

class Test:
    def __init__(self) -> None:
        self.var = 1

    def testfunc(self, a, b):
        print('Will sleep a little')
        time.sleep(15)
        print('Done sleeping, returning')
        self.var = a + b
        return a + b

if __name__ == '__main__':
    test = Test()
    res = None
    timeout = 2
    try:
        res = run_with_processes_nokill(timeout, test.testfunc, a=2, b=3)
    except futures.TimeoutError:
        print('Timout reached')
    print(f'{res=} {test.var=}')