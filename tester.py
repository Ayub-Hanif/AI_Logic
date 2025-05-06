from homework2_mhanifsaleh import Atom, And, Or, Not, Implies, Iff


def test_atom_equality():
    print("Atom('a') == Atom('a'):", Atom("a") == Atom("a"))
    print("Atom('a') == Atom('b'):", Atom("a") == Atom("b"))
    print("And(Atom('a'), Not(Atom('b'))) == And(Not(Atom('b')), Atom('a')):", And(Atom("a"), Not(Atom("b"))) == And(Not(Atom("b")), Atom("a")))
    
    


test_atom_equality()

