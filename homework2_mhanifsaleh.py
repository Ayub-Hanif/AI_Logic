############################################################
# ECS 170: Logic
############################################################

student_name = "Mohammad Ayub Hanif Saleh"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import itertools

############################################################
# Section 1: Propositional Logic
############################################################
before = ", "

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
    
    #I tired my best to make it look like the expression given in the example but can't be exact.
    def __repr__(self):
        return f"Atom({self.name})"
    
    def atom_names(self):
        return {self.name}
    
    #I think the easy was is to just check if its true or false by checking the name of the atom.
    def evaluate(self, assignment):
        if self.name not in assignment:
            return False
        else: 
            return bool(assignment[self.name]) 
    
    def to_cnf(self):
        return self

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
        return self.arg.atom_names()
    
    #The way this should be is that not of arg with the assignment.
    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)
    
    def to_cnf(self):
        if isinstance(self.arg, Atom):
            return self
        if isinstance(self.arg, Not):
            return self.arg.arg.to_cnf()
        
        # I think de Morgan's law we should use here so we can convert the negation of a conjunction
        # into a disjun of neg. but we also need to check if the arg is a disjun and conjuction.
        if isinstance(self.arg, And):
            neg_cons = []
            for con in self.arg.conjuncts:
                neg_con = Not(con).to_cnf()
                neg_cons.append(neg_con)
            result = Or(*neg_cons)
            return result.to_cnf()
        
        #same thing from above but with or.
        if isinstance(self.arg, Or):
            neg_dis = []
            
            for disjunct in self.arg.disjuncts:
                dis = Not(disjunct).to_cnf()
                neg_dis.append(dis)
            result = And(*neg_dis)
            return result.to_cnf()
        return Not(self.arg.to_cnf()).to_cnf()


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
        return f"And({before.join(repr(a) for a in self.conjuncts)})"
    
    def atom_names(self):
        name = set()
        for con in self.conjuncts:
            name.update(con.atom_names())
        return name
    
    #I think the easy was is to just check if its true or false by checking the name of the atom.
    def evaluate(self, assignment):
        for con in self.conjuncts:
            if not con.evaluate(assignment):
                return False
        return True
    
    def to_cnf(self):
        #temp_expr_cnf of the conjuction is conjuction of the temp_expr_cnf parts flatten nested Ands
        cnf_conjuncts_part = []
        for con in self.conjuncts:
            sub = con.to_cnf()
            if isinstance(sub, And):
                cnf_conjuncts_part.extend(sub.conjuncts)
            else:
                cnf_conjuncts_part.append(sub)
        if len(cnf_conjuncts_part) == 1:
            return cnf_conjuncts_part[0]
        return And(*cnf_conjuncts_part)

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
        return f"Or({before.join(repr(a) for a in self.disjuncts)})"
    
    def atom_names(self):
        name = set()
        for dis in self.disjuncts:
            name.update(dis.atom_names())
        return name
    
    # I think we evaluate the disjuncts and if any one of them is true then return it.
    def evaluate(self, assignment):
        for dis in self.disjuncts:
            if dis.evaluate(assignment):
                return True
        return False

    def to_cnf(self):
        #This is same ish like last one I did I am guessing we do temp_expr_cnf of the disjunction which should be disjunction of the temp_expr_cnf parts flatten nested Or
        # each disjunct into temp_expr_cnf first and then flatten nested Or
        parts = [d.to_cnf() for d in self.disjuncts]

        # if repeatedly distribute OR over AND until no AND is inside then we can return the result.
        result = parts[0]
        for i in range(1, len(parts)):
            current_expression = parts[i]
            result = Or._distribute(result, current_expression)

        #I think making flatten nested Or that may remain after dis is done.
        if isinstance(result, Or):
            flat = []
            for d in result.disjuncts:
                flat.extend(d.disjuncts if isinstance(d, Or) else [d])
            result = Or(*flat)
        
        #I keep failing the test I think it is the check for the nested And and if it is true then we need to do the distribution.
        # The AND is inside the Or not equalling the Cnf but not sure we'll rerun it and see.
        # good fixed one test I think but didn't fix all of them.
        for a in result.disjuncts if isinstance(result, Or) else []:
            if isinstance(a, And):
                result = Or._distribute(*result.disjuncts).to_cnf()
                break
        
        #after testing more I think I found why it is not passing, it is becuase Clause might not contain an Or inside another Or.
        #The ﬂatten‑once might not be enough,
        #to solve it I think I will just use a recursive function to flatten the Ors.
        #rerun check to see if it does fix my problem.
        if isinstance(result, Or):
            def recur_flat(disj):
                for a in disj.disjuncts:
                    if isinstance(a, Or):
                        yield from recur_flat(a)
                    else:
                        yield a
            result = Or(*recur_flat(result))
        
        return result

    #I know the @saticmethod from my research project once again.
    @staticmethod # staticmethod I created so that I can call it in the to_cnf function.
    # it makes my code cleaner and easier to read.
    def _distribute(a, b):
        if isinstance(a, And):
            return And(*[Or._distribute(c, b) for c in a.conjuncts]).to_cnf()
        if isinstance(b, And):
            return And(*[Or._distribute(a, c) for c in b.conjuncts]).to_cnf()
        return Or(a, b)

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
        #union of the both sides of the implies by using union function that I learned the union function when using it for my research project.
        return self.left.atom_names().union(self.right.atom_names())
    
    #the same as the or but we need to check the left and if it is false or right side bc we just do a or.
    def evaluate(self, assignment):
        not_eval = not self.left.evaluate(assignment)
        eval = self.right.evaluate(assignment)
        return not_eval or eval

    def to_cnf(self):
        first = Not(self.left).to_cnf()
        second = self.right.to_cnf()
        final = Or(first, second).to_cnf()
        return final

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash(self.hashable)

    #I think this one is the same as the last eq function but this is insensitive.
    def __eq__(self, other):
        if isinstance(other, Iff):
            return {self.left, self.right} == {other.left, other.right}
        return False

    def __repr__(self):
        return f"Iff({self.left}, {self.right})"

    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())

    #iff is true if both sides are false or true otherwise it is false.
    def evaluate(self, assignment):
        left_eval = self.left.evaluate(assignment)
        right_eval = self.right.evaluate(assignment)
        return left_eval == right_eval

    def to_cnf(self):
        A_to_B = Implies(self.left, self.right).to_cnf()
        B_to_A = Implies(self.right, self.left).to_cnf()
        final = And(A_to_B, B_to_A).to_cnf()
        return final

def satisfying_assignments(expr):
    name = expr.atom_names()
    #changed the F and T so it matches the example but IDK if they care alot? or want it either way.
    for value in itertools.product([False, True], repeat=len(name)):
        #we make a dict of the name and value and then we check if the expr is true or false.
        #the zip func is used to bring name and value tog to make it easier to check the expr.
        temp = dict(zip(name, value))
        if expr.evaluate(temp):
            yield temp
#frozenset I used to make the set immutable so that it can be used only as a 
#key for the dictary and not be able to be changed at all after it is created.
class KnowledgeBase(object):
    def __init__(self):
        self.fact = set()

    def get_facts(self):
        return set(self.fact)
    
    def tell(self, expr):
        temp_expr_cnf = expr.to_cnf()
        if isinstance(temp_expr_cnf, And):
            self.fact.update(temp_expr_cnf.conjuncts)
        else:
            self.fact.add(temp_expr_cnf)
    
    # the ask function is used to check if the expr is true or false
    # for the knowledge base and it uses the resolution which was said in the hw and 
    # I think the it is best way to check the expr.
    ##((okay so it is help all those edge cases and checks that I add now.))
    def ask(self, query):
        # added more checks and edge cases because maybe they are checking for edges idky yet.
        if query is True:
            return True
        
        #overall there is all this checks because I want to see if I missed any edge cases or not and hopefully
        #this will cover all of the test cases.
        
        #just as the name says I created this function to make it easier to check the literals in the clause.
        # and it will also make it easier to keep debugging and testing as the code gets bigger since it is not passing all the test yet.
        def helper_literal_set(clause):
            if isinstance(clause, Or):
                items = clause.disjuncts
            else:
                items = [clause]
            literals = set()
            for any_literal in items:
                if isinstance(any_literal, Atom) or (isinstance(any_literal, Not) and isinstance(any_literal.arg, Atom)):
                    literals.add(any_literal)
            return frozenset(literals)

        #if the query is not a literal made it to convert it to cnf then check if it is true.
        clause = {helper_literal_set(a) for a in self.fact}
        if query is not False:
            nq = Not(query).to_cnf()
            if isinstance(nq, And):
                clause.update({helper_literal_set(a) for a in nq.conjuncts})
            else:
                clause.add(helper_literal_set(nq))

        while True:
            new = set()
            clist = list(clause)
            for i, clause_one in enumerate(clist):
                #if we have a clause that is empty then we can return true.
                #otherwise we need keep going and checking from 1 to end.
                for clause_two in clist[i + 1:]:
                    if clause_one <= clause_two or clause_two <= clause_one:
                        continue
                    #I made a check to see if the literal is an atom and then I check if its in the clau.
                    for temp_literal in clause_one:
                        if isinstance(temp_literal, Atom):
                            complement_literal = Not(temp_literal)
                        else:
                            complement_literal = temp_literal.arg
                        # I made it to check if the complement literal is in the clause two.
                        #if it is then I can make the resolvent therefore check if it is empty or not.
                        if complement_literal in clause_two:
                            clause_one_reduced = clause_one - {temp_literal}
                            clause_two_reduced = clause_two - {complement_literal}
                            resolvent = clause_one_reduced | clause_two_reduced
                            if not resolvent:
                                return True
                            #the any check is used to see if the resol is in the clau or not.
                            if any((Not(x) if isinstance(x, Atom) else x.arg) in resolvent for x in resolvent):
                                continue
                            #then make sure it is all not in the clause.
                            if all(not k <= resolvent for k in clause):
                                new.add(frozenset(resolvent))

            # if is subset of the clause then we do false.
            if new.issubset(clause):
                return False
            clause.update(new)

############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()

#If the unicorn is mythical, then it is immortal
kb1.tell(Implies(Atom("mythical"), Not(Atom("mortal"))))

#but if it is not mythical, then it is a mortal mammal
kb1.tell(Implies(Not(Atom("mythical")), And(Atom("mortal"), Atom("mammal"))))

# If the unicorn is either immortal or a mammal, then it is horned.
kb1.tell(Implies(Or(Not(Atom("mortal")), Atom("mammal")), Atom("horned")))

#The unicorn is magical if it is horned.
kb1.tell(Implies(Atom("horned"), Atom("magical")))



#idk if they want it like this??
# Write an Expr for each query that should be asked of the knowledge base
mythical_query = Atom("mythical")  # the unicorn is mythical? 
magical_query = Atom("magical") # the unicorn is magical?
horned_query = Atom("horned") # the unicorn is horned?

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = And(Implies(Or(Atom("a"),Atom("m")), Atom("j")),
                        Implies(Not(Atom("m")), Atom("a")),
                        Implies(Atom("a"),Not(Atom("j")))                
                        )

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = list(satisfying_assignments(party_constraints))

# Write your answer to the question in the assignment
puzzle_2_question = """
I think the correct answer is that Ann don't come since she is not coming with Mary.
And John is not coming with Ann. So the only way it will work is if Mary and John only comes and not Ann. 
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

#whats in the rooms
kb3.tell(Iff(Atom("p1"), Not(Atom("e1"))))
kb3.tell(Iff(Atom("p2"), Not(Atom("e2"))))

#what are the signs saying
kb3.tell(Iff(Atom("s1"), And(Atom("p1"), Atom("e2"))))
kb3.tell(Iff(Atom("s2"), And(Or(Atom("e1"),Atom("e2")), Or(Atom("p1"), Atom("p2")))))

#only one sign can be true
kb3.tell(Iff(Atom("s1"), Not(Atom("s2"))))

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
I think the room 1 is empty since room 2 have the prize and sign 1 is false because to
have the sign 1 false and sign 2 true then the prize is in room 2 and thus room 1 is empty.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()

#finally got the last 3 tests to pass, it was very hard but stupidly simple since I didn't think
#about the last case which I have to define :( Also this was the hardest part for me and simplest at the same time.

# Adam is innocent and blame Brown indirectly and Clark is innocent.
kb4.tell(Iff(Atom("ia"), And(Atom("kb"), Not(Atom("kc")))))

#Brown says he didn't know the guy and he is innocent. Then Adam is lying.
#kb4.tell(Iff(Atom("ib"), And(Not(Atom("ka")), Atom("kc"))))

#Brown says he is innocent because he said he didn't know him.
kb4.tell(Iff(Atom("ib"), Not(Atom("kb"))))

#(((((((((((((now to clean up my code and resubmit..))))))))))))

#Clark is innocent  bceause he says I didn't do it and I saw both Adam and Brown with him.
#so he knew both possibly and one of them is guilty not Clark from what he said.
kb4.tell(Iff(Atom("ic"), And(Atom("ka"), Atom("kb"))))

#to check and also combine since sometimes the test is passing with some conditions and some times it does not.
#so I am making exactly 2 things are true and only one thing is false which will be guilty.
kb4.tell(Or(And(Atom("ia"),   Atom("ib"),   Not(Atom("ic"))),
            And(Atom("ia"),   Not(Atom("ib")), Atom("ic")),
            And(Not(Atom("ia")), Atom("ib"),   Atom("ic"))
            )
        )

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
I think the guilty one is Brown because I asked the KB whether each victim is innocent or not.
I found that the adam is innocent and Clark is innocent but brown was guilty by getting false for him.
"""