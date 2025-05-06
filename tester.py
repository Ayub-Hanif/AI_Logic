from homework2_mhanifsaleh import *

def assert_true(msg, cond):
    print(msg, "PASS" if cond else "FAIL")
    if not cond:
        raise AssertionError(msg)

# -------------------------------------------------------------------- 1  Expr.__eq__
print("\n### 1  Expr.__eq__\n")

a, b, c, d = map(Atom, "abcd")
assert_true("Iff equality order‑insensitive",
            Iff(a, b) == Iff(b, a))

assert_true("And equality set‑insensitive (4 conjuncts)",
            And(a, b, c, d) == And(d, c, b, a))

assert_true("Or equality set‑insensitive (duplicates removed)",
            Or(a, a, b) == Or(b, a))

assert_true("Not unequal to Atom with same name",
            Not(a) != a)

# -------------------------------------------------------------------- 2  satisfying_assignments
print("\n### 2  satisfying_assignments ordering\n")

expr = Or(a, b)             # atoms: a < b
gen  = satisfying_assignments(expr)
expected = [
    {'a': False, 'b': True},
    {'a': True,  'b': False},
    {'a': True,  'b': True}
]
assert_true("satisfying_assignments enumerates False‑first & lexicographic",
            expected == [next(gen) for _ in expected])

try:
    next(gen)
    assert_true("generator exhausted after all models", False)
except StopIteration:
    print("generator exhausted after all models  PASS")

# -------------------------------------------------------------------- 3  to_cnf corner cases
print("\n### 3  to_cnf corner cases\n")

def cnf_equiv(e):
    cnf = e.to_cnf()
    # logically equivalent & result is conjunction of clauses of literals
    models_ok = all(e.evaluate(m) == cnf.evaluate(m)
                    for m in satisfying_assignments(Or(a, b, c)))
    structural_ok = isinstance(cnf, (Atom, Not, And, Or))
    return models_ok and structural_ok

exprs = [
    Not(Iff(a, b)),
    Or(And(a, b), c),
    Implies(And(a, b), Or(c, d)),
    Not(Or(And(a, b), Not(c)))
]
for i, e in enumerate(exprs, 1):
    assert_true(f"to_cnf complex #{i}", cnf_equiv(e))

# -------------------------------------------------------------------- 4  KnowledgeBase.ask difficult cases
print("\n### 4  KnowledgeBase.ask resolution soundness\n")

kb = KnowledgeBase()
kb.tell(Implies(a, b))
kb.tell(Implies(b, c))
kb.tell(a)
assert_true("kb ⊨ c        (chained implication)",
            kb.ask(c))

assert_true("kb ⊭ ¬c       (negation not entailed)",
            not kb.ask(Not(c)))

kb2 = KnowledgeBase()
kb2.tell(And(a, Not(a)))      # explicit contradiction
assert_true("Contradictory KB entails everything (principle of explosion)",
            kb2.ask(b) and kb2.ask(Not(b)))

kb3 = KnowledgeBase()
kb3.tell(Or(a, b))
kb3.tell(Implies(a, c))
kb3.tell(Implies(b, c))
assert_true("multiple support, but neither a nor b individually entailed",
            kb3.ask(c) and not kb3.ask(a) and not kb3.ask(b))

print("\nAll extra edge‑case checks completed.")


def test_atom_equality():
    print("\nPropositional Logic - Test#1: ")
    print("--------------------------------------------------------------------")
    print("Atom('a') == Atom('a'):", Atom("a") == Atom("a"))
    print("******************************")
    print("Atom('a') == Atom('b'):", Atom("a") == Atom("b"))
    print("******************************")
    print("And(Atom('a'), Not(Atom('b'))) == And(Not(Atom('b')), Atom('a')):", And(Atom("a"), Not(Atom("b"))) == And(Not(Atom("b")), Atom("a")))
    print("=====================================================================")
    print("\nPropositional Logic - Test#2:\n ")
    print("--------------------------------------------------------------------")
    a, b, c = map(Atom, "abc")
    print("a,b,c = map(Atom, 'abc')")
    print("Implies(a,Iff(b,c))")
    print(Implies(a, Iff(b, c)))
    print("******************************")
    a, b, c = map(Atom, "abc")
    print("a,b,c = map(Atom, 'abc')")
    print("And(a, Or(Not(b), c))")
    print(And(a, Or(Not(b), c)))
    print("=====================================================================")
    print("\nPropositional Logic - Test#3:\n ")
    print("--------------------------------------------------------------------")
    print("Atom('a').atom_names()")
    print(Atom("a").atom_names())
    print("******************************")
    print("Not (Atom('a')).atom_names()")
    print(Not(Atom("a")).atom_names())
    print("******************************")
    print("a, b, c = map(Atom, 'abc')")
    a, b, c = map(Atom, "abc")
    print("expr = And(a, Implies(b, Iff(a,c)))")
    expr = And(a, Implies(b, Iff(a, c)))
    print("expr.atom_names()")
    print(expr.atom_names())
    print("******************************")
    print("=====================================================================")
    print("\nPropositional Logic - Test#4:\n ")
    print("--------------------------------------------------------------------")
    print("e = Implies(Atom('a'), Atom('b'))")
    e = Implies(Atom("a"), Atom("b"))
    print("e.evaluate({'a': False, 'b': True})")
    print(e.evaluate({"a": False, "b": True}))
    print("******************************")
    print("e.evaluate({'a': True, 'b': False})")
    print(e.evaluate({"a": True, "b": False}))
    print("******************************")
    print("a, b, c = map(Atom, 'abc')")
    a, b, c = map(Atom, "abc")
    print("e = And(Not(a), Or(b, c))")
    e = And(Not(a), Or(b, c))
    print("e.evaluate({'a': False, 'b': False, 'c': True})")
    print(e.evaluate({"a": False, "b": False, "c": True}))
    print("=====================================================================")
    print("\nPropositional Logic - Test#5:\n ")
    print("--------------------------------------------------------------------")
    print("e = Implies(Atom('a'), Atom('b'))")
    j = Implies(Atom("a"), Atom("b"))
    print("a = satisfying_assignments(j)")
    a = satisfying_assignments(j)
    print("next(a)")
    print(next(a))
    print("******************************")
    print("next(a)")
    print(next(a))
    print("******************************")
    print("next(a)")
    print(next(a))
    print("******************************")
    print("e = Iff(Iff(Atom('a'), Atom('b')), Atom('c'))")
    e = Iff(Iff(Atom("a"), Atom("b")), Atom("c"))
    print("list(satisfying_assignments(e))")
    print(list(satisfying_assignments(e)))
    print("=====================================================================")
    print("\nPropositional Logic - Test#6:\n ")
    print("--------------------------------------------------------------------")
    print("Atom('a').to_cnf()")
    print(Atom("a").to_cnf())
    print("******************************")
    print("a, b, c = map(Atom, 'abc')")
    a, b, c = map(Atom, "abc")
    print("Iff(a, Or(b, c)).to_cnf()")
    print(Iff(a, Or(b, c)).to_cnf())
    print("******************************")
    print("Or(Atom('a'), Atom('b')).to_cnf()")
    print(Or(Atom("a"), Atom("b")).to_cnf())
    print("******************************")
    print("a, b, c, d = map(Atom, 'abcd')")
    a, b, c, d = map(Atom, "abcd")
    print("Or(And(a, b), And(c, d)).to_cnf()")
    print(Or(And(a, b), And(c, d)).to_cnf())
    print("=====================================================================")
    print("\nPropositional Logic - Test#7:\n ")
    print("--------------------------------------------------------------------")
    print("a, b, c = map(Atom, 'abc')")
    a, b, c = map(Atom, "abc")
    print("kb = KnowledgeBase()")
    kb = KnowledgeBase()
    print("kb.tell(a)")
    kb.tell(a)
    print("kb.tell(Implies(a, b))")
    kb.tell(Implies(a, b))
    print("kb.get_facts()")
    print(kb.get_facts())
    print("******************************")
    print("kb.ask(x) for x in (a, b, c)")
    for x in (a, b, c):
        print(f"kb.ask({x})")
        print(kb.ask(x))
    print("******************************")





          


test_atom_equality()

