class classproperty(property):
    "Acts like property but for calculated attributes on classes"

    def __get__(self, inst, cls):
        return super(classproperty, self).__get__(cls, cls)

    def __set__(self, inst, cls):
        return super(classproperty, self).__set__(cls, cls)

    def __delete__(self, inst, cls):
        return super(classproperty, self).__delete__(cls, cls)
