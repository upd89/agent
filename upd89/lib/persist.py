import shelve


class Persist:

    def __init__(self, filename):
        self.store = shelve.open(filename)

    def __contains__(self, key):
        return key in self.store

    def delete_key(self, key):
        if (key in self.store):
            del self.store[key]

    def get_key(self, key):
        if (key in self.store):
            return(self.store[key])
        else:
            return('')

    def get_keys(self):
        return self.store.keys()

    def set_key(self, key, value):
        self.store[key] = value

    def close(self):
        self.store.close()
