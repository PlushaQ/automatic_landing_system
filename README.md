# Automatic Airport Landing System

#### Note: This project is currently in the planning and developing phase.



## Welcome to the Automatic Airport Landing System project! 

This project is a simulation and no airplanes or passengers can be harmed :)

This ambitious project aims to create a sophisticated system for safely landing airplanes at an airport.
This system will manage the airspace, handle incoming planes, and ensure safe landings for all aircraft.

## Project Overview

### Technical Assumptions

    1. The system will be built using socket programming.
    2. Information about established connections, collisions, and successful landings will be stored in a database.
    3. Clients represent airplanes, and the server represents the automatic landing system.

### Business Assumptions

    1. The airport has two runways.
    2. The airport's airspace can accommodate a maximum of 100 airplanes. Any additional incoming airplanes will be informed to find an alternative airport.
    3. The airport manages a 10 km by 10 km airspace with a height limit of 5 km.
    4  Each incoming airplane has enough fuel for a 3-hour flight.
    5. Establishing air corridors for landing is essential.
    6. Airplanes appear randomly along the border of the airspace, outside the designated air corridors, at altitudes between 2 km and 5 km.
    7. Bringing an airplane to the ground involves directing it to an air corridor and ensuring a clear path to the runway. The airplane must be at ground level (0m) for a successful landing; otherwise, it's considered a failed landing and results in a collision.
    8. If two airplanes are within 10 meters of each other, it's considered a collision.
    9. If an airplane runs out of fuel while waiting, it's considered a collision.

### Project Goals

    1. Develop a robust server-client system for managing airplane landings.
    2. Implement algorithms to guide airplanes into designated air corridors and safely to the runway.
    3. Monitor and log successful landings, collisions, and other relevant data.
    4. Ensure efficient fuel management to prevent airplane collisions due to fuel exhaustion.

