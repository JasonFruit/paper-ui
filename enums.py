class enum(object):
    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

align = enum(left=-1, center=0, right=1)
directions = enum(x=0, y=1)
keystates = enum(down=1, up=0, hold=2)
