"""Reproducible finite-run comparison with steady-state M/M/1 formulas."""

import argparse
import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulation.single_server_queue import SingleServerQueue


def theoretical_metrics(mean_interarrival, mean_service):
    if mean_interarrival <= 0 or mean_service <= 0:
        raise ValueError("Mean times must be positive")
    rho = mean_service / mean_interarrival
    if rho >= 1:
        raise ValueError("A steady-state M/M/1 queue requires utilization below 1")
    return {
        "average_queue_delay": mean_service * rho / (1 - rho),
        "average_queue_length": rho * rho / (1 - rho),
        "utilization": rho,
    }


def run_study(mean_interarrival=1.0, mean_service=0.5, customers=20_000,
              replications=5, first_seed=1973272912):
    theory = theoretical_metrics(mean_interarrival, mean_service)
    if customers < 1 or replications < 1:
        raise ValueError("Customers and replications must be positive")
    if not 1 <= first_seed <= SingleServerQueue.MODLUS - replications:
        raise ValueError("Seed range exceeds the generator's supported state")

    rows = []
    for index in range(replications):
        seed = first_seed + index
        result = SingleServerQueue(mean_interarrival, mean_service, customers,
                                   seed=seed).run_simulation(verbose=False)
        rows.append({"replication": index + 1, "seed": seed, **result})

    summary = {
        metric: {
            "simulated_mean": statistics.mean(row[metric] for row in rows),
            "simulated_sd": statistics.stdev(row[metric] for row in rows) if len(rows) > 1 else 0.0,
            "theoretical": value,
        }
        for metric, value in theory.items()
    }
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interarrival", type=float, default=1.0)
    parser.add_argument("--service", type=float, default=0.5)
    parser.add_argument("--customers", type=int, default=20_000)
    parser.add_argument("--replications", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1973272912)
    parser.add_argument("--csv", type=Path, help="optional path for per-replication results")
    args = parser.parse_args()
    rows, summary = run_study(args.interarrival, args.service, args.customers,
                              args.replications, args.seed)
    print("Metric                 Simulated mean     SD          M/M/1 theory")
    for name, result in summary.items():
        print(f"{name:23} {result['simulated_mean']:12.4f} {result['simulated_sd']:10.4f} {result['theoretical']:14.4f}")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()

