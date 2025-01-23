import numpy as np
from typing import List, Tuple
from src.database.waypoint_manager import Waypoint


class TrajectoryCalculator:
    @staticmethod
    def calculate_great_circle_distance(wp1: Waypoint, wp2: Waypoint) -> float:
        """
        Calculate great-circle distance between two waypoints.
        Returns distance in kilometers.
        """
        # Earth's radius in kilometers
        R = 6371.0

        # Convert latitude and longitude to radians
        lat1, lon1 = np.radians(wp1.latitude), np.radians(wp1.longitude)
        lat2, lon2 = np.radians(wp2.latitude), np.radians(wp2.longitude)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) * 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) * 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c

    def calculate_trajectory(self, waypoints: List[Waypoint], num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Calculate interpolated trajectory between waypoints.

        :param waypoints: List of Waypoint objects
        :param num_points: Number of interpolation points
        :return: Interpolated trajectory points as (latitude, longitude)
        """
        if len(waypoints) < 2:
            return [(wp.latitude, wp.longitude) for wp in waypoints]

        trajectory = []

        for i in range(len(waypoints) - 1):
            start_wp = waypoints[i]
            end_wp = waypoints[i + 1]

            # Linear interpolation (simplified)
            lats = np.linspace(start_wp.latitude, end_wp.latitude, num_points)
            lons = np.linspace(start_wp.longitude, end_wp.longitude, num_points)

            trajectory.extend(zip(lats, lons))

        return trajectory

    def calculate_bearing(self, wp1: Waypoint, wp2: Waypoint) -> float:
        """
        Calculate initial bearing between two waypoints.
        Returns bearing in degrees.
        """
        # Convert latitude and longitude to radians
        lat1, lon1 = np.radians(wp1.latitude), np.radians(wp1.longitude)
        lat2, lon2 = np.radians(wp2.latitude), np.radians(wp2.longitude)

        # Calculate bearing
        dlon = lon2 - lon1
        y = np.sin(dlon) * np.cos(lat2)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)

        # Convert to degrees and normalize
        initial_bearing = np.degrees(np.arctan2(y, x))
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing
