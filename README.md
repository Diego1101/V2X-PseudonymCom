# V2X Project SS24

This project provide a base to run multiple psuedonym change strategies, using the [Artery framework](http://artery.v2x-research.eu/), this work is partially based in [MobCom_Project_22WS](https://gitlab.hs-esslingen.de/dschoop/mobcom_project_22ws) and provides a simpler way to get starter with the code.


## Project Structure

The main folder is a clone of [artery repository](https://github.com/riebl/artery), the scenario to use can be found under "scenarios/pseudonym-changep" wich contains all the services and sumo files required for the simulation.

The attacker folder contains the python scrips used for the static attacker simulation and result analsys.

The artery simulation output "cam.txt" file that then has to be provided to the python attacker attacker in order to work, this file can be found under "scenarios/pseudonym-changep/results"


## Instalation 

This repository is based in the main brank for the [artery framework](http://artery.v2x-research.eu/install/), refer to artery documentation for installation.

## Execution of artery simulation

To exute the simulation first build the project

1. Create the folder "build" and navigate to it
2. Run
   ```
   make ..
   ```
3. Run
   ```
   cmake --build .
    ```
NOTE: Dont forget the point at the end of this command. The first time this command is executed the process might take a while, please be patient.

Once the project is build return to the main folder and run

``` 
cmake --build build --target run_pseudonym-changep
```

## Execution of python attacker

The code for the static attacker can be found under the directory "attacker", to run it its necessary to install the pandas library. It is recomended to run it using python3.
