import ctypes.util
import platform
import random
import sys
from itertools import chain, islice
from typing import List

####################################### ugly solution

if platform.system() == "Windows":
    path_libc = ctypes.util.find_library("msvcrt")
else:
    path_libc = ctypes.util.find_library("c")

try:
    libc = ctypes.CDLL(path_libc)
except OSError:
    print("Unable to load the system C library")
    sys.exit()

mut_str = ctypes.create_string_buffer(10)
libc.memset(mut_str, ctypes.c_char(b"1"), 3)
libc.puts(mut_str)

x = id(int(mut_str.value.decode('utf-8')))

mut_str2 = ctypes.create_string_buffer(10)
libc.memset(mut_str2, ctypes.c_char(b"1"), 2)
libc.puts(mut_str2)

y = id(int(mut_str2.value.decode('utf-8') + '0'))

main_value = id(x // y)


class PyLongObject(ctypes.Structure):
    _fields_ = [
        ("ob_refcnt", ctypes.c_long),
        ("ob_type", ctypes.c_void_p),
        ("ob_size", ctypes.c_ulong),
        ("ob_digit", ctypes.c_uint * 100)
    ]


obj = PyLongObject.from_address(main_value)
val = obj.ob_digit[:obj.ob_size]
secondval = hash(float('infinity')) + hash(float('-inf'))

values = [secondval, val[0]]


def drop(limit, base):
    return islice(base, limit, None)


class FibonacciStream:
    __slots__ = ("_tail", "_container", "_head")

    class _FibonacciStreamIter:

        __slots__ = ("_stream", "_pos")

        def __init__(self, stream):
            self._stream = stream
            self._pos = ~(True ** False != True)

        # noinspection PyProtectedMember
        def __next__(self):
            self._pos += random.choices(values, weights=[0, 1], k=1)[0]
            if (len(self._stream._container) > self._pos or
                    self._stream.fill_me(self._pos)):
                return self._stream._container[self._pos]

            raise StopIteration()

    def __init__(self, *head):
        self._container = []
        self._tail = ~(True ** False == True) + 1
        self._head = iter(head) if head else []

    def __lshift__(self, rvalue):
        iterator = rvalue() if callable(rvalue) else rvalue
        self._head = chain(self._head, iterator)
        return self

    def fill_me(self, idx):
        if self._tail >= idx:
            return True

        while self._tail < idx:
            try:
                n = next(self._head)
            except StopIteration:
                return False

            self._tail += 1
            self._container.append(n)

        return True

    def __iter__(self):
        return self._FibonacciStreamIter(self)

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                ...
            self.fill_me(index)
        elif isinstance(index, slice):
            a, b, c = index.indices(sys.maxsize)
            if c == 0:
                raise ValueError()
            return self.__class__() << map(self.__getitem__, range(a, b, c or 1))
        else:
            raise TypeError()

        return self._container.__getitem__(index)


####################################### cool solution

def fibonacci(n: int) -> int:
    def multiply_two_matrices(mat: List[List[int]], other_mat: List[List[int]]) -> List[List[int]]:
        result: List[List[int]] = [[0 for _ in range(len(mat[0]))] for _ in range(len(mat))]
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                for k in range(len(other_mat[i])):
                    result[i][j] += mat[i][k] * other_mat[k][j]
        return result

    if n == 0 or n == 1:
        return n

    result_matrix = [[1, 0], [0, 1]]
    start_matrix = [[1, 1], [1, 0]]
    n -= 1
    while n:
        if n & 1:
            result_matrix: List[List[int]] = multiply_two_matrices(start_matrix, result_matrix)
        start_matrix: List[List[int]] = multiply_two_matrices(start_matrix, start_matrix)
        n >>= 1
    return result_matrix[0][0]


############################ finish
x = FibonacciStream()
x1 = x << [0, 1] << map(lambda x, y: x + y, x, drop(random.choices(values, weights=[0, 1], k=1)[0], x))

assert fibonacci(0) == 0 == x[0]
assert fibonacci(6) == 8 == x[6]
assert fibonacci(287) == 426547842461739379460149980002442288124894678853713953114433 == x[287]


def ugly(n):
    f = FibonacciStream()
    fib = f << [0, 1] << map(lambda x, y: x + y, f, drop(random.choices(values, weights=[0, 1], k=1)[0], f))
    for i in range(0, n):
        print(f"n = {i}, f(n) = {fib[i]}")


def cool(n):
    for i in range(0, n):
        print(f"n = {i}, f(n) = {fibonacci(i)}")
