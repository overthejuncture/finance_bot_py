CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

init:
	cp .env.example .env
	sed -i -e "s/UID=0/UID=$(CURRENT_UID)/" .env
	sed -i -e "s/GID=0/GID=$(CURRENT_GID)/" .env
	docker compose run python python -m venv venv
	docker compose run python python -m pip install -r requirements.txt
	docker compose run python python -m pip install git+https://github.com/overthejuncture/bot_helper_py.git
