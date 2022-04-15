import copy
from email.policy import default
from functools import reduce
from posixpath import split
from turtle import back


class CSP:
    def __init__(self, vars, domains, constraints, neighbors):
        #print("Initialize the CSP Problem")
        vars = vars
        update(self, vars=vars, domains=domains, constraints=constraints, neighbors=neighbors)
    def assign(self, var, val, assignment):
        #print("Assign the val to variable and place in assignment")
        assignment[var] = val
    def unassign(self, var, assignment):
        #print("unassign the var")
        if var in assignment:
            del assignment[var]
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            val2=assignment.get(var2, None)
            return val2!=None and not self.constraints(var, val, var2, val2)
        return count_if(conflict, self.neighbors[var])


def count_if(fun, seq):
    f = lambda count, x:count + (fun(x))
    return reduce(f, seq, 0)

def different_values_constraint(A, a, B, b):
    return a!=b

def backtracking(csp):
    update(csp)
    return recursive_backtracking({}, csp)


def recursive_backtracking(assignment, csp):
    #print("perform backtracking")
    if len(assignment) == len(csp.vars):
        return assignment
    
    var = select_unassigned_variable(assignment, csp)

    
    for val in order_domain_values(var, assignment, csp):
        if csp.nconflicts(var, val, assignment)==0:
            csp.assign(var, val, assignment)
            result = recursive_backtracking(assignment, csp)
            if result is not None:
                return result
            csp.unassign(var, assignment)
    return None

    # def order_domain_values(var, assignment, csp):
def select_unassigned_variable(assignment, csp):
    for v in csp.vars:
        if v not in assignment:
            return v

def order_domain_values(var, assignment, csp):
    #print("return any value from the domain")
    domain = csp.domains[var][:]
    while domain:
        yield domain.pop()

def update(x, **entries):
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x

vars = ['a', 'b', 'c']
domains = [1, 2, 3]
neighbors = {'a':['b'], 'b':['a', 'c'], 'c':['b']}

class UniversalDict:
    def __init__(self, value):
        self.value=value
    def __getitem__(self, key):
        return self.value

class DefaultDict(dict):
    def __init__(self, default):
        self.default = default
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))

    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy
print (f"\nOwn Example Answer: \n\n{backtracking(CSP(vars, UniversalDict(domains), different_values_constraint, neighbors))}\n")

def neighbors_parse(neighbors, vars=[]):
    dict = DefaultDict([])
    # make as much dict as variables
    for var in vars:
        dict[var]=[]
    specs = [ spec.split (":") for spec in neighbors.split(";")]
    for (A, Aneighbors) in specs:
        A = A.strip()
        dict.setdefault(A, [])
        for B in Aneighbors.split():
            dict[A].append(B)
            dict[B].append(A)
    return dict

print(f"Example Answer:\n\n{neighbors_parse('x: y z; y: z', list('xyz'))}\n")

def MapColoringCSP(colors, neighbors):
    if isinstance (neighbors, str):
        neighbors = neighbors_parse(neighbors)
        return CSP(neighbors.keys(), UniversalDict(colors), different_values_constraint, neighbors)

australia = MapColoringCSP(list("RGB"), "SA:WA NT Q NSW V; NT:WA Q; NSW: Q V; T: ")
# print(australia)

print(f"Map Coloring Answer:\n\n{backtracking(australia)}")