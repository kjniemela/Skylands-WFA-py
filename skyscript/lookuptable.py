class LookupTable:
    def __init__(self):
        self.env = {}
        self.parent = None

    def __repr__(self):
        return "LookupTable(%s, $=%s)" % (str(self.env), repr(self.parent))

    def lookup(self, var):
        if var in self.env:
            return self.env[var]
        elif self.parent != None:
            return self.parent.lookup(var)
        else:
            return None

    def insert(self, var, val):
        self.env[var] = val

    def push_scope(self):
        parent = LookupTable()
        parent.env = self.env
        parent.parent = self.parent
        self.__init__()
        self.parent = parent

    def pop_scope(self):
        if self.parent != None:
            self.env = self.parent.env
            self.parent = self.parent.parent