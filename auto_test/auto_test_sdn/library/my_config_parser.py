#!/bin/env python

from ConfigParser import ConfigParser

class XConfigParser(object):
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

    def get_string_url(self, key):
        if self.parser_.has_option("globalsection", key) is True:
            v = self.parser_.get("globalsection", key)
            return v.split(":",1)[1]
        return None

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
