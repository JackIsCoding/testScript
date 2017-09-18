from ConfigParser import ConfigParser
import binascii
from archive import *

class CommandBase(object):
    def __init__(self):
        self.parser_ = ConfigParser()

    def load(self, filename):
        ret = self.parser_.read(filename);
        if len(ret)==0:
            return False

        return True;

    # private method
    def set_with_section(self, section, key, value):
        if self.parser_.has_option(section, key) is True:
            v = self.parser_.get(section, key)
            t = v.split(":")[0]
            self.parser_.set(section, key, str(t) + ":" + str(value));
            return True
        return False

    # private method
    def get_with_section(self, section, key):
        if self.parser_.has_option(section, key) is True:
            v = self.parser_.get(section, key)
            return v.split(":")[1]
        return None

    def set(self, key, value):
        return self.set_with_section("globalsection", key, value)

    def get_int(self, key):
        v = self.get_with_section("globalsection", key)
        if v is None:
            return None
        return int(v)

    def get_string(self, key):
        v = self.get_with_section("globalsection", key)
        if v is None:
            return None
        return v

    def set_struct_value(self, key, ikey, value):
        v = self.parser_.get("globalsection", key)

        section = v.split(":")[0]
        return self.set_with_section(key + "_" + section, ikey, value)

    def get_struct_value(self, key, ikey):
        v = self.parser_.get("globalsection", key)

        section = v.split(":")[0]
        return self.get_with_section(key + "_" + section, ikey)

    def get_struct_value_int(self, key, ikey):
        v = self.get_struct_value(key, ikey)
        if v is None:
            return None

        return int(v)

    def get_struct_value_string(self, key, ikey):
        v = self.get_struct_value(key, ikey)
        if v is None:
            return None

        return v

    def get_list_size(self, key):
        v = self.parser_.get("globalsection", key)
        if len(v.split(":"))<3 or v.split(":")[0]!="list":
            return None
        return int(v.split(":")[2])

    def get_list_type(self, key):
        v = self.parser_.get("globalsection", key)
        if len(v.split(":"))<3 or v.split(":")[0]!="list":
            return None
        return v.split(":")[1]

    def set_list_element_value(self, key, n, ikey, value):
        v = self.parser_.get("globalsection", key)
        if len(v.split(":"))!=3 or v.split(":")[0]!="list":
            return False;

        section = v.split(":")[1]

        if self.parser_.has_section( key + "_" + section + "_" + str(n) ) is False:
            return False

        return self.set_with_section( key + "_" + section + "_" + str(n), ikey, value )
    
    def add_list_element(self, key):
        v = self.parser_.get("globalsection", key)
        if len(v.split(":"))!=3 or v.split(":")[0]!="list":
            return False;

        section = v.split(":")[1]
        size = int(v.split(":")[2])

        if self.fork_section( section, key + "_" + section + "_" + str(size) ) is False:
            return False

        # set new list size
        self.parser_.set("globalsection", key, "list:" + section + ":" + str(size+1))
        return True

    def get_list_element_value(self, key, n, ikey):
        v = self.parser_.get("globalsection", key)
        if len(v.split(":"))!=3 or v.split(":")[0]!="list":
            return None;

        section = v.split(":")[1]

        if self.parser_.has_section( key + "_" + section + "_" + str(n) ) is False:
            return None

        return self.get_with_section( key + "_" + section + "_" + str(n), ikey )

    def get_list_element_value_int(self, key, n, ikey):
        v = self.get_list_element_value(key, n, ikey)
        if v is None:
            return None
        return int(v)

    def get_list_element_value_string(self, key, n, ikey):
        v = self.get_list_element_value(key, n, ikey)
        if v is None:
            return None
        return v

    # private method
    def fork_section(self, from_section, to_section):
        if self.parser_.has_section(from_section) is False:
            return False
        
        self.parser_.add_section(to_section)
        items = self.parser_.items(from_section)
        for item in items:
            self.parser_.set(to_section, item[0], item[1])
        return True

    def check_section(self, section):
        if self.parser_.has_section(section) is False:
            return False
        return True

    def print_all(self):
        for section in self.parser_.sections():
            print "[" + section + "]"
            for k in self.parser_.options(section):
                print k + " = " + self.parser_.get(section, k)
            print ""


class Request(CommandBase):
    def __init__(self):
        super(Request, self).__init__()

    def encode(self, ar):
        return self.encode_section(ar, "globalsection")
    
    def encode_section(self, ar, section):
        if self.parser_.has_section(section) is False:
            return False
        for k in self.parser_.options(section): #iterate all elements  
            if k=="__with_struct_size__":
                continue
            tmp = self.parser_.get(section, k) #value
            t = tmp.split(":")[0] # element type
            v = tmp.split(":")[1]
            if t=="uint8":
                ar.writeByte( int(v) ) 
            elif t=="uint16":
                ar.writeU16( int(v) )
            elif t=="uint32":
                ar.writeU32( int(v) )
            elif t=="uint64":
                ar.writeU64( int(v) )
            elif t=="string":
                ar.writeString( v )
            elif t=="string_hex":
                ar.writeString( binascii.unhexlify(v) )
            elif t=="list":
                element_type = tmp.split(":")[1]
                llen = int( tmp.split(":")[2] )
                # TODO
                # support build-in type array element
                # currently only self-defined struct is supportted
                
                ar.writeU32(llen)

                for n in range(llen):
                    if self.encode_struct(ar, k + "_" + element_type + "_" + str(n)) is False: # {key}_{struct}_{N}
                        return False

            else: # self-defined struct
                if self.encode_struct(ar, k + "_" + t) is False: # {key}_{struct}
                    return False
            
        return True;

    def encode_struct(self, ar, type):
        buf = ar.getbuff()
        last_pos = buf.tell()

        is_with_struct_size = 0
        if self.parser_.has_option(type, "__with_struct_size__") is False or int(self.parser_.get(type, "__with_struct_size__")) == 1:
            is_with_struct_size = 1

        if is_with_struct_size == 1:
            ar.writeU32(0) # placement struct length

        if self.encode_section(ar, type) is False:
           return False;

        if is_with_struct_size == 1:
            now_pos = buf.tell()
            buf.seek(last_pos)
            ar.writeU32( now_pos - last_pos - 4 )
            buf.seek(now_pos)
        return True

class Response(CommandBase):
    def __init__(self):
        super(Response, self).__init__()

    def decode(self, ar):
        try:
            return self.decode_section("globalsection", ar)
        except EOFError as e:
            print "e:%s"%e
            return False

    def decode_section(self, section, ar):
        if self.parser_.has_section(section) is False:
            print "!!!1"
            return False
        for k in self.parser_.options(section): #iterate all elements
            if k=="__with_struct_size__":
                continue
            tmp = self.parser_.get(section, k) #value
            t = tmp.split(":")[0] # element type
            v = ""
            if t=="uint8":
                v = ar.readByte() 
            elif t=="uint16":
                v = ar.readU16()
            elif t=="uint32":
                v = ar.readU32()
            elif t=="uint64":
                v = ar.readU64()
            elif t=="string":
                v = ar.readString()
            elif t=="string_unhex":
                v = binascii.hexlify( ar.readString() ).upper()
            elif t=="list":
                element_type = tmp.split(":")[1]
                # TODO
                # support build-in type array element
                # currently only self-defined struct is supportted
                
                llen = ar.readU32() # list len
                self.parser_.set(section, k, t + ":" + element_type + ":" + str(llen)) # set list length, list:mystruct:2
                for n in range(llen):
                    self.fork_section(element_type, k + "_" + element_type + "_" + str(n)) # create new section {key}_{struct}_{N}
                    if self.decode_struct(ar, k + "_" + element_type + "_" + str(n)) is False:
                        return False
                continue
            else: # self-defined struct
                self.fork_section(t, k + "_" + t) # create new section {key}_{struct}
                if self.decode_struct(ar, k + "_" + t) is False:
                    return False
                continue
	    #print("FUCK: type:%s -- value:%s", t,str(v))
            self.parser_.set(section, k, t + ":" + str(v))
            if k == 'sn_num' and int(v) == 0:
                break
        return True

    def decode_struct(self, ar, type):
        if self.parser_.has_option(type, "__with_struct_size__") is False or int(self.parser_.get(type, "__with_struct_size__")) == 1:
            len = ar.readU32()
        return self.decode_section(type, ar)

