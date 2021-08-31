# Mobiliti_Analytics

This module provides tools for analytics for outputs from Mobiliti simulator. Mobiliti is a scalable transportation system simulator that implements parallel discrete event simulation on high-performance computers \cite{chan_mobiliti_2018}. We instantiate millions of nodes, links, and agents to simulate the movement of the population through the San Francisco Bay Area road network and provide estimates of the associated congestion, energy usage, and productivity loss. Our preliminary results show excellent scalability on multiple compute nodes for statically-routed agents, simulating 14 million trip legs  over a road network with 1.1 million nodes and 2.2 million links, processing 2.4 billion events in less than 30 seconds using 1,024 cores on NERSC's Cori computer.

Mobiliti outputs flows and speeds for every 15 minutes for a standard day. Flows are in veh/sec and speeds are in metre/sec units.
