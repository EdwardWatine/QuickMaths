from quickmaths import *
class equality:
    def __init__(self, e1, e2):
        self.eq1 = e1
        self.eq2 = e2
    def simplify(self):
        self = self.copy()
        eqfactor = commonFactor(*(self.eq1.chain()+self.eq2.chain()))
        self.eq1 = divide(self.eq1, eqfactor)
        self.eq2 = divide(self.eq2, eqfactor)
        return self
    def rearrange(self, subject):
        self = self.copy()
        while True:
            flag = False
            if not isinstance(self.eq1, addChain) and not self.eq1.contains(subject):
                self.eq2 = add(self.eq2, mult(-1, self.eq1).expand())
                self.eq1 = NumFrac(0, 1)
                flag = True

            if not isinstance(self.eq2, addChain) and self.eq2.contains(subject):
                self.eq1 = add(self.eq1, mult(-1, self.eq2).expand())
                self.eq2 = NumFrac(0, 1)
                flag = True
            for op in (addChain, multChain):
                switch = []

                if isinstance(self.eq1, op):
                    switch.extend(x for x in self.eq1.allargs() if not x.contains(subject))
                if isinstance(self.eq2, op):
                    switch.extend(x for x in self.eq2.allargs() if x.contains(subject))
                if switch:
                    inverse = op.inverse(op.function()(*switch))
                    self.eq1 = op.function()(self.eq1, inverse)
                    self.eq2 = op.function()(self.eq2, inverse)
                    flag = True

            if not flag:
                break
        if isinstance(self.eq1, powerPair) and self.eq1.base.contains(subject):
            self.eq2 = power(self.eq2, power(self.eq1.exp, -1))
            self.eq1 = self.eq1.base
            #self.simplify()
            return self
        factored = factor(self.eq1)
        switch = tuple(x for x in factored.allargs() if not x.contains(subject))
        if len(switch)==len(factored.allargs())-1:
            self.eq1 = divide(self.eq1, mult(*switch))
            self.eq2 = divide(self.eq2, mult(*switch))
            #self.simplify()
            return self
        if isinstance(self.eq1, addChain):
            coefs = {}
            zero = False
            if self.eq2==0:
                self.simplify()
                zero = True
            for term in self.eq1.allargs():
                for item in term.allargs():
                    if item.contains(subject):
                        if not isinstance(item.exp, NumFrac):
                            return
                        coefs[item.exp] = divide(term, item)
                        break
                else:
                    return self
            minimum = min(coefs.keys())
            powers = set(map(lambda x: x.divide(minimum), coefs.keys()))
            if powers == set((1, 2)):
                import equations as eqs
                self.eq1 = Var(subject)
                self.eq2 = eqs.QUADRATIC.substitute(a=coefs[minimum*2], b=coefs[minimum], c=mult(-1, self.eq2))
                if zero:
                    self.eq2 = multivalue(self.eq2, NumFrac(0, 1))
            if powers == set((1, 2, 3)):
                import equations as eqs
                self.eq1 = Var(subject)
                #a=coefs[minimum*3], b=coefs[minimum*2], c=coefs[minimum], d=mult(-1, self.eq2)), eqs.DEPRESSED_CUBIC_COEFS))
                
            return self

    def substitute(self, **values):
        new = self.copy()
        new.eq1 = self.eq1.substitute(**values)
        new.eq2 = self.eq2.substitute(**values)
        return new
    def solve(self, var, **values):
        new = self.copy().substitute(**values).rearrange(var)
        return new.eq2
    def copy(self):
        return equality(self.eq1.copy(), self.eq2.copy())

    def print(self):
        print(self)

    def __str__(self):
        return f"{self.eq1}={self.eq2}"

class function(equality):
    def __init__(self, expr, *args):
        self.args = args
        self.expr = expr
    def __call__(self, *args):
        return self.expr.substitute(**dict(zip(self.args, args)))

if __name__=='__main__':
    from ui import tokenize
