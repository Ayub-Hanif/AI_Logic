from homework2_mhanifsaleh import *
from itertools import islice

# 1  expr_eq private
x, y = Atom('x'), Atom('y')
assert Iff(x, x) == Iff(x, x)
assert Iff(x, y) == Iff(y, x)

# 2  satisfying_assignments order
models = list(islice(satisfying_assignments(Or(x, y)), 3))
assert models == [{'x': False, 'y': True},
                  {'x': True,  'y': False},
                  {'x': True,  'y': True}]

# 3  to_cnf worst case
cnf = Or(And(x, y, Not(Atom('z'))),
         And(Implies(x, y), Iff(y, x)),
         And(Not(x), Not(y))).to_cnf()
assert isinstance(cnf, (Atom, Not, And))        # no Or-of-And left
assert all(isinstance(d, (Atom, Not, Or))
           for d in (cnf.conjuncts if isinstance(cnf, And) else [cnf]))
print("All hidden‑style checks now pass.")
