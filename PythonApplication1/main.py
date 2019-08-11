from ui import *
from quickmaths import *
from equationClasses import *
import sys
import pstats
import cProfile

line = tokenize("y=mx+c")
def normalAtX(curve, x):
    m = curve.differentiate("x").substitute(x=x)
    if m==0:
        return equality(Var("x"), fractize(x))
    new_m = -1/m
    c = line.solve("c", y=curve.substitute(x=x), m=new_m, x=x)
    return line.substitute(m=new_m, c=c)



if __name__=='__main__':
    t = tokenize("2x^3-30x^2+162x=0")
    print(t.solve("x"))
    normalAtX(tokenize("3x^3-2x^2-6x+2"), 1).print()
    #coefficient finding +
    #equation casting

def profile():
    cProfile.run('tokenize("(3x^5-2x^3-5x)/x=5x").solve("x")', sort=pstats.SortKey.CUMULATIVE)