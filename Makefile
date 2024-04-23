PYTHON=python3
PIP=pip3
PY_FILES=$(wildcard resumate/*.py)
DATA_DIR=data
#UUID:=$(shell uuidgen)
UUID="TEST"
RESUME_DIR=$(DATA_DIR)/$(UUID)
YAML_FILE=$(RESUME_DIR)/resume.yaml
PDF_FILE=$(RESUME_DIR)/resume.pdf
TEMPLATE_PDF_FILE=template/resume-1.yaml


.PHONY: all clean install template load save generate_pdf generate_fake_resume generate_yaml_and_pdf

all: $(PDF_FILE)

template:
	$(PYTHON) -m resumate.cli template $(YAML_FILE)

new_style:
	$(PYTHON) -m resumate.cli new_style $(TEMPLATE_PDF_FILE)

load:
	$(PYTHON) -m resumate.cli load $(YAML_FILE)

save:
	$(PYTHON) -m resumate.cli save $(YAML_FILE)

generate_pdf:
	$(PYTHON) -m resumate.cli generate_pdf $(YAML_FILE)


generate_fake:new_style
	$(PYTHON) -m resumate.cli generate_fake $(YAML_FILE)
	$(PYTHON) -m resumate.cli generate_pdf $(YAML_FILE)


extract: template
	$(PYTHON) -m resumate.cli extract "$(TEMPLATE_PDF_FILE)"

install:
	$(PIP) install -r Pipfile

clean:
	rm -rf $(RESUME_DIR)
