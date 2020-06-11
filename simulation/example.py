from mlsolver.kripke import *
from mlsolver.tableau import *
from mlsolver.model import *
from mlsolver.formula import *

worlds = [
  World('1', {'p': True, 'q': True}),
  World('2', {'p': True, 'q': False}),
  World('3', {'p': False, 'q': True})
]

relations = {('1', '2'), ('2', '1'), ('1', '3'), ('3', '1'), ('3', '3'), ('2', '2')}
ks = KripkeStructure(worlds, relations)
print(ks)
f = And(Atom('q'), Atom('p'))
model = ks.solve(f)
print(model)
#model = ks.solve()