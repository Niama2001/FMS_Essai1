import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from src.navigation.trajectory_calculator import TrajectoryCalculator
from src.navigation.flight_planner import FlightPlan


class MapDisplay:
    def __init__(self, master, flight_plan: FlightPlan):
        self.master = master
        self.flight_plan = flight_plan
        self.trajectory_calculator = TrajectoryCalculator()

        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Plot Morocco boundaries
        self._plot_morocco_boundaries()

        # Plot waypoints and trajectory
        self._plot_flight_route()

    def _plot_morocco_boundaries(self):
        """Plot approximate Morocco boundaries."""
        # Moroccan boundary coordinates (simplified)
        lat_min, lat_max = 21.4, 36.0
        lon_min, lon_max = -17.0, -1.0

        # Fill background
        self.ax.set_facecolor('#F0F0F0')

        # Plot country boundaries
        self.ax.plot([lon_min, lon_max, lon_max, lon_min, lon_min],
                     [lat_min, lat_min, lat_max, lat_max, lat_min],
                     color='black', linewidth=2)

        self.ax.set_xlim(lon_min - 1, lon_max + 1)
        self.ax.set_ylim(lat_min - 1, lat_max + 1)
        self.ax.set_title('Moroccan Flight Route')
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        self.ax.grid(True, linestyle='--', alpha=0.7)

    def _plot_flight_route(self):
        """Plot flight route with waypoints."""
        route_waypoints = self.flight_plan.get_flight_route()

        # Extract coordinates
        lats = [wp.latitude for wp in route_waypoints]
        lons = [wp.longitude for wp in route_waypoints]

        # Plot trajectory
        trajectory = self.trajectory_calculator.calculate_trajectory(route_waypoints)
        traj_lats, traj_lons = zip(*trajectory)

        # Plot full trajectory
        self.ax.plot(traj_lons, traj_lats, 'b-', linewidth=2, label='Flight Path')

        # Plot waypoints
        self.ax.scatter(lons, lats, color='red', s=100, zorder=5)

        # Annotate waypoints
        for wp in route_waypoints:
            self.ax.annotate(wp.icao_code,
                             (wp.longitude, wp.latitude),
                             xytext=(5, 5),
                             textcoords='offset points')

        self.ax.legend()
        self.canvas.draw()

    def update_aircraft_position(self, position):
        """Update aircraft position on the map."""
        # Clear previous aircraft position
        for artist in self.ax.get_children():
            if isinstance(artist, plt.Line2D) and artist.get_label() == 'Aircraft':
                artist.remove()

        # Plot new aircraft position
        self.ax.plot(position[1], position[0], 'go', markersize=10, label='Aircraft')
        self.canvas.draw()


