#!usr/bin/env python

# Objective function with constraints to optimize
# Author: Sandeep Baskar

def objective_function(X):
    # Make your own objective function here
    # Define constraints if any
    constraint_1 = (X[1] <= 3.2) or (X[1] >= 6.4);
    constraint_2 = ((X[0] ** 2 + X[1] ** 2) >= 1);
    constraint_3 = (X[0] != X[1]);

    # Penalty function
    def penalty_objective():
        # Add penalty function for violating constraints if desired
        return 200

    if ((constraint_1 == True) and (constraint_2 == True) and (constraint_3 == True)):
        o = sum((X)**2)
    else:
        o = penalty_objective()

    return o
