"""Checks for analytic reference values and deterministic generator behavior."""

import unittest

from experiments.mm1_validation import run_study, theoretical_metrics
from simulation.single_server_queue import SingleServerQueue


class ExperimentTests(unittest.TestCase):
    def test_mm1_reference_and_stability_boundary(self):
        self.assertEqual(theoretical_metrics(1.0, 0.5), {
            "average_queue_delay": 0.5,
            "average_queue_length": 0.5,
            "utilization": 0.5,
        })
        with self.assertRaises(ValueError):
            theoretical_metrics(1.0, 1.0)

    def test_seeded_replicates_are_reproducible(self):
        first, _ = run_study(customers=1000, replications=2)
        second, _ = run_study(customers=1000, replications=2)
        self.assertEqual(first, second)
        self.assertNotEqual(first[0]["average_queue_delay"], first[1]["average_queue_delay"])

    def test_rejects_invalid_queue_inputs(self):
        with self.assertRaises(ValueError):
            SingleServerQueue(0, 0.5, 100)
        with self.assertRaises(ValueError):
            SingleServerQueue(1, 0.5, 0)


if __name__ == "__main__":
    unittest.main()

