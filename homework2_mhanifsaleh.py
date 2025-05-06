############################################################
# ECS 170: Logic
############################################################

student_name = "Mohammad Ayub Hanif Saleh"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    
class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __hash__(self):
        return hash(self.name)
    #we need to check the type of the other object but not with string or other types
    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.name == other.name
        return False
    
    def __repr__(self):
        return f"Atom({self.name})"
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __hash__(self):
        return hash(self.arg)
    
    #This time we need to I think compare the arg with the other arg rather than the name.
    def __eq__(self, other):
        if isinstance(other, Not):
            return self.arg == other.arg
        return False
    
    def __repr__(self):
        return f"Not({self.arg})"
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __hash__(self):
        return hash(self.conjuncts)
    
    #This time we need to I think compare the conjuncts with the other conjuncts rather than the name.
    def __eq__(self, other):
        if isinstance(other, And):
            return self.conjuncts == other.conjuncts
        return False

    def __repr__(self):
        args = ", ".join(repr(a) for a in self.conjuncts)
        return f"And({args})"
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __hash__(self):
        return hash(self.disjuncts)
    
    #This time we need to I think compare the disjuncts with the other disjuncts rather than the name.
    def __eq__(self, other):
        if isinstance(other, Or):
            return self.disjuncts == other.disjuncts
        return False

    def __repr__(self):
        args = ", ".join(repr(a) for a in self.disjuncts)
        return f"Or({args})"
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash(self.hashable)

    #this one is alittle diff we need to test the type of the other object comparing the left and right of the other object.
    #it is because we have more information to compare now than just the name or the arg or signal component.
    def __eq__(self, other):
        if isinstance(other, Implies):
            return self.left == other.left and self.right == other.right
        return False

    def __repr__(self):
        return f"Implies({self.left}, {self.right})"
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash(self.hashable)

    #I think this one is the same as the last eq function but this is insensitive.
    def __eq__(self, other):
        if isinstance(self, other):
            return {self.left, self.right} == {other.left, other.right}
        return False

    def __repr__(self):
        return f"Iff({self.left}, {self.right})"

    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

def satisfying_assignments(expr):
    pass

class KnowledgeBase(object):
    def __init__(self):
        pass
    def get_facts(self):
        pass
    def tell(self, expr):
        pass
    def ask(self, expr):
        pass

############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = None
magical_query = None
horned_query = None

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = None
is_magical = None
is_horned = None

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = None

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = None

# Write your answer to the question in the assignment
puzzle_2_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
# guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
