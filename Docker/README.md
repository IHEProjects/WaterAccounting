# 20190904 task

* Docker environment for jupyter
* Small dataset as example
* Go through the codes, split different blocks based on the function (download, clip, calculate)
* GUI (area, layer, clip, calculate)
* 1st check after Marloes holiday
* Handout of how to use docker

# WaPOR

## [API Token](https://wapor.apps.fao.org/profile)

ae34c8743c4dc4b3c32d26501fcef18b0cc47464baaa87cceb1b10d5ee1096ba03ab36196d29fe07

# BIOS Virtualization

Enable Virtualization in BIOS

# Docker

* [Docker Osgeo GDAL](https://hub.docker.com/r/osgeo/gdal)
* [DockerImages](https://wiki.osgeo.org/wiki/DockerImages)
* [Docker Toolbox](https://docs.docker.com/toolbox/overview/)
* [Docker Community Edition](https://docs.docker.com/docker-for-windows/release-notes/)
* [Docker Volume Windows](https://stackoverflow.com/questions/33126271/how-to-use-volume-option-with-docker-toolbox-on-windows)

## Setup shared folder with docker

### Windows 7, VirtualBox

Use toolbox to install docker, it will create VirtualBox default machine (boot2docker.iso)

VirtualBox -> Settings -> Shared Folders

Add

* Folder Path: D:\20190904-Training_Oct
* Folder Name: d/20190904-Training_Oct
* Auto-mount
* Make Permanent

Docker CMD

* docker-machine ssh
* ls /d/20190904-Training_Oct

### Windows 10, Hyper-V

## Docker-machine

```
docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
default   *        virtualbox   Running   tcp://192.168.99.100:2376           v18.09.9

# docker-machine env
# export DOCKER_TLS_VERIFY="1"
# export DOCKER_HOST="tcp://192.168.99.100:2376"
# export DOCKER_CERT_PATH="C:\Users\qpa001\.docker\machine\machines\default"
# export DOCKER_MACHINE_NAME="default"
# export COMPOSE_CONVERT_WINDOWS_PATHS="true"
# # Run this command to configure your shell:
# # eval $("C:\Program Files\Docker Toolbox\docker-machine.exe" env)

docker-machine start default
docker-machine stop default
```

## Build and start docker

cmd window 1

```
cd D:\20190904-Training_Oct\Docker
docker build -t wapor/jupyter .
```

### Windows 7, VirtualBox

```
cd D:\20190904-Training_Oct
docker run -it --name jupyter -p 8888:8888 -v /d/20190904-Training_Oct:/notebooks wapor/jupyter
```

### Windows 10, Hyper-V

```
cd D:\20190904-Training_Oct
docker run -it --name jupyter -p 8888:8888 -v D:/20190904-Training_Oct:/notebooks wapor/jupyter
```

### Mac, Linux

```
cd /Volumes/QPan_T5/20190904-Training_Oct/
docker run -it --name jupyter -p 8888:8888 -v $(PWD):/notebooks wapor/jupyter

# docker run -d --name jupyter -p 8888:8888 -v $(PWD):/notebooks wapor/jupyter
```

## Access to runing docker

cmd window 2

```
docker exec -it jupyter bash

jupyter notebook list

cd /notebooks

gdalinfo --version
GDAL 3.1.0dev-650fc42f344a6a4c65f11eefc47c473e9b445a68, released 2019/08/25

python3 wapor_gdalwarp.py 
```

## Copy data to docker

```
docker cp /Volumes/QPan_T5/20190904-Training_Oct gdal:/
```

## Clean docker

```
docker system prune -f && docker volume prune -f && docker container prune -f
```

## Save docker images

```
docker save --output wapor_jupyter.tar wapor/jupyter
```

## Load docker images

```
docker load --input wapor_jupyter.tar
```
