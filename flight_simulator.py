import time
import random
from typing import List, Tuple
from src.database.waypoint_manager import Waypoint
from src.navigation.trajectory_calculator import TrajectoryCalculator
from src.navigation.flight_planner import FlightPlan


class AircraftState:
    def __init__(self, initial_waypoint: Waypoint):
        self.current_position = (initial_waypoint.latitude, initial_waypoint.longitude)
        self.altitude = 0  # feet
        self.speed = 0  # knots
        self.heading = 0  # degrees


class FlightSimulator:
    def __init__(self, flight_plan: FlightPlan):
        self.flight_plan = flight_plan
        self.trajectory_calculator = TrajectoryCalculator()
        self.trajectory = self._generate_trajectory()
        self.current_state = AircraftState(flight_plan.origin)
        self.simulation_time = 0
        self.is_running = False

    def _generate_trajectory(self) -> List[Tuple[float, float]]:
        """Generate smooth trajectory from flight plan."""
        route_waypoints = self.flight_plan.get_flight_route()
        return self.trajectory_calculator.calculate_trajectory(route_waypoints)

    def start_simulation(self):
        """Start the flight simulation."""
        self.is_running = True
        self.simulation_time = 0
        print("Flight simulation started.")

    def update_aircraft_state(self, time_step: float = 1.0):
        """
        Update aircraft state for each simulation time step.

        :param time_step: Time step in seconds
        """
        if not self.is_running:
            return None

        # Simulate movement along trajectory
        if len(self.trajectory) > 0:
            next_position = self.trajectory.pop(0)
            self.current_state.current_position = next_position

            # Simulate realistic aircraft parameters
            self.current_state.altitude += random.uniform(50, 200)
            self.current_state.speed = random.uniform(250, 450)

            # Calculate heading to next waypoint if trajectory is not empty
            if self.trajectory:
                self.current_state.heading = self.trajectory_calculator.calculate_bearing(
                    Waypoint(name="Current", icao_code="CURR",
                             latitude=self.current_state.current_position[0],
                             longitude=self.current_state.current_position[1], type="type"),
                    Waypoint(name="Next", icao_code="NEXT",
                             latitude=self.trajectory[0][0],
                             longitude=self.trajectory[0][1], type="type")
                )

            self.simulation_time += time_step

        # Check if simulation is complete
        if len(self.trajectory) == 0:
            self.is_running = False
            print("Flight simulation completed.")

        return self.current_state

    def run_simulation(self, update_interval: float = 1.0):
        """
        Run full flight simulation with real-time updates.

        :param update_interval: Time between state updates in seconds
        """
        self.start_simulation()

        while self.is_running:
            state = self.update_aircraft_state(update_interval)
            if state:
                print(f"Time: {self.simulation_time}s")
                print(f"Position: {state.current_position}")
                print(f"Altitude: {state.altitude} ft")
                print(f"Speed: {state.speed} knots")
                print(f"Heading: {state.heading}°")
                print("---")

            time.sleep(update_interval)
