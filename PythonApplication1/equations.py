import ui
from constants import *
QUADRATIC = ui.tokenize(f"(-b{PLUS_MINUS}(b^2-4ac)^0.5)/(2a)")
#http://www.sosmath.com/algebra/factor/fac11/fac11.html
DEPRESSED_CUBIC_COEFS = ui.tokenize("c/a-b^2/(3a^2)"), ui.tokenize("d/a+2b^3/(27a^3)-bc/(3a^2)")
