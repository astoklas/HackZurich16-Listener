# HackZurich16-Listener

Example listener to process messages from the rabbitmq used in HackZurich16

##Quick Start
adapt env variable in docker-compose for the rabbitmq to the IP hosting the rabbitmq
docker-compose build
docker-compose up

## Configuration
### Grafana
Head over to the grafan board (running on port 3000), user:admin admin:C1sco123(default, change with env variable)
Add datasource influx db (http://influxdb:8086, proxy-access, no auth, add db HackZurich16 with root/root)
Add dashboard, add panel and add graph



### Influxdb
tbd
