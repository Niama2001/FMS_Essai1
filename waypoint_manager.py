import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os


@dataclass
class Waypoint:
    name: str
    icao_code: str
    latitude: float
    longitude: float
    type: str
    elevation: float = 0.0


class WaypointManager:
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = os.path.join(os.path.dirname(__file__), 'moroccan_waypoints.json')
        self.database_path = database_path
        self.waypoints = self._load_waypoints()

    def _load_waypoints(self) -> List[Waypoint]:
        """Load initial Moroccan waypoints."""
        default_waypoints = [
            Waypoint(
                name="Casablanca VOR",
                icao_code="CAS",
                latitude=33.365,
                longitude=-7.586,
                type="VOR"
            )
        ]

        try:
            with open(self.database_path, 'r') as f:
                saved_waypoints = json.load(f)
                return [Waypoint(**wp) for wp in saved_waypoints]
        except FileNotFoundError:
            self._save_waypoints(default_waypoints)
            return default_waypoints

    def _save_waypoints(self, waypoints: List[Waypoint]):
        """Save waypoints to JSON file."""
        with open(self.database_path, 'w') as f:
            json.dump([asdict(wp) for wp in waypoints], f, indent=2)

    def add_waypoint(self, waypoint: Waypoint) -> bool:
        """Add a new waypoint to the database."""
        if not self._is_in_morocco(waypoint.latitude, waypoint.longitude):
            raise ValueError("Waypoint must be located in Morocco")

        # Check for duplicate
        if any(wp.icao_code == waypoint.icao_code for wp in self.waypoints):
            return False

        self.waypoints.append(waypoint)
        self._save_waypoints(self.waypoints)
        return True

    def get_waypoint_by_code(self, icao_code: str) -> Optional[Waypoint]:
        """Retrieve a waypoint by its ICAO code."""
        return next((wp for wp in self.waypoints if wp.icao_code == icao_code), None)

    def _is_in_morocco(self, latitude: float, longitude: float) -> bool:
        """
        Validate if coordinates are within Moroccan boundaries.
        Approximate boundaries of Morocco:
        - Latitude: 21.4° to 36.0° N
        - Longitude: -17.0° to -1.0° W
        """
        return (21.4 <= latitude <= 36.0) and (-17.0 <= longitude <= -1.0)
