from helper import pl, createString, cartFunc, nth_root, multiList
import math, re
from functools import wraps
from constants import *
import sys
if __name__=='__main__':
    sys.setrecursionlimit(100)

def handleArgs(direct=False, expand=True):
    def _wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            new = multiList()
            for v in args:
                if isinstance(v, (int, float)):
                    new.append(fractize(v))
                elif isinstance(v, str):
                    if v.isalpha():
                        if v=="i":
                            new.append(I())
                        else:
                            new.append(Var(v))
                    else:
                        new.append(fractize(v))
                elif isinstance(v, (NumFrac, Var)):
                    new.append(v.copy())
                elif isinstance(v, multiValue):
                    new.split(*map(lambda value: list(value.copy().allargs()) if expand and value.function().__name__==f.__name__ else [value.copy()], v.values))
                elif expand and v.function().__name__==f.__name__:
                    new.extend(v.copy().allargs())
                else:
                    new.append(v.copy())
            fcomp = lambda cls, nargs: nargs[0] if len(nargs)==1 else cls(*nargs)
            if direct:
                return fcomp(multivalue, tuple(f(*x, **kwargs) for x in new))
            return fcomp(multivalue, tuple(fcomp(*f(*x, **kwargs)) for x in new))
        return wrapper
    return _wrapper

