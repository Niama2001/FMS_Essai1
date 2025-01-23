# FMS_Essai1
Dans ce projet, nous avons essayé de developper chaque partie du FMS séparemment et les rassembler ensuite pour simuler le focntionnement global du Flight Management System.


flight_management_system/
│
├── src/
│   ├── _init_.py
│   ├── database/
│   │   ├── _init_.py
│   │   ├── waypoint_manager.py
│   │   └── moroccan_waypoints.json
│   │
│   ├── navigation/
│   │   ├── _init_.py
│   │   ├── trajectory_calculator.py
│   │   └── flight_planner.py
│   │
│   ├── gui/
│   │   ├── _init_.py
│   │   ├── cdu_simulator.py
│   │   ├── map_display.py
│   │   └── flight_data_panel.py
│   │
│   └── simulation/
│       ├── _init_.py
│       ├── flight_simulator.py
│       └── autopilot.py
│
├── tests/
│   ├── test_waypoint_manager.py
│   ├── test_trajectory_calculator.py
│   └── test_flight_simulator.py
│
├── requirements.txt
└── README.md
