import sys
import os
import unittest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.waypoint_manager import WaypointManager, Waypoint


class TestWaypointManager(unittest.TestCase):
    def setUp(self):
        self.waypoint_manager = WaypointManager()

    def test_add_valid_waypoint(self):
        new_waypoint = Waypoint(
            name="Agadir–Al Massira Airport",
            icao_code="GMAD",
            latitude=30.3753,
            longitude=-9.5478,
            type="airport"
        )
        self.assertTrue(self.waypoint_manager.add_waypoint(new_waypoint))

    def test_add_invalid_waypoint(self):
        invalid_waypoint = Waypoint(
            name="Invalid Airport",
            icao_code="INVALID",
            latitude=0,
            longitude=0,
            type="airport"
        )
        with self.assertRaises(ValueError):
            self.waypoint_manager.add_waypoint(invalid_waypoint)

    def test_get_waypoint_by_code(self):
        waypoint = self.waypoint_manager.get_waypoint_by_code("GMMN")
        self.assertIsNotNone(waypoint)
        self.assertEqual(waypoint.name, "Mohammed V International Airport")

    def test_duplicate_waypoint(self):
        duplicate_waypoint = Waypoint(
            name="Mohammed V International Airport",
            icao_code="GMMN",
            latitude=33.3675,
            longitude=-7.5898,
            type="airport"
        )
        self.assertFalse(self.waypoint_manager.add_waypoint(duplicate_waypoint))


if __name__ == '_main_':
    unittest.main()
