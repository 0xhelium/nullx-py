import sys
import re

class Event:
    pass

class Observable:
    def _init(self):
        if not hasattr(self, "callbacks"):
            self.callbacks = []

    def subscribe(self, callback):
        self._init()
        self.callbacks.append(callback)
    
    def fire(self, **kwargs):
        self._init()
        e = Event()
        for k, v in kwargs.items():
            setattr(e, k, v)
        for cb in self.callbacks:
            cb(self, e)

def printb(b, end=b"\n"):
    return sys.stdout.buffer.write(b + end)

def search(x, fmt, binary_encoding="utf-8"):
    rgfmt = re.sub(r"(?<!\\)%", r".*?", fmt)
    if binary_encoding is not None:
        pattern = re.compile(rgfmt.encode(binary_encoding))
    else:
        pattern = re.compile(rgfmt)
    match = pattern.search(x)
    return None if match is None else match.group(0)

def search_group(x, fmt, binary_encoding="utf-8"):
    rgfmt = re.sub(r"(?<!\\)%", r"(.*?)", fmt)
    if binary_encoding is not None:
        pattern = re.compile(rgfmt.encode(binary_encoding))
    else:
        pattern = re.compile(rgfmt)
    match = pattern.search(x)
    return None if match is None else match.group(1)

import shutil

def clear():
    sys.stdout.write("\n" * shutil.get_terminal_size().columns)
