class Term:
    def __init__(self, coef=NumFrac(1, 1), var=None):
        self.coef = fractize(coef)
        self.var = var
        self.varcode = ""
        if var:
            self.varcode = self.var.genVarcode()
            
    def copy(self):
        if self.isNum():
            return Term(self.coef)
        return Term(self.coef, self.var.sym, self.var.power)
    def isNum(self):
        return not bool(self.var)
    def isZero(self):
        return self.coef.den==0
    def addCoef(self, n):
        copy = self.copy()
        copy.coef += n
        return copy
    def getCoef(self):
        return self.coef
    def addPower(self, n):
        copy = self.copy()
        assert copy.var
        copy.var.power += n
        return copy
    def __str__(self):
        return createString(
            (
                ("{}", self.coef),
                ("({})", self.var)
            )
        )


class divPair(chainBase):
    def __init__(self, num, den):
        raise PendingDeprecationWarning
        self.num = num
        self.den = den
        self.function = None
        self.varcode = frozenset()
    def copy(self):
        return divPair(self.num.copy(), self.den.copy())
    def chain(self):
        return (self,)
    def canMult(self, other):
        return True
    def mult(self, other):
        if isinstance(other, divPair):
            return divide(mult(self.num, other.num), mult(self.den, other.den))
        return divide(mult(self.num, other), self.den)
    def __str__(self):
        return "({})/({})".format(self.num, self.den)