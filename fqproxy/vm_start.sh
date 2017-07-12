#!/bin/bash
sudo docker run -i -t -d\
     -v /home/ubuntu/.cow/rc:/.cow/rc \
     --name proxy\
     -p 3129:7777\
     fqproxy
