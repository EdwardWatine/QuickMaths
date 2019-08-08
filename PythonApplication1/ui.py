from quickmaths import *
import equationClasses as eqs
from constants import *
ops = f"=+*/^"
unary_ops = f"-{PLUS_MINUS}"
all_ops = ops+unary_ops
digit = lambda x: x.isdigit() or x=="."
neg = lambda x: mult(-1, x)
#unary = lambda f: lambda a1, a2: f(a2)

def tokenize(s):
    ns = []
    sindex = []
    brackets = []
    for i, x in enumerate(s):
        if x==")":
            brackets.append(str2chain("".join(ns[sindex[-1]:]), brackets))
            ns[sindex[-1]:] = f"\x00{len(brackets)-1}\x00"
            sindex.pop()
            if i<len(s)-2 and s[i+1]=="(":
                ns.append("*")
            continue
        if x=="(":
            sindex.append(len(ns))
            continue
        if (digit(x) or x.isalpha()) and i<len(s)-1 and s[i+1]!=")" and s[i+1] not in all_ops:
            if digit(x) and digit(s[i+1]):
                ns.append(x)
                continue

            ns.append(x+"*")
            continue
        if x in ("-", PLUS_MINUS) and i!=0 and (ns and ns[-1] not in all_ops and ns[-1]!="("):
            ns.append("+")
        ns.append(x)

        
            
    ns = "".join(ns)
    return str2chain(ns, brackets)

opdict = {"-":neg, "+":add, "*":mult, "/":divide, 
          "^":lambda *args: power(*args, positive_root=True), "=":eqs.equality, 
          PLUS_MINUS:plusminus }
def str2chain(s, brackets=[]):
    #print(repr(s))
    for x in ops:
        if x in s:
            return opdict[x](*(str2chain(z, brackets) for z in s.split(x)))
    for x in unary_ops:
        if x == s[0]:
            return opdict[x](str2chain(s[1:], brackets))
    if s[0]=="\x00":
        return brackets[int(s[1:-1])]
    if s.isalpha():
        if s=="i":
            return I()
        return Var(s)
    else:
        return fractize(s)

