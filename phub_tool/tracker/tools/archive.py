import struct
from struct import pack
from struct import unpack
from StringIO import StringIO

class OArchive:
    def __init__(self):
        self.__buff = StringIO()
    def getdata(self):
        return self.__buff.getvalue()
    def getbuff(self):
        return self.__buff
    def writeByte(self, byte):
        self.__buff.write( pack("B", byte) )
    def writeS16(self, i16):
        self.__buff.write( pack("h", i16) )
    def writeU16(self, i16):
        self.__buff.write( pack("H", i16) )
    def writeS32(self, i32):
        self.__buff.write( pack("i", i32) )
    def writeU32(self, i32):
        self.__buff.write( pack("I", i32) )
    def writeS64(self, i64):
        self.__buff.write( pack("q", i64) )
    def writeU64(self, i64):
        self.__buff.write( pack("Q", i64) )
    def writeString(self, str):
        self.writeU32(len(str))
        self.__buff.write(str)

class IArchive:
    def __init__(self, data):
        self.__buff = StringIO(data)
    def readAll(self, n):
        chunk = self.__buff.read(n)
        if len(chunk)!=n:
            raise EOFError()
        return chunk
    def readByte(self):
        buff = self.readAll(1)
        val, = unpack("B", buff)
        return val
    def readS16(self):
        buff = self.readAll(2)
        val, = unpack("h", buff)
        return val;
    def readU16(self):
        buff = self.readAll(2)
        val, = unpack("H", buff)
        return val;
    def readS32(self):
        buff = self.readAll(4)
        val, = unpack("i", buff)
        return val;
    def readU32(self):
        buff = self.readAll(4)
        val, = unpack("I", buff)
        return val;
    def readS64(self):
        buff = self.readAll(8)
        val, = unpack("q", buff)
        return val;
    def readU64(self):
        buff = self.readAll(8)
        val, = unpack("Q", buff)
        return val;
    def readString(self):
        len = self.readU32()
        str = self.readAll(len)
        return str
