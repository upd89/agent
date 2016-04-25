import shelve


class Persist:

    def __init__(self, filename):
        self.store = shelve.open(filename)

    def has_key(self, key):
        return(self.store.has_key(key))

    def delete_key(self, key):
        if (self.has_key(key)):
            del self.store[key]

    def get_key(self, key):
        if (self.has_key(key)):
            return(self.store[key])
        else:
            return('')

    def get_keys(self):
        return self.store.keys()

    def set_key(self, key, value):
        self.store[key] = value

    def close(self):
        self.store.close()
