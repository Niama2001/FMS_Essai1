import sys
import os
import unittest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.waypoint_manager import WaypointManager
from src.navigation.flight_planner import FlightPlanner
from src.simulation.flight_simulator import FlightSimulator


class TestFlightSimulator(unittest.TestCase):
    def setUp(self):
        self.waypoint_manager = WaypointManager()
        self.flight_planner = FlightPlanner(self.waypoint_manager)

        # Create a sample flight plan
        self.flight_plan = self.flight_planner.create_flight_plan("GMMN", "GMAD")
        self.flight_simulator = FlightSimulator(self.flight_plan)

    def test_flight_simulator_initialization(self):
        self.assertIsNotNone(self.flight_simulator.trajectory)
        self.assertEqual(self.flight_simulator.current_state.current_position[0], self.flight_plan.origin.latitude)
        self.assertEqual(self.flight_simulator.current_state.current_position[1], self.flight_plan.origin.longitude)

    def test_update_aircraft_state(self):
        # Start simulation
        self.flight_simulator.start_simulation()

        # Update state
        state = self.flight_simulator.update_aircraft_state()

        # Check state updates
        self.assertIsNotNone(state)
        self.assertNotEqual(state.altitude, 0)
        self.assertNotEqual(state.speed, 0)
        self.assertNotEqual(state.heading, 0)

    def test_simulation_completion(self):
        # Run simulation
        self.flight_simulator.start_simulation()

        # Exhaust trajectory
        while self.flight_simulator.is_running:
            self.flight_simulator.update_aircraft_state()

        # Check simulation completion
        self.assertFalse(self.flight_simulator.is_running)


if __name__ == '__main__':
    unittest.main()
