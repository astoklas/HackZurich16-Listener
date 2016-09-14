# HackZurich16-Listener

##Overview
Example listener to process messages from the rabbitmq used in HackZurich16. This example reads the data from the rabbitMQ, does a simple transformation and writes the data into an influx time series database. Grafana has been chosen for a simple visualization of values over time.
influxdb and grafana are from the official repository. 
The listener is written in python and dockerized based on a python:2.7-slim official image with all required packages.

##Quick Start
**Make sure to have the HackZurich16 project running first**.  
Adapt env variable in docker-compose for the rabbitmq to the IP hosting the rabbitmq!
docker-compose build (only required first time)
docker-compose up  

to shut down use docker-compose down

scaling with any of the tiers has not been tested!

## Configuration
### Grafana
Head over to the grafana board (running on port 15002), user:admin admin:C1sco123(default, change with env variable)
Add datasource influx db **(http://198.18.134.28:8086, proxy-access, no auth, add db HackZurich16 with root/root)**

![addDB](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/addDBnew.png)

Add dashboard  
![add Dashboard](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/addDash.png)

Add a Panel  
![add Panel](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/addPanel.png)

Adding Graphs, selecting DB and measurement HackZurich16. Maybe you need to wait a short period of time until all available fields have been populated.  
![add Graph 1](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/addData1.png)  
![add Graph 2](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/addData2.png)

Result  
![Result](https://github.com/astoklas/HackZurich16-Listener/blob/master/doc/panel.png)

### Influxdb
tbd
