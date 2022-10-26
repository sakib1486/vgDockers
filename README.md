# Virtual Gym Backend 

## Author
|Student name|     Email      |
|------------|---------------|
|   Sakib Hasan   |  sakib2@ualberta  |

This repository contains all the necessary scripts and docker containers that Virtual Gym backend requires. This project was done as a part of completion
requirements of the  Master's in Computing Science(crse) at the University of Alberta. The project was specifically done under the supervision
of Dr. Eleni Stroulia who mentored the CMPUT 701 for the student.

<details open="open">
<summary>Table of Content</summary>

- [High Level Overview](#about)
- [Folders and Files](#folders)
- [Usage](#usage)
- [Report](#report)

</details>

## High Level Overview

Users play Virtual Gym on a VR headset. We have mostly worked with the Oculus Quest 2, however the system is designed to be generalizable to other headsets. 
The Virtual Gym app contains a collection of smaller games such as *Slice Saber* and *Balloon Party*. A **session** is what we call a playthrough of 
a single mini game. As a session is being played, data is being sent through a websocket to our server. The server is a PC running Ubuntu in the SSRG lab 
[here](http://129.128.184.214)). Users can see statistics about their progress, scores, and fitness.

## Folders and Files
- _APIs_ : directory containing the docker-compose file and scripts to run the FAST APIs built upon python which helps communicate among different parts of the Virtual Gym.
- _Kafka_ : directory containing the docker-compose file required to launch the Apche Kafka for the backend.
- _crate_ : directory containing the docker-compose file required to launch the Crate DB required to store the streamed data.
- _jupyterlab_: directory containing the docker-compose file required to launch the jupyterlab notebooks to transfer data from Kafka to CrateDB through Apache Spark.
- _metrics.py_ : python script file which calculates the metrics for a completed session, and saves them back to a PostgreSQL and a Crate database. One might need to install a local postgres to make it work.

## Usage

Running the dockers have to be done in a serial manner After cloning the repo, navigate to the root directory. 

Firstly, to launch the Apache Kafka, run the followings:

`cd kafka`

`sudo docker-compose up -d`

`cd ..`

Once kafka is up, next to launch is CrateDB with:

`cd crate`

`sudo docker-compose up -d`

`cd ..`

After this, jupyterlab needs to be run with:

`cd jupyterlab`

`sudo docker-compose up -d`

`cd ..`

And, finally we launch the APIs needed to communicate with:

`cd APIs`

`sudo docker-compose up -d`

`cd ..`

After launching all these, the dockers can be reached with public URL at:

_localhost:9021_ : Kafka Confluent Dashboard
_localhost:4200_ : CrateDB Dashboard
_localhost:8006_ : JupyterLab Dashboard
_locahost:8100/_ : APIs

The built up APIs's definition can be found [APIs/app/main.py](here). To use aparticular API, one need to use url like this:

`localhost:8100/{API direction}`

## Report

The final report for the project can be found [here](here).

## Virtual Gym Pipeline Documentation

The virtual gym overall pipeline and documentation is explained in [SoDa-TAP Documentation] (https://www.sodatap.ml/en/latest/useCases/virtualGym/).
