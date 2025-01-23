import sys
import os
import tkinter as tk
from src.database.waypoint_manager import WaypointManager, Waypoint
from src.navigation.flight_planner import FlightPlanner
from src.navigation.trajectory_calculator import TrajectoryCalculator
from src.simulation.flight_simulator import FlightSimulator
from src.simulation.autopilot import Autopilot
from src.gui.cdu_simulator import CDUSimulator
from src.gui.map_display import MapDisplay
from src.gui.flight_data_panel import FlightDataPanel

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def demonstrate_waypoint_management():
    print("\n--- Waypoint Management Demonstration ---")
    waypoint_manager = WaypointManager()

    # Display existing waypoints
    print("Existing Waypoints:")
    for wp in waypoint_manager.waypoints:
        print(f"{wp.name} ({wp.icao_code}): {wp.latitude}, {wp.longitude}")

    # Add a new waypoint
    new_waypoint = Waypoint(
        name="Marrakech Menara Airport",
        icao_code="GMMX",
        latitude=31.6069,
        longitude=-8.0364,
        type="airport",
        elevation=240
    )

    try:
        if waypoint_manager.add_waypoint(new_waypoint):
            print("\nNew Waypoint Added Successfully:")
            print(f"{new_waypoint.name} ({new_waypoint.icao_code})")
        else:
            print("Waypoint already exists.")
    except ValueError as e:
        print(f"Error: {e}")


def demonstrate_flight_planning():
    print("\n--- Flight Planning Demonstration ---")
    waypoint_manager = WaypointManager()
    flight_planner = FlightPlanner(waypoint_manager)
    trajectory_calculator = TrajectoryCalculator()

    try:
        # Create a flight plan from Casablanca to Agadir
        flight_plan = flight_planner.create_flight_plan("GMMN", "GMAD")

        # Calculate total distance
        total_distance = flight_plan.calculate_total_distance()
        print(f"Flight Route: {flight_plan.origin.name} to {flight_plan.destination.name}")
        print(f"Total Distance: {total_distance:.2f} km")

        # Calculate estimated time en route
        est_time = flight_planner.calculate_estimated_time_en_route(flight_plan)
        print(f"Estimated Time En Route: {est_time:.2f} hours")

        # Generate trajectory
        trajectory = trajectory_calculator.calculate_trajectory(flight_plan.get_flight_route())
        print(f"Trajectory Points: {len(trajectory)}")
    except Exception as e:
        print(f"Flight Planning Error: {e}")


def demonstrate_flight_simulation():
    print("\n--- Flight Simulation Demonstration ---")
    waypoint_manager = WaypointManager()
    flight_planner = FlightPlanner(waypoint_manager)

    try:
        # Create a flight plan
        flight_plan = flight_planner.create_flight_plan("GMMN", "GMAD")

        # Create flight simulator
        flight_simulator = FlightSimulator(flight_plan)

        # Create autopilot
        autopilot = Autopilot(flight_plan)

        # Start simulation
        flight_simulator.start_simulation()

        # Engage autopilot
        autopilot.engage(flight_simulator.current_state)

        # Simulate a few state updates
        print("Simulation Updates:")
        for _ in range(5):
            state = flight_simulator.update_aircraft_state()
            if state:
                print(f"Position: {state.current_position}")
                print(f"Altitude: {state.altitude:.2f} ft")
                print(f"Speed: {state.speed:.2f} knots")
                print(f"Heading: {state.heading:.2f}°")
                print("---")

                # Demonstrate autopilot functions
                autopilot.maintain_altitude(30000)
                autopilot.maintain_speed(450)
    except Exception as e:
        print(f"Simulation Error: {e}")


def launch_gui():
    print("\n--- Launching Flight Management System GUI ---")
    root = tk.Tk()
    root.title("Flight Management System")

    # Create main window with multiple panels
    waypoint_manager = WaypointManager()
    flight_planner = FlightPlanner(waypoint_manager)

    # Create a sample flight plan
    flight_plan = flight_planner.create_flight_plan("GMMN", "GMAD")

    # Create CDU Simulator
    cdu_frame = tk.Frame(root)
    cdu_frame.pack(side=tk.LEFT, padx=10, pady=10)
    tk.Label(cdu_frame, text="CDU Simulator", font=('Arial', 12, 'bold')).pack()
    cdu_simulator = CDUSimulator(cdu_frame)

    # Create Flight Data Panel
    data_frame = tk.Frame(root)
    data_frame.pack(side=tk.LEFT, padx=10, pady=10)
    tk.Label(data_frame, text="Flight Data Panel", font=('Arial', 12, 'bold')).pack()
    flight_data_panel = FlightDataPanel(data_frame, flight_plan)

    root.mainloop()


def main():
    print("Moroccan Flight Management System Demonstration")

    # Demonstrate key functionalities
    demonstrate_waypoint_management()
    demonstrate_flight_planning()
    demonstrate_flight_simulation()

    # Optional: Launch GUI
    launch_choice = input("\nDo you want to launch the GUI? (yes/no): ").lower()
    if launch_choice == 'yes':
        launch_gui()


if __name__ == "__main__":
    main()
