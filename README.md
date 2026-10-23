# Performance Evaluation Coursework

Coursework by Seyyed Ali Aghamiri on probability, queueing, and discrete-event simulation.

## Contents

- `reports/homework-1.pdf` to `homework-3.pdf`: submitted written assignments.
- `reports/additional-exercise.pdf`: another submitted exercise.
- `simulation/single_server_queue.py`: original Python implementation of a single-server queue simulator. It estimates queue delay, queue length, utilization, and end time from event arrivals/departures.
- `experiments/random_number_generator.py` and `reports/rng-project.pdf`: exploratory random-number-generator exercise and its submitted write-up.

## Run

```bash
python simulation/single_server_queue.py
python experiments/random_number_generator.py  # requires NumPy
python -m unittest discover -s tests
```

The queue program uses a fixed built-in scenario (mean interarrival 1 minute, mean service 0.5 minute, 1,000 delayed customers). It is a finite simulation, so its output need not equal the analytical M/M/1 averages. The second script is an exploratory exercise rather than a validated library.

The submitted reports have had the student number removed. Course textbooks, lecture material, blank templates, and incomplete zero-byte files are excluded.
