.PHONY: dev.install db.migration.new db.migrate db.rollback

include .env
export

MIGRATIONS_DIR := migrations
DB_URL := postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)

dev.install:
	pip install -r requirements.txt

db.migration.new:
	yoyo new $(MIGRATIONS_DIR) -m "$(name)"

db.migrate:
	yoyo apply --database "$(DB_URL)" $(MIGRATIONS_DIR) --batch

db.rollback:
	yoyo rollback --database "$(DB_URL)" $(MIGRATIONS_DIR) --batch
