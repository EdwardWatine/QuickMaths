def pl(l, *args, **kwargs):
    print([str(n) for n in l], *args, **kwargs)

def createString(codeValPairs):
    return ''.join('' if not value else code.format(value) for code, value in codeValPairs)

def cartFunc(a, b, func):
    for x in a:
        for y in b:
            yield func(x, y)

def nth_root(num, n):
    if num==1:
        return 1
    for i in range(1, num):
        val = pow(i, n)
        if val==num:
            return i
        if val>num:
            return None

class multiList(list):
    def __init__(self):
        super().__init__([[]])
    def append(self, x):
        for y in self:
            y.append(x)
    def split(self, *values):
        for y in self[:]:
            for value in values[1:]:
                super().append(y[:]+value)
            y.extend(values[0])
    def extend(self, i):
        for x in i:
            self.append(x)