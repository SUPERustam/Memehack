from functools import wraps
import time
import string

def timeit(func):
    """ measure execution time of function"""
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(
            f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def normalization_text(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation))
