import tkinter as tk
from typing import Optional
from src.navigation.flight_planner import FlightPlan
from src.simulation.flight_simulator import AircraftState


class FlightDataPanel:
    def __init__(self, master, flight_plan: Optional[FlightPlan] = None):
        self.master = master
        self.flight_plan = flight_plan

        # Create main frame
        self.frame = tk.Frame(master, borderwidth=2, relief=tk.RAISED)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Flight Plan Information
        self.flight_plan_label = tk.Label(self.frame, text="Flight Plan", font=('Arial', 12, 'bold'))
        self.flight_plan_label.pack(pady=5)

        self.origin_label = tk.Label(self.frame, text="Origin: ")
        self.origin_label.pack()

        self.destination_label = tk.Label(self.frame, text="Destination: ")
        self.destination_label.pack()

        self.distance_label = tk.Label(self.frame, text="Total Distance: ")
        self.distance_label.pack()

        # Aircraft State Information
        self.aircraft_state_label = tk.Label(self.frame, text="Aircraft State", font=('Arial', 12, 'bold'))
        self.aircraft_state_label.pack(pady=5)

        self.position_label = tk.Label(self.frame, text="Position: ")
        self.position_label.pack()

        self.altitude_label = tk.Label(self.frame, text="Altitude: ")
        self.altitude_label.pack()

        self.speed_label = tk.Label(self.frame, text="Speed: ")
        self.speed_label.pack()

        self.heading_label = tk.Label(self.frame, text="Heading: ")
        self.heading_label.pack()

        # Update flight plan information if provided
        if flight_plan:
            self.update_flight_plan(flight_plan)

    def update_flight_plan(self, flight_plan: FlightPlan):
        """Update flight plan information."""
        self.flight_plan = flight_plan
        self.origin_label.config(text=f"Origin: {flight_plan.origin.name}")
        self.destination_label.config(text=f"Destination: {flight_plan.destination.name}")
        self.distance_label.config(text=f"Total Distance: {flight_plan.calculate_total_distance():.2f} km")

    def update_aircraft_state(self, aircraft_state: AircraftState):
        """Update aircraft state information."""
        self.position_label.config(text=f"Position: {aircraft_state.current_position}")
        self.altitude_label.config(text=f"Altitude: {aircraft_state.altitude:.2f} ft")
        self.speed_label.config(text=f"Speed: {aircraft_state.speed:.2f} knots")
        self.heading_label.config(text=f"Heading: {aircraft_state.heading:.2f}°")



