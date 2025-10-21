import tracemalloc
from timeit import timeit


ITER_MEM  = 100
ITER_TIME = 1000


def func_1():
    pass


def func_2():
    pass


def measure(func):
    bits = 0
    for i in range(ITER_MEM):
        tracemalloc.reset_peak()
        tracemalloc.start()
        func()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        bits += peak
    return int(bits / ITER_MEM)


def print_results(i, b, t):
    kb = b / 1024
    mb = kb / 1024
    gb = mb / 1024
    print(f"| {i:>10} | {int(b):>10,} | {kb:>10,.3f} | {mb:>10.3f} | {gb:>10.6f} | {t:>10,.6f} | {ITER_TIME:>10,} |")


M1 = measure(func_1)
M2 = measure(func_2)
T1 = timeit(func_1, number=ITER_TIME)
T2 = timeit(func_2, number=ITER_TIME)


print(f"|{'-'*90}|")
print(f"| {'Function':^10} | {'Bytes':^10} | {'KB':^10} | {'MB':^10} | {'GB':^10} | {'Time':^10} | {'Iterations':^10} |")
print(f"|{'-'*90}|")
print_results(i=1, b=M1, t=T1)
print_results(i=2, b=M2, t=T2)
