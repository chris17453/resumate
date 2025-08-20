PYTHON=python3
PIP=pip3
PY_FILES=$(wildcard resumate/*.py)
DATA_DIR=data
#UUID:=$(shell uuidgen)
UUID="TEST"
RESUME_DIR=$(DATA_DIR)/$(UUID)
RESUME_YAML=$(RESUME_DIR)/resume.yaml
PDF_FILE=$(RESUME_DIR)/resume.pdf
TEMPLATE_PDF_FILE=template/resume-1.yaml


.PHONY: all clean install template load save generate_pdf generate_fake_resume generate_yaml_and_pdf

all: $(PDF_FILE)

template:
	$(PYTHON) -m resumate.cli template $(RESUME_YAML)

new_style:
	$(PYTHON) -m resumate.cli new_style $(TEMPLATE_PDF_FILE)

load:
	$(PYTHON) -m resumate.cli load $(RESUME_YAML)

save:
	$(PYTHON) -m resumate.cli save $(RESUME_YAML)

generate_pdf:
	$(PYTHON) -m resumate.cli generate_pdf $(RESUME_YAML)

chris:new_style
	$(PYTHON) -m resumate.cli generate_pdf data/cwatkins/watkins-chris-2024-05-resume.yaml


generate_fake:new_style
	$(PYTHON) -m resumate.cli generate_fake $(RESUME_YAML)
	$(PYTHON) -m resumate.cli generate_pdf $(RESUME_YAML)

flaten-rect:
	python resumate/svg_flatener.py --input submodules/logos/logos/aws-ec2.svg  --output submodules/logos/logos/aws-ec2-flatened.svg

flaten-path:
	python resumate/svg_flatener.py --input submodules/devicons/icons/python/python-original.svg  --output submodules/devicons/icons/python/python-original_flaten.svg

extract: template
	$(PYTHON) -m resumate.cli extract "$(TEMPLATE_PDF_FILE)"

install:
	$(PIP) install -r Pipfile

clean:
	rm -rf $(RESUME_DIR)
