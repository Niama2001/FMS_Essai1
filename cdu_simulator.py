import tkinter as tk
from tkinter import messagebox, simpledialog
from src.database.waypoint_manager import WaypointManager
from src.navigation.flight_planner import FlightPlanner
from src.simulation.flight_simulator import FlightSimulator


class CDUSimulator:
    def __init__(self, master):
        self.master = master
        master.title("Flight Management System - CDU Simulator")
        master.geometry("800x600")

        # Initialize components
        self.waypoint_manager = WaypointManager()
        self.flight_planner = FlightPlanner(self.waypoint_manager)

        # Create main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create display screen
        self.display_screen = tk.Text(self.main_frame, height=10, width=80, font=('Courier', 12))
        self.display_screen.pack(pady=10)

        # Create button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Create buttons
        buttons = [
            ("INIT", self.init_flight),
            ("RTE", self.route_management),
            ("DEP/ARR", self.departure_arrival),
            ("LEGS", self.view_legs),
            ("DIR", self.direct_to_waypoint),
            ("FIX", self.set_reference_point),
            ("PERF", self.performance_settings),
            ("VNAV", self.vertical_navigation),
            ("PROG", self.flight_progress)
        ]

        # Layout buttons in a grid
        for i, (label, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=label, command=command, width=10)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def update_display(self, message):
        """Update the display screen with a message."""
        self.display_screen.delete(1.0, tk.END)
        self.display_screen.insert(tk.END, message)

    def init_flight(self):
        """Initialize flight settings."""
        aircraft_type = simpledialog.askstring("INIT", "Enter Aircraft Type:")
        weight = simpledialog.askfloat("INIT", "Enter Aircraft Weight (kg):")
        fuel = simpledialog.askfloat("INIT", "Enter Fuel Quantity (kg):")

        if aircraft_type and weight and fuel:
            message = f"Flight Initialized\n" \
                      f"Aircraft: {aircraft_type}\n" \
                      f"Weight: {weight} kg\n" \
                      f"Fuel: {fuel} kg"
            self.update_display(message)

    def route_management(self):
        """Manage flight route."""
        origin = simpledialog.askstring("RTE", "Enter Origin Airport ICAO Code:")
        destination = simpledialog.askstring("RTE", "Enter Destination Airport ICAO Code:")

        try:
            flight_plan = self.flight_planner.create_flight_plan(origin, destination)
            message = f"Route Plan:\n" \
                      f"Origin: {flight_plan.origin.name}\n" \
                      f"Destination: {flight_plan.destination.name}\n" \
                      f"Total Distance: {flight_plan.calculate_total_distance():.2f} km"
            self.update_display(message)
        except ValueError as e:
            messagebox.showerror("Route Error", str(e))

    def departure_arrival(self):
        """Configure departure and arrival procedures."""
        self.update_display("DEP/ARR: Select Departure and Arrival Procedures")

    def view_legs(self):
        """View and edit waypoint sequences."""
        self.update_display("LEGS: View Waypoint Sequence")

    def direct_to_waypoint(self):
        """Navigate directly to a specific waypoint."""
        waypoint_code = simpledialog.askstring("DIR", "Enter Waypoint ICAO Code:")
        waypoint = self.waypoint_manager.get_waypoint_by_code(waypoint_code)

        if waypoint:
            message = f"Direct To:\n" \
                      f"Waypoint: {waypoint.name}\n" \
                      f"Coordinates: {waypoint.latitude}, {waypoint.longitude}"
            self.update_display(message)
        else:
            messagebox.showerror("Waypoint Error", "Waypoint not found")

    def set_reference_point(self):
        """Set reference points for navigation."""
        self.update_display("FIX: Set Reference Point")

    def performance_settings(self):
        """Configure performance parameters."""
        self.update_display("PERF: Performance Settings")

    def vertical_navigation(self):
        """Configure vertical navigation profile."""
        self.update_display("VNAV: Vertical Navigation")

    def flight_progress(self):
        """Display flight progress information."""
        self.update_display("PROG: Flight Progress")

def run_cdu_simulator():
        root = tk.Tk()
        cdu_simulator = CDUSimulator(root)
        root.mainloop()
