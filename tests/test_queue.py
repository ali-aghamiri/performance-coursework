"""A statistical smoke test against the stable M/M/1 reference case."""
import contextlib
import io
import unittest

from simulation.single_server_queue import SingleServerQueue


class QueueSimulationTests(unittest.TestCase):
    def test_long_run_agrees_with_mm1_reference(self):
        sim = SingleServerQueue(1.0, 0.5, 100_000)
        with contextlib.redirect_stdout(io.StringIO()):
            sim.run_simulation()

        # Arrival rate 1/minute, service rate 2/minute: rho = Lq = Wq = 0.5.
        self.assertEqual(sim.num_custs_delayed, 100_000)
        self.assertAlmostEqual(sim.area_server_status / sim.sim_time, 0.5, delta=0.03)
        self.assertAlmostEqual(sim.area_num_in_q / sim.sim_time, 0.5, delta=0.04)
        self.assertAlmostEqual(sim.total_of_delays / sim.num_custs_delayed, 0.5, delta=0.04)


if __name__ == '__main__':
    unittest.main()
