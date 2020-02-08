SILENT = 0
ERROR = 1
WARNING = 2
INFO = 3
VERBOSE = 4

log_level = INFO
use_color = True
multiline_shift = 2

def _attach_suffix_to_newlines(msg, suffix):
    return msg.replace("\n", "\n" + suffix)

def error(msg):
    if log_level >= ERROR:
        if use_color:
            print("\033[91m", end="")
        print("[x]", _attach_suffix_to_newlines(msg, "[x] " + " " * multiline_shift), end="\033[0m\n")

def throw(err):
    try:
        raise err.__class__()
    finally:
        error(str(err))

def warn(msg):
    if log_level >= WARNING:
        if use_color:
            print("\033[93m", end="")
        print("[!]", _attach_suffix_to_newlines(msg, "[!] " + " " * multiline_shift), end="\033[0m\n")

def info(msg):
    if log_level >= INFO:
        print("[*]", _attach_suffix_to_newlines(msg, "[*] " + " " * multiline_shift))

def verbose(msg):
    if log_level == VERBOSE:
        info(msg)

def ll(info, verbose):
    if info is None and verbose is None:
        return
    if log_level <= INFO:
        print("[*]", _attach_suffix_to_newlines(info, "[*] " + " " * multiline_shift))
    else:
        print("[*]", _attach_suffix_to_newlines(verbose, "[*] " + " " * multiline_shift))
