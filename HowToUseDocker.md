# devika_docker

[devika](https://github.com/stitionai/devika) docker environment

## Prerequisite

Install docker and docker-compose.
This is sample steps for ubuntu 22.04.

```sh
sudo apt install gnome-terminal
sudo apt install docker-ce
sudo apt install docker-compose
```

Please see.
https://docs.docker.com/desktop/install/ubuntu/

## Setup

Execute following command:

```sh
$ cd && git clone https://github.com/nobu007/devika.git
```

## .env

Update .env for your environment.

```sh
$ cp .env.sample .env
$ vi .env
```

## config.toml

Update config.toml for your environment.

```sh
$ cp sample.config.toml config.toml
$ vi config.toml
```

## Run

### Docker build & run

```sh
$ cd ~/devika
$ docker-compose --env-file .env up --build
```

### Browse app

Browse http://localhost:3000/