def autofactor(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        val = f(*args)
        if "factor" in kwargs and kwargs["factor"] and isinstance(val, addChain):
            return factor(val)
        return val
    return wrapper


def mult_gcd(*mults):
    current = mults[0]
    for x in mults[1:]:
        toadd = []
        for term in toadd():
            pass

def commonFactor(*chain):

    chainlist = chain
    current = chainlist[0]
    for term in chainlist[1:]:
        toadd = []
        for item in current.allargs():
            for comp in term.allargs():
                if isNum(item) or isNum(comp):
                    if (getattr(item, "den", 0)==getattr(comp, "den", 0) and 
                        math.gcd(getattr(item, "num", 0), getattr(comp, "num", 0))) > 1:
                            toadd.append(NumFrac(math.gcd(getattr(item, "num", 0), getattr(comp, "num", 0)), 1))
                            break
                    continue
                if item.varlist == comp.varlist:
                    toadd.append(power(item.var, max(0, min(item.exp, comp.exp))))
                    if toadd[-1]==1:
                        del ttoadd[-1]
                    break
        if not toadd:
            return NumFrac(1, 1)
        current = mult(*toadd)
    if len(current.allargs())==1:
        return current.allargs()[0]
    return current

def factor(chain):
    if not isinstance(chain, addChain):
        return chain
    f = commonFactor(*chain.chain())
    if f==1:
        return chain
    a = multChain(*f.allargs(), chain.removefactor(f))
    return a





def isNum(obj):
    return isinstance(obj, NumFrac)
def isNumOrI(obj):
    return isinstance(obj, (NumFrac, I))
def isNeg(obj):
    return getattr(obj, "coef", NumFrac(1, 1)).num<0



class chainBase:
    def allargs(self):
        return self.args
    def multargs(self):
        return self.allargs()
    def copy(self):
        return self.__class__(*(x.copy() for x in self.allargs()))
    def factor(self):
        return factor(self)
    @staticmethod
    def function():
        return lambda *args: None
    def genstr(self, other):
        return f"({self})" if self.oop<other.oop else f"{self}"
    def expand(self):
        return self
    def print(self):
        print(self)
    def substitute(self, **kwargs):
        return self.function()(*(x.substitute(**kwargs) for x in self.allargs()))
    def __neg__(self):
        return mult(-1, self)
    def __mul__(self, y):
        return mult(self, y)
    def __rmul__(self, y):
        return mult(self, y)
    def __truediv__(self, y):
        return divide(self, y)
    def __rtruediv__(self, y):
        return divide(y, self)
    def __add__(self, y):
        return add(self, y)
    def __radd__(self, y):
        return add(self, y)
    def __sub__(self, y):
        return add(self, -y)
    def __rsub__(self, y):
        return add(-self, y)
    def __exp__(self, y):
        return power(self, y)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return str(self)==str(other) and isinstance(other, chainBase)
    def __ne__(self, other):
        return not self.__eq__(other)

def fractize(num):
    if isNum(num):
        return num
    return NumFrac(*float(num).as_integer_ratio())
  
    
@autofactor
@handleArgs()
def add(*args, factor=False):
    new = []
    for x in args:
        if isNum(x) and x.isZero():
            continue
        for index, y in enumerate(new):
            if x.varcode==y.varcode:
                new[index] = y.add(x.coef)
                if new[index].coef.isZero():
                    del new[index]
                break
        else:
            new.append(x)
    if not new:
        return None, NumFrac(0, 1).chain()

    return addChain, new

class NumFrac(chainBase):

    oop = math.inf
    def __init__(self, num, den):
        if den==0:
            raise ZeroDivisionError()
        FGCD = math.gcd(num, den)
        self.num = num//FGCD
        self.den = den//FGCD
        if self.den<0:
            self.num *= -1
            self.den *= -1
        self.varcode = frozenset()
        self.varlist = frozenset()
        self.coef = self
        self.var = None
    def add(self, other):
        return NumFrac(self.num*other.den+self.den*other.num, self.den*other.den)
    def subtract(self, other):
        return NumFrac(self.num*other.den-self.den*other.num, self.den*other.den)
    def mult(self, other):
        return NumFrac(self.num*other.num, self.den*other.den)
    def divide(self, other):
        return NumFrac(self.num*other.den, self.den*other.num)
    def isZero(self):
        return self.num==0
    def isOne(self):
        return self.num==1 and self.den==1
    def copy(self):
        return NumFrac(self.num, self.den)
    def canMult(self, other):
        return isNum(other)
    def chain(self):
        return (self,)
    def allargs(self):
        return (self,)
    def multargs(self):
        return (self,)
    def contains(self, x):
        return False
    def substitute(self, **kwargs):
        return self
    def differentiate(self, subject):
        return NumFrac(0, 1)
    def __abs__(self):
        return NumFrac(abs(self.num), self.den)
    def __str__(self):
        return str(self.num)+('' if self.den==1 else "/{}".format(self.den))
    def __lt__(self, other):
        if math.isinf(other):
            return True
        other = fractize(other)
        return self.num*other.den<self.den*other.num
    def __gt__(self, other):
        if math.isinf(other):
            return False
        other = fractize(other)
        return self.num*other.den>self.den*other.num
    def __eq__(self, other):
        other = fractize(other)
        return self.den==other.den and self.num==other.num
    def __float__(self):
        return self.num/self.den
    def __neg__(self):
        return NumFrac(-self.num, self.den)
    def __hash__(self):
        return hash(self.num/self.den)
        
class Var(chainBase):
    oop = math.inf

    def __init__(self, var):
        self.var = var
        self.varlist = frozenset((var,))
        self.varcode = frozenset((self.var+"1",))
        self.coef = NumFrac(1, 1)
        self.exp = NumFrac(1, 1)   
        self.priority = ord("z")-ord(var)
    def __str__(self):
        return str(self.var)
    def add(self, coef):
        return multChain(NumFrac(1, 1).add(coef), self)
    def copy(self):
        return Var(self.var)
    def chain(self):
        return (self,)
    def canMult(self, other):
        return self.var in getattr(other, "varlist", ())
    def contains(self, x):
        return self.var==x
    def substitute(self, **kwargs):
        if self.var in kwargs:
            return kwargs[self.var]
        return self
    def allargs(self):
        return (self,)
    def multargs(self):
        return (self,)
    def mult(self, other):
        return power(self, other.exp.add(NumFrac(1, 1)))
    def divide(self, other):
        return power(self, NumFrac(1, 1).subtract(other.exp))
    def differentiate(self, subject):
        if subject==self.var:
            return NumFrac(1, 1)
        return NumFrac(0, 1)

class I(Var):
    def __init__(self):
        super().__init__("i")
    def mult(self, other):
        return NumFrac(-1, 1) if other.exp==1 else power(self, other.exp.add(NumFrac(1, 1)))
    def copy(self):
        return self
    def __str__(self):
        return "i"

class addChain(chainBase):
    oop = 0

    @staticmethod
    def function():
        return add

    @staticmethod
    def inverse(x):
        return mult(x, -1).expand()

    def __init__(self, *args):
        self.args = tuple(sorted(args, key=lambda x: getattr(x, "priority", 0), reverse=True))
        self.varcode = frozenset(str(x) for x in self.args)
        self.varlist = frozenset((frozenset(str(x) for x in self.args), frozenset(str(mult(-1, x)) for x in args)))
        self.neg = frozenset(str(mult(-1, x)) for x in args)
        self.exp = NumFrac(1, 1)
    def chain(self):
        return self.args
    def multargs(self):
        return (self,)
    def canMult(self, other):
        if self.varcode in other.varlist:
            return True
        if not isinstance(other, (addChain, powerPair)):
            return True
        return False
    def removefactor(self, other):
        return addChain(*(x.divide(other) for x in self.args))
    def divide(self, other):
        nargs = [self]
        if all(x.canMult(other) for x in self.args):
            return addChain(*(x.divide(other) for x in self.args)) #Cleared by factor instead?
        for x in other.multargs(): # REDO mAYBE # To factor or not to factor?
            if self.varcode in x.varlist:
                nargs[0] = (mult(-1, power(self, nargs[0].exp.subtract(x.exp))))
                if isinstance(x, addChain):
                    if self.varcode==x.neg:
                        nargs[0] = -nargs[0]
            else:
                nargs.append(power(x, -1))
        return mult(*nargs)
        """if self.varcode in other.varlist:
            if isinstance(other, addChain):
                if self.varcode==other.varlist[1]:
                    return mult(-1, power(self, self.exp.subtract(other.exp)))
            return power(self, self.exp.subtract(other.exp))
        if all(x.canMult(other) for x in self.args):
            return addChain(*(x.divide(other) for x in self.args))"""
        return multChain(self, power(other, -1))
    def mult(self, other):
        if not isinstance(other, addChain):
            return self.mult_through(other)
        if self.varcode == other.neg:
            return mult(-1, power(self, self.exp.add(other.exp)))
        return power(self, self.exp.add(other.exp))
    def mult_through(self, other):
        return add(*cartFunc(self.chain(), other.chain(), mult))
    def contains(self, x):
        return any(y.contains(x) for y in self.allargs())
    def differentiate(self, subject):
        return add(*(x.differentiate(subject) for x in self.args))
    def __str__(self):
        strs = [self.args[0].genstr(self)]
        for x in self.args[1:]:
            n = str(x)
            if n[0]=="-":
                strs.append(x.genstr(self))
                continue
            strs.append("+"+x.genstr(self))
        return "".join(strs)

@handleArgs()
def mult(*args):
    args = list(args)
    new = []
    while args:
        x = args.pop()

        for index, y in enumerate(new):
            if y.canMult(x):
                new.pop(index)
                args.append(y.mult(x))
                break
            if x.canMult(y):
                new.pop(index)
                args.append(x.mult(y))
                break
        else:
            new.append(x)
            if isNum(new[-1]) and new[-1].isOne():
                new.pop()
            elif isNum(new[-1]) and new[-1].isZero():
                return None, NumFrac(0, 1).chain()
    if new==[]:
        return None, NumFrac(1, 1).chain()
    return multChain, new

class multChain(chainBase):
    @staticmethod
    def function():
        return mult
    oop = 1
    def __init__(self, *args):
        self.args = list(sorted(args, key=lambda x: math.inf if isNum(x) else getattr(x, "priority", 0), reverse=True))
        self.coef = NumFrac(1, 1)
        self.varcode = []
        self.varlist = frozenset(x.varcode for x in self.args)
        for index, x in enumerate(self.args[:]):
            if isNum(x):
                self.coef = x
                del self.args[index]
            else:
                self.varcode.append(next(iter(x.varcode)))
        self.varcode = frozenset(self.varcode)
        self.priority = max(getattr(x, "priority", 0) for x in self.args)

    def allargs(self):
        return self.args if self.coef==1 else [self.coef]+(self.args)
    def chain(self):
        return (self,)
    def getCoef(self):
        return self.coef
    def add(self, coef):
        self.coef = self.coef.add(coef)
        return self
    def canMult(self, other):
        return True
    def contains(self, x):
        return any(y.contains(x) for y in self.args)
    def divide(self, other):
        nargs = []
        den = list(other.multargs())
        for item in self.multargs():
            for comp in other.multargs():
                if isNum(item) and isNum(comp):
                    nargs.append(item.divide(comp))
                    den.remove(comp)
                    break
                if item.varlist == comp.varlist:
                    nargs.append(item.divide(comp))
                    den.remove(comp)
                    break
            else:
                nargs.append(item)
        nargs.extend([power(x, -1) for x in den])
        return mult(*nargs)
    def expand(self):
        args = [x.expand() for x in self.allargs()]
        pil = -1
        for i, x in enumerate(args):
            if isinstance(x, addChain):
                pil = i
                break
        else:
            return mult(*args)
        new = self.allargs()[pil]
        for i, x in enumerate(self.allargs()):
            if i==pil:
                continue
            new = new.mult_through(x)
        assert isinstance(new, addChain)
        return new
    def differentiate(self, subject):
        oArgs = self.allargs()
        args = oArgs[:]
        new = []
        for x in range(len(args)):
            args[x] = args[x].differentiate(subject)
            args[x-1] = oArgs[x-1]
            new.append(mult(*args))
        return add(*new)
    @staticmethod
    def inverse(x):
        return power(x, -1)
    def __str__(self):
        if self.coef.isOne():
            strs = []
        elif self.coef == -1:
            strs = ["-"]
        else:
            strs = [str(self.coef)]
        for x in self.args:
            strs.append(x.genstr(self))
        return "".join(strs)
"""def reverse(f):
    def wrapper(base, exp):
        res = f(base, exp)
        if exp<NumFrac(0, 1):
            return divide(1, res)
        return res
    return wrapper"""

def powerplusminus(f):
    @wraps(f)
    def wrapper(base, exp, **kwargs):
        res = f(base, exp, **kwargs)
        if not isNum(exp) or exp.den%2!=0:
            return res
        if "positive_root" not in kwargs or not kwargs["positive_root"]:
            return plusminus(res)
        return res
    return wrapper

#@reverse
@powerplusminus
@handleArgs(direct=True, expand=False)
def power(base, exp, **kwargs):
    if not (isNum(base) and base==-1) and isNeg(base):
        return mult(power(-1, exp, **kwargs), power(mult(-1, base), exp, **kwargs))
    if isNum(base) and isNum(exp) and exp.den!=1:
        nr, dr = nth_root(base.num, exp.den), nth_root(base.den, exp.den)
        if nr and dr:
            base.num = nr
            base.den = dr
            exp.den = 1
    if isNumOrI(base) and isNum(exp) and exp.num != 1:
        m=NumFrac(1, 1)
        for x in range(abs(exp.num)):
            m=mult(m, base)
        if exp.num<0 and isNum(base):
            return NumFrac(1, 1).divide(base)
        if exp.den != 1:
           m = power(m, NumFrac(1, exp.den, **kwargs))
        return m
    if isNum(exp) and isNum(base) and base==-1 :
        if exp.den%2 == 1:
            return NumFrac(-1, 1)
        return I()
    if isNum(base) and base.isZero():
        return NumFrac(0, 1)
    if isNum(exp) and exp.isZero():
        return NumFrac(1, 1)
    if isNum(exp) and exp.isOne():
        return base
    if isinstance(base, multChain):
        return mult(*(power(x, exp, **kwargs) for x in base.allargs()))
    if isinstance(base, powerPair):
        return power(base.base, mult(base.exp, exp), **kwargs)
    return powerPair(base, exp)  

class powerPair(chainBase):
    @staticmethod
    def function():
        return power
    oop = 2
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp
        self.varcode = frozenset(("{}{}".format(base, exp),))
        self.varlist = getattr(base, "varlist", frozenset())
        self.var = getattr(base, "var", None)
        self.priority = getattr(base, "priority", 0)
        if isNum(exp):
            self.priority += float(exp)/128 #128 = 2^n > 26
        
    def copy(self):
        return powerPair(self.base, self.exp)
    def canMult(self, other):
        return self.var in getattr(other, "varlist", ())
    def mult(self, other):
        return power(self.base, other.exp.add(self.exp))
    def divide(self, other):
        return power(self.base, self.exp.subtract(other.exp))
    def chain(self):
        return (self,)
    def contains(self, x):
        return self.base.contains(x) or self.exp.contains(x)
    def expand(self):
        if not isNum(self.exp) or self.exp.den!=1:
            return self
        m = NumFrac(1, 1)
        for x in range(abs(self.exp.num)):
            m = add(*cartFunc(m.chain(), self.base.chain(), mult))
        return power(m, math.copysign(1, self.exp.num))
    def substitute(self, **kwargs):
        return power(self.base.substitute(**kwargs), self.exp.substitute(**kwargs), positive_root=True)
    def differentiate(self, subject): #NEEDS LN!
        if isinstance(self.base, Var) and self.base.var==subject:
            return mult(self.exp, power(self.base, self.exp-1))
    def allargs(self):
        return (self,)
    def multargs(self):
        return (self,)
    def __str__(self):
        return self.base.genstr(self)+"^"+self.exp.genstr(self)

#@handleArgs(direct=True, expand=False)
def multivalue(*args):
    values = []
    for v in args:
        if isinstance(v, multiValue):
            values.extend(v.values)
        else:
            values.append(v)
    s = tuple(set(values))
    if len(s)==1:
        return s[0]
    if len(s)==2 and s[0]==-s[1]:
        return plusminus(s[0])
    return multiValue(*s)

class multiValue(chainBase):
    def __init__(self, *args):
        self.values = args
    def __str__(self):
        return ", ".join(str(x) for x in self.values)
    def substitute(self, **kwargs):
        return multivalue(*(x.substitute(**kwargs) for x in self.values))
    def copy(self):
        return multiValue(*(x.copy() for x in self.values))
    def contains(self, subject):
        return any(x.contains(subject) for x in self.values)
    def __iter__(self):
        return iter(self.values)



@handleArgs(direct=True, expand=False)
def divide(num, den):
    num, den = factor(num), factor(den)
    if num.canMult(den):
        return num.divide(den)
    return mult(num, power(den, NumFrac(-1, 1)))

#@handleArgs(direct=True, expand=False)
def plusminus(y):
    if y==-y:
        return y
    return plusMinus(y)

class plusMinus(multiValue):
    def __init__(self, y):
        y = -y if isNeg(y) else y
        super().__init__(y, mult(-1, y))
    def __str__(self):
        return PLUS_MINUS+str(self.values[0])

def root(x, n):
    return power(x, NumFrac(1, n))

if __name__=='__main__':
    from ui import tokenize
    t = add("x", 5)
    t2 = power(add("x", 5), NumFrac(-1, 3))
    t3 = divide(t, t2)
    b = tokenize("3x+4xy+2xz")
    a = factor(b)
    print(a)





                
                        
