import sys
import struct
from nullx.utils import printb

FORMAT_SIZES = {
    "b": 8,
    "B": 8,
    "h": 16,
    "H": 16,
    "i": 32,
    "I": 32,
    "q": 64,
    "Q": 64,
    "n": len(struct.pack("n", 0)) * 8,
    "N": len(struct.pack("N", 0)) * 8,
    "P": len(struct.pack("P", 0)) * 8,
    "f": 32,
    "d": 64
}

def bits_to_bytes(bits, f):
    if len(bits) < FORMAT_SIZES[f]:
        bits = [0] * (FORMAT_SIZES[f] - len(bits)) + bits
    b = bytearray()
    for i in range(int(FORMAT_SIZES[f] / 8)):
        tmp = 0
        for j in range(8):
            tmp = (tmp << 1) | bits[i * 8 + j]
        b.append(tmp)
    return bytes(b)

class TypedArray(bytes):
    def __new__(self, f, python_type, *args, endianness=sys.byteorder):
        self.__f = f
        self.endianness = endianness
        init_vals = list(args)
        if len(init_vals) == 1 and (isinstance(init_vals[0], bytes) or isinstance(init_vals[0], list) or isinstance(init_vals[0], tuple)):
            init_vals = list(init_vals[0])
        for i in range(len(init_vals)):
            if isinstance(init_vals[i], python_type):
                init_vals[i] = struct.pack(("<" if self.endianness == "little" else ">") + self.__f, init_vals[i])
        b = bytes()
        for v in init_vals:
            b += v
        return super().__new__(self, b)

    def p(self, end=b"\n"):
        return printb(self, end=end)
    
    def data(self):
        decimals = []
        for i in range(0, super().__len__(), int(FORMAT_SIZES[self.__f] / 8)):
            decimals.append(struct.unpack(("<" if self.endianness == "little" else ">") + self.__f, super().__getitem__(slice(i, i+int(FORMAT_SIZES[self.__f]/8))))[0])
        return decimals
    
    def item(self, i=None):
        if i is None:
            i = 0
        i = i * int(FORMAT_SIZES[self.__f]/8)
        return struct.unpack(("<" if self.endianness == "little" else ">") + self.__f, super().__getitem__(slice(i, i+int(FORMAT_SIZES[self.__f]/8))))[0]
    
    def __len__(self):
        return int(super().__len__() / (FORMAT_SIZES[self.__f] / 8))
    
    def __check_i(self, i):
        if i >= len(self):
            raise IndexError("list index out of range")
        elif i < 0:
            i = len(self) + i
            if i < 0:
                raise IndexError("list index out of range")
        return i
    
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise Exception("Slicing is not supported")
        i = self.__check_i(i)
        return self.item(i)
    
    def cast(self, new_type):
        FORMAT_STRINGS = {
            "int8": "b",
            "uint8": "B",
            "int16": "h",
            "uint16": "H",
            "int32": "i",
            "uint32": "I",
            "int64": "q",
            "uint64": "Q",
            "ssize_t": "n",
            "size_t": "N",
            "void_p": "P",
            "float32": "f",
            "float64": "d"
        }
        if new_type not in FORMAT_STRINGS:
            raise TypeError("new_type must be a type")
        return new_type(struct.unpack(("<" if self.endianness == "little" else ">") + FORMAT_STRINGS[new_type], bytes(self)), endianness=self.endianness)

class Ints(TypedArray):
    def __new__(self, f, *args, endianness=sys.byteorder):
        return super().__new__(self, f, int, *args, endianness=endianness)

class Decimals(TypedArray):
    def __new__(self, f, *args, endianness=sys.byteorder):
        return super().__new__(self, f, float, *args, endianness=endianness)

class int8(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "b", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return int8(*bits_to_bytes(bits, f="b"))

class uint8(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "B", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return uint8(*bits_to_bytes(bits, f="B"))

class int16(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "h", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return int16(*bits_to_bytes(bits, f="h"))

class uint16(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "H", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return uint16(*bits_to_bytes(bits, f="H"))

class int32(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "i", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return int32(*bits_to_bytes(bits, f="i"))

class uint32(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "I", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return uint32(*bits_to_bytes(bits, f="I"))

class int64(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "q", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return int64(*bits_to_bytes(bits, f="q"))

class uint64(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "Q", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return uint64(*bits_to_bytes(bits, f="Q"))

class ssize_t(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "n", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return ssize_t(*bits_to_bytes(bits, f="n"))

class size_t(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "N", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return size_t(*bits_to_bytes(bits, f="N"))

class void_p(Ints):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "P", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return void_p(*bits_to_bytes(bits, f="P"))

class float32(Decimals):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "f", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return float32(*bits_to_bytes(bits, f="f"))

class float64(Decimals):
    def __new__(self, *args, endianness=sys.byteorder):
        return super().__new__(self, "d", *args, endianness=endianness)
    
    @staticmethod
    def from_bits(bits):
        return float64(*bits_to_bytes(bits, f="d"))
