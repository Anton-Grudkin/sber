import time
import argparse
from multiprocessing import Process
import logging

logging.basicConfig(level=logging.INFO, filename='finder.log',
                    format='%(asctime)s :: %(levelname)s - %(message)s')

def time_profile(fn):

    def with_time_profiling(*args, **kwargs):
        start_time = time.time()
        res = fn(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.info(f"Function '{fn.__name__}' was executed in {elapsed_time:.3f} s")
        return res

    return with_time_profiling

class time_profile_with_timeout(object):

    def __init__(self, timeout = 5.0):
        self.__timeout = timeout

    def __call__(self, fn):
        def wrapped_fn(*args, **kwargs):
            action_process = Process(target=fn, args=args, kwargs=kwargs)
            start_time = time.time()
            action_process.start()
            action_process.join(timeout=self.__timeout)
            if action_process.is_alive():
                action_process.terminate()
                logging.warning(f"Execution of '{fn.__name__}' was terminated due to exceeding {self.__timeout:.1f} s time quota")
            else:
                elapsed_time = time.time() - start_time
                logging.info(f"Function '{fn.__name__}' was executed in {elapsed_time:.3f} s")
            return 
        return wrapped_fn

@time_profile # example of simple time profiling decorator usage
def get_wrapped_finder(timeout):
    @time_profile_with_timeout(timeout = timeout) # example of time profiling decorator with timeout usage
    def get_nth_prime(n):
        if n < 1:
            print("\tIndex should be positive")
            return None
        primes = [2]
        current = primes[-1]
        while len(primes) < n:
            current += 1
            for p in primes:
                if not current % p:
                    break
            else:
                primes.append(current)
        print(f"\t{n}-th prime number is {primes[-1]}")
        return primes[-1]
    return get_nth_prime

parser = argparse.ArgumentParser(description='Finds n-th prime number.')
parser.add_argument('-n', type=int, help='prime number index')
parser.add_argument('-t', type=float, help='timeout in seconds', default=5.0)

args = parser.parse_args()
p = get_wrapped_finder(args.t)(args.n)
