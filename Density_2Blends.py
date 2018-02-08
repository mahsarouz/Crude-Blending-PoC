# Import PuLP modeler functions
from pulp import *
import pickle


Ing1 = ['C4', 'Condensate1']
Ing2 = ['Condensate2', 'Crude Oil']

# A dictionary of the costs of each of the Ing
costs1 = {'C4': 550, 
         'Condensate1': 410} 

costs2 = {'Condensate2': 410, 
         'Crude Oil': 385}         
         
# A dictionary of the density 
density1 = {'C4': 725, 
           'Condensate1': 520}

density2 = {'Condensate2': 520, 
           'Crude Oil': 680}

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Crude Blend",LpMinimize)

# A dictionary called 'ing_vars' is created to contain the referenced Variables
ing_vars1 = LpVariable.dicts("Ing1", Ing1, 0)
ing_vars2 = LpVariable.dicts("Ing2", Ing2, 0)

# The objective function is added to 'prob' first
prob += lpSum([costs1[i]*ing_vars1[i] for i in Ing1])+lpSum([costs2[i]*ing_vars2[i] for i in Ing2]), "Total Cost"

# The five constraints are added to 'prob'
prob += lpSum([density1[i] * ing_vars1[i] for i in Ing1]) >= 600, "Min Blend1 Target Density"
prob += lpSum([density1[i] * ing_vars1[i] for i in Ing1]) <= 640, "Max Blend1 Target Density"
prob += lpSum([density2[i] * ing_vars2[i] for i in Ing2]) >= 560, "Min Blend2 Target Density"
prob += lpSum([density2[i] * ing_vars2[i] for i in Ing2]) <= 620, "Max Blend2 Target Density"

prob += lpSum([ing_vars1[i] for i in Ing1]) == 1, "PercentagesSum1"
prob += lpSum([ing_vars2[i] for i in Ing2]) == 1, "PercentagesSum2"

# The problem data is written to an .lp file
prob.writeLP("CrudeBlend.lp")

print(prob)

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print ("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print (v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen    
print ("Total Cost", value(prob.objective))


# serialize the model on disk in the special 'outputs' folder
print ("Export the model to model.pkl")
f = open('./outputs/model.pkl', 'wb')
pickle.dump(prob, f)
f.close()