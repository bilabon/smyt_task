# -*- makefile -*-

# definitions
PROJECT       = smyt_task
HOST          = 127.0.0.1
PORT          = 8895

#PROJECT_TEST_TARGETS=data
PYTHONPATH=.:..

MANAGE=cd $(PROJECT) && PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings django-admin.py

manage:
ifndef CMD
	@echo Please, specify CMD argument to execute Django management command
else
	$(MAKE) clean
	$(MANAGE)  $(CMD)
endif

run:
	$(MAKE) clean
	$(MANAGE) runserver $(HOST):$(PORT)

shell:
	$(MAKE) clean
	$(MANAGE) shell

init_syncdb:
	$(MAKE) clean
	$(MANAGE) syncdb
	$(MAKE) manage -e CMD="migrate"

migrate_data:
	python generate.py smyt_task/apps/core/model.yml
	-$(MANAGE) schemamigration data --auto
	$(MANAGE) migrate data
	@echo Done

clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)
