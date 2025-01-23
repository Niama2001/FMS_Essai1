from typing import List, Tuple
from src.navigation.flight_planner import FlightPlan
from src.navigation.trajectory_calculator import TrajectoryCalculator
from src.simulation.flight_simulator import AircraftState


class Autopilot:
    def __init__(self, flight_plan: FlightPlan):
        self.flight_plan = flight_plan
        self.trajectory_calculator = TrajectoryCalculator()
        self.current_state = None

    def engage(self, initial_state: AircraftState):
        """
        Engage autopilot with initial aircraft state.

        :param initial_state: Initial aircraft state
        """
        self.current_state = initial_state
        print("Autopilot engaged.")

    def navigate_to_waypoint(self, target_waypoint):
        """
        Navigate to a specific waypoint.

        :param target_waypoint: Waypoint to navigate to
        """
        if not self.current_state:
            raise ValueError("Autopilot not engaged. Call engage() first.")

        # Calculate bearing to waypoint
        bearing = self.trajectory_calculator.calculate_bearing(
            self.current_state.current_position,
            target_waypoint
        )

        # Adjust heading
        self.current_state.heading = bearing

        # Maintain altitude and speed
        print(f"Navigating to waypoint: {target_waypoint.name}")
        print(f"Adjusted heading to: {bearing}°")

    def maintain_altitude(self, target_altitude: float):
        """
        Maintain a specific altitude.

        :param target_altitude: Altitude to maintain in feet
        """
        if not self.current_state:
            raise ValueError("Autopilot not engaged. Call engage() first.")

        # Simple altitude adjustment logic
        altitude_diff = target_altitude - self.current_state.altitude

        if abs(altitude_diff) > 100:
            # Adjust climb/descent rate
            climb_rate = 500 if altitude_diff > 0 else -500
            self.current_state.altitude += climb_rate / 60  # per minute
            print(f"Adjusting altitude. Target: {target_altitude} ft, Current: {self.current_state.altitude} ft")

    def maintain_speed(self, target_speed: float):
        """
        Maintain a specific speed.

        :param target_speed: Speed to maintain in knots
        """
        if not self.current_state:
            raise ValueError("Autopilot not engaged. Call engage() first.")

        # Simple speed adjustment logic
        speed_diff = target_speed - self.current_state.speed

        if abs(speed_diff) > 10:
            # Adjust speed
            acceleration = 50 if speed_diff > 0 else -50
            self.current_state.speed += acceleration / 60  # per minute
            print(f"Adjusting speed. Target: {target_speed} knots, Current: {self.current_state.speed} knots")
