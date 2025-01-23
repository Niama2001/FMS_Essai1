import sys
import os
import unittest
import math

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.navigation.trajectory_calculator import TrajectoryCalculator
from src.database.waypoint_manager import Waypoint


class TestTrajectoryCalculator(unittest.TestCase):
    def setUp(self):
        self.trajectory_calculator = TrajectoryCalculator()
        self.casablanca = Waypoint(
            name="Mohammed V International Airport",
            icao_code="GMMN",
            latitude=33.3675,
            longitude=-7.5898,
            type="airport"
        )
        self.agadir = Waypoint(
            name="Agadir–Al Massira Airport",
            icao_code="GMAD",
            latitude=30.3753,
            longitude=-9.5478,
            type="airport"
        )

    def test_great_circle_distance(self):
        distance = self.trajectory_calculator.calculate_great_circle_distance(
            self.casablanca, self.agadir
        )
        # Expected distance is approximately 460-470 km
        self.assertAlmostEqual(distance, 465, delta=20)

    def test_trajectory_calculation(self):
        trajectory = self.trajectory_calculator.calculate_trajectory([self.casablanca, self.agadir])

        # Check trajectory generation
        self.assertGreater(len(trajectory), 1)

        # Check first and last points
        self.assertEqual(trajectory[0], (self.casablanca.latitude, self.casablanca.longitude))
        self.assertEqual(trajectory[-1], (self.agadir.latitude, self.agadir.longitude))

    def test_calculate_bearing(self):
        bearing = self.trajectory_calculator.calculate_bearing(self.casablanca, self.agadir)

        # Bearing should be between 0 and 360 degrees
        self.assertTrue(0 <= bearing <= 360)


if __name__ == '_main_':
    unittest.main()
