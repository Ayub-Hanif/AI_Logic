from homework2_mhanifsaleh import Atom, And, Or, Not, Implies, Iff


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
    




          


test_atom_equality()

