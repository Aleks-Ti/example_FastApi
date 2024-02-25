ifeq (revision,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for run
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ... and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY:

start:
	poetry run uvicorn \
	--reload \
	--host 127.0.0.1 \
	--port 8000 \
	"sqlalchemy_practic.main:app"

user:
	python seed/create_data_test.py
