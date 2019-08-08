from ui import *
from quickmaths import *
from equationClasses import *
import sys
import pstats
import cProfile

def normalAtX(m, c, x):
    y = m*x+c
    new_m = -1/m
    new_c = y-new_m*x
    return equality(Var("y"), new_m*Var("x")+new_c)

if __name__=='__main__':
    t = tokenize("2x^3-30x^2+162x=0")
    print(t.solve("x"))
    normalAtX(NumFrac(5, 1), NumFrac(-3, 1), NumFrac(-6, 1)).print()
    #coefficient finding +
    #equation casting

def profile():
    cProfile.run('tokenize("(3x^5-2x^3-5x)/x=5x").solve("x")', sort=pstats.SortKey.CUMULATIVE)