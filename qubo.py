from dwave_qbsolv import QBSolv
import dimod
import hybrid
import neal
import itertools
import random
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Integer

Q = {(0, 0): 1, (1, 1): 1, (0, 1): 1}
response = QBSolv().sample_qubo(Q)
print("samples=" + str(list(response.samples())))
print("energies=" + str(list(response.data_vectors['energy'])))


qubo_size = 500
subqubo_size = 30
Q = {t: random.uniform(-1, 1) for t in itertools.product(range(qubo_size), repeat=2)}
sampler = neal.SimulatedAnnealingSampler()
response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=subqubo_size)
print("energies=" + str(list(response.data_vectors['energy'])))   # doctest: +SKIP
# energies=[-2800.794817495185]

#BQM
# Construct a problem
bqm = dimod.BinaryQuadraticModel({}, {'ab': 1, 'bc': -1, 'ca': 1}, 0, dimod.SPIN)

# Define the workflow
iteration = hybrid.RacingBranches(
    hybrid.InterruptableTabuSampler(),
    hybrid.EnergyImpactDecomposer(size=2)
    | hybrid.QPUSubproblemAutoEmbeddingSampler()
    | hybrid.SplatComposer()
) | hybrid.ArgMin()
workflow = hybrid.LoopUntilNoImprovement(iteration, convergence=3)

# Solve the problem
init_state = hybrid.State.from_problem(bqm)
final_state = workflow.run(init_state).result()

# Print results
print("Solution: sample={.samples.first}".format(final_state))