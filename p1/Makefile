SHELL:=/bin/bash

.PHONY: build, start, stop, clean, dependencies

build:
	@docker-compose build

start:
	@docker-compose up -d

stop:
	@docker-compose down

test:
	@python3 -m pytest tests/

clean:
	@sudo rm -f /var/log/server.log
	@docker-compose down --rmi all

dependencies:
	sudo apt update && sudo apt upgrade
	sudo apt install linux-image-extra-$(uname -r) linux-image-extra-virtual
	sudo apt install apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
	sudo apt update && apt-cache policy docker-ce
	sudo apt install -y docker-ce
	sudo usermod -aG docker $(whoami)
	sudo apt install docker-compose

healthcheck:
	@if command -v docker > /dev/null;\
	then \
		echo "docker: ok";\
	else \
		echo "ERROR: docker is not installed";\
	fi;
	@if command -v docker-compose > /dev/null;\
	then \
		echo "docker: ok";\
	else \
		echo "ERROR: docker is not installed";\
	fi;
