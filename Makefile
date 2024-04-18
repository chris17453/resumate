PYTHON=python3
PIP=pip3
PY_FILES=$(wildcard resumeonator/*.py)
DATA_DIR=data
#UUID:=$(shell uuidgen)
UUID="TEST"
RESUME_DIR=$(DATA_DIR)/$(UUID)
YAML_FILE=$(RESUME_DIR)/resume.yaml
PDF_FILE=$(RESUME_DIR)/resume.pdf
TEMPLATE_PDF_FILE=samples/Template V1 -Resume.pdf


.PHONY: all clean install template load save generate_pdf generate_fake_resume generate_yaml_and_pdf

all: $(PDF_FILE)

template:
	$(PYTHON) -m resumeonator.cli template $(YAML_FILE)

load:
	$(PYTHON) -m resumeonator.cli load $(YAML_FILE)

save:
	$(PYTHON) -m resumeonator.cli save $(YAML_FILE)

generate_pdf:
	$(PYTHON) -m resumeonator.cli generate_pdf $(YAML_FILE)


generate_fake:
	echo $(UUID)
	echo $(UUID)
	echo $(UUID)
	$(PYTHON) -m resumeonator.cli generate_fake $(YAML_FILE)
	$(PYTHON) -m resumeonator.cli generate_pdf $(YAML_FILE)


extract: template
	$(PYTHON) -m resumeonator.cli extract "$(TEMPLATE_PDF_FILE)"

install:
	$(PIP) install -r Pipfile

clean:
	rm -rf $(RESUME_DIR)
