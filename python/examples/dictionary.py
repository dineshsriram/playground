import collections

class StrKeyDict(collections.UserDict):
    def __setitem__(self, key, value):
        self.data[str(key)] = value
    
    def __contains__(self, key):
        return str(key) in self.data

    def __missing__(self, key):
        if(isinstance(key, str)):
            raise KeyError
        return self.data[str(key)]
