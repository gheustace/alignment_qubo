from dwave_qbsolv import QBSolv
import dimod
import hybrid
import neal
import itertools
import random
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Integer

cqm = ConstrainedQuadraticModel()

# Define the variables
x = Integer('x', lower_bound=-10, upper_bound=10)
y = Integer('y', lower_bound=-10, upper_bound=10)

# Add a quadratic objective
cqm.set_objective(2*x**2 - 3*y**2 + 2*x*y)

# Add a constraint
cqm.add_constraint(x + y == 1, label='constraint1')


# Setup the sampler from D-Wave Leap
sampler = LeapHybridCQMSampler(token='DEV-ea483650b914e36932343ac84e0ea4d1eaf31cbd')

# Sample the CQM
sampleset = sampler.sample_cqm(cqm)

# Print the results
for sample in sampleset:
    print(f"x: {sample['x']}, y: {sample['y']}")