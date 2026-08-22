"""
This module provides classes and functions for constructing and solving 
Constraint Satisfaction Problems (CSPs). It includes utilities for 
defining variable domains, constraints, and evaluating solutions.

This module is specifically written for COSC367 quizzes at
the University of Canterbury.

Author: Kourosh Neshatian
Last modified: 13 Aug 2024
"""



import collections, collections.abc


def scope(constraint):
    """
    Returns the set of variable names that the given constraint depends on.

    Parameters:
    constraint (function): A function representing the constraint. 
        It is expected to be a predicate function with variable names 
        as its formal parameters.

    Returns:
    set: A set containing the names of the formal parameters of the 
        constraint.
    """

    return set(constraint.__code__.co_varnames[
        :constraint.__code__.co_argcount])


def satisfies(assignment, constraint):
    """
    Checks whether a given assignment satisfies the specified constraint.

    Parameters:
    assignment (dict): A dictionary mapping variable names to their assigned values.
    constraint (function): A predicate function representing the constraint 
        that should be satisfied.

    Returns:
    bool: True if the assignment satisfies the constraint, False otherwise.
    """

    return constraint(**{var:val for var,val in assignment.items()
                         if var in scope(constraint)})
                     

class CSP(collections.namedtuple("CSP", "var_domains, constraints")):
    """
    Represents a Constraint Satisfaction Problem (CSP).

    An instance of CSP is constructed by specifying a dictionary of 
    variable domains and a collection of constraints. The variable domains 
    define the possible values for each variable, and the constraints 
    restrict the valid combinations of variable assignments.

    Attributes:
    var_domains (dict): A dictionary mapping variable names (str) to sets of 
        possible values (set).
    constraints (iterable): A collection of predicate functions representing 
        the constraints that must be satisfied by the variable assignments.
    """

    def __init__(self, var_domains, constraints):
        assert type(var_domains) is dict
        assert all(type(name) is str and type(domain) is set
                   for name, domain in var_domains.items())
        assert isinstance(constraints, collections.abc.Iterable)
        assert all(callable(c) and scope(c) <= set(var_domains.keys())
                   for c in constraints)



class Relation(collections.namedtuple("Relation", "header, tuples")):
    """
    Represents a relational table with a header and rows of data.

    The `header` is a sequence of strings representing column names. 
    Each tuple in the `tuples` set corresponds to a row in the table, 
    with its elements matching the columns defined by the `header`.

    For example, if the `header` is ['A', 'B', 'C'], then each tuple 
    should have three elements, where the first element corresponds to 'A', 
    the second to 'B', and the third to 'C'.

    """

    def __init__(self, header, tuples):
        assert isinstance(header, collections.abc.Sequence)
        assert all(type(element) is str for element in header)
        assert type(tuples) is set
        assert all(type(element) is tuple for element in tuples)
        assert all(len(tpl) == len(header) for tpl in tuples)

import itertools

def generate_and_test(csp):
    result = []
    
    names, domains = zip(*csp.var_domains.items())
    constraints = csp.constraints

    cart = itertools.product(*domains)
    
    for variables in cart:
        total_assignment = dict(zip(names, variables))
        solution = True
        for c in constraints:
            if not satisfies(total_assignment, c):
                solution = False
                break
        if solution:
            result.append(total_assignment)
            
    return result

crossword_puzzle = CSP(
    var_domains={
        # read across:
        'a1': set("ant,big,bus,car".split(',')),
        'a3': set("book,buys,hold,lane,year".split(',')),
        'a4': set("ant,big,bus,car,has".split(',')),
        # read down:
        'd1': set("book,buys,hold,lane,year".split(',')),
        'd2': set("ginger,search,symbol,syntax".split(',')),
        },
    constraints={
        lambda a1, d1: a1[0] == d1[0],
        lambda d1, a3: d1[2] == a3[0],
        lambda a1, d2: a1[2] == d2[0],
        lambda d2, a3: d2[2] == a3[2],
        lambda d2, a4: d2[4] == a4[0],
        })

solution = next(iter(generate_and_test(crossword_puzzle)))

# printing the puzzle similar to the way it actually  looks 
pretty_puzzle = ["".join(line) for line in itertools.zip_longest(
    solution['d1'], "", solution['d2'], fillvalue=" ")]
pretty_puzzle[0:5:2] = solution['a1'], solution['a3'], "  " + solution['a4']
print("\n".join(pretty_puzzle))