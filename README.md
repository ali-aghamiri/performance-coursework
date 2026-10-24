# Performance Evaluation Coursework

Coursework by Seyyed Ali Aghamiri on probability, queueing, and discrete-event simulation.

## Contents

- `reports/homework-1.pdf` to `homework-3.pdf`: submitted written assignments.
- `reports/additional-exercise.pdf`: another submitted exercise.
- `simulation/single_server_queue.py`: the submitted single-server discrete-event simulator, with parameter validation, a configurable seed, and reusable metrics.
- `experiments/mm1_validation.py`: a reproducible follow-up experiment comparing distinct-seed finite simulations with steady-state M/M/1 queue formulas.
- `experiments/random_number_generator.py` and `reports/rng-project.pdf`: the random-number-generator exercise and submitted write-up. The combined generator now uses integer arithmetic and the module can be imported without running the demo.

## Run

```bash
python simulation/single_server_queue.py
python simulation/single_server_queue.py --interarrival 1 --service 0.5 --customers 1000 --seed 1973272912
python experiments/mm1_validation.py --customers 20000 --replications 5 --csv results/mm1.csv
python experiments/random_number_generator.py  # requires NumPy
python -m unittest discover -s tests
```

The default queue scenario uses a mean interarrival time of 1 minute and mean service time of 0.5 minute. For this stable M/M/1 case, utilization, mean queue length, and mean queue delay are all 0.5. The validation experiment prints the simulated mean and standard deviation across runs alongside these theoretical values. Its runs stop after a fixed number of customers begin service, so finite-run results can differ from the steady-state formulas; these are not confidence intervals or hardware measurements. The simulator retains the original 100-customer waiting-room limit and raises an error if it is exceeded.

The PDF reports are the submitted course material. The validation experiment and code cleanup were added later to make the software easier to inspect and reproduce.

The submitted reports have had the student number removed. Course textbooks, lecture material, blank templates, and incomplete zero-byte files are excluded.

