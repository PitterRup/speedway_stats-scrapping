#!/bin/bash

docker image rm -f speedway_parser
docker build -t speedway_parser .
docker container rm speedway_parser_app
docker create -p 5000:5000 -v /home/piotrek/Python/pge-ekstraliga/speedway_data_parser/:/app --name speedway_parser_app speedway_parser
