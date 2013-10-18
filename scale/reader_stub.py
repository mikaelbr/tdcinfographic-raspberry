import random

__max = 300
__acc = 0
def establish(idVendor, idProduct):

    def read():
        global __acc

        __acc = __acc + random.randint(1, __max/10)
        if __acc < __max:
            return __acc

        __acc = 0
        return __max

    return read