from typing import List
from src.database.waypoint_manager import Waypoint, WaypointManager
from src.navigation.trajectory_calculator import TrajectoryCalculator


class FlightPlan:
    def __init__(self, origin: Waypoint, destination: Waypoint, waypoints: List[Waypoint] = None):
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints or []
        self.trajectory_calculator = TrajectoryCalculator()

    def calculate_total_distance(self) -> float:
        """Calculate total flight distance."""
        all_points = [self.origin] + self.waypoints + [self.destination]
        return sum(
            self.trajectory_calculator.calculate_great_circle_distance(all_points[i], all_points[i + 1])
            for i in range(len(all_points) - 1)
        )

    def get_flight_route(self) -> List[Waypoint]:
        """Get complete flight route including origin, waypoints, and destination."""
        return [self.origin] + self.waypoints + [self.destination]


class FlightPlanner:
    def __init__(self, waypoint_manager: WaypointManager):
        self.waypoint_manager = waypoint_manager
        self.trajectory_calculator = TrajectoryCalculator()

    def create_flight_plan(self, origin_code: str, destination_code: str,
                           waypoint_codes: List[str] = None) -> FlightPlan:
        """
        Create a flight plan with origin, destination, and optional waypoints.

        :param origin_code: ICAO code of origin airport
        :param destination_code: ICAO code of destination airport
        :param waypoint_codes: Optional list of waypoint ICAO codes
        :return: FlightPlan object
        """
        origin = self.waypoint_manager.get_waypoint_by_code(origin_code)
        destination = self.waypoint_manager.get_waypoint_by_code(destination_code)

        if not origin or not destination:
            raise ValueError("Invalid origin or destination waypoint")

        waypoints = []
        if waypoint_codes:
            for code in waypoint_codes:
                wp = self.waypoint_manager.get_waypoint_by_code(code)
                if wp:
                    waypoints.append(wp)
                else:
                    raise ValueError(f"Waypoint with code {code} not found")

        return FlightPlan(origin, destination, waypoints)

    def calculate_estimated_time_en_route(self, flight_plan: FlightPlan, avg_speed_knots: float = 450) -> float:
        """
        Calculate estimated time en route.

        :param flight_plan: FlightPlan object
        :param avg_speed_knots: Average aircraft speed in knots
        :return: Estimated time en route in hours
        """
        total_distance_nm = flight_plan.calculate_total_distance() * 0.539957  # Convert km to nautical miles
        return total_distance_nm / avg_speed_knots
