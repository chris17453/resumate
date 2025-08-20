PYTHON=python3
PIP=pip3
PY_FILES=$(wildcard resumate/*.py)
DATA_DIR=data
UUID="TEST"
RESUME_DIR=$(DATA_DIR)/$(UUID)
RESUME_YAML=$(RESUME_DIR)/resume.yaml
PDF_FILE=$(RESUME_DIR)/resume.pdf
TEMPLATE_PDF_FILE=template/resume-1.yaml

# Package info
VERSION=$(shell python -c "print(open('setup.py').read().split('version=')[1].split(',')[0].strip('\"'))")
PACKAGE_NAME=resumate

.PHONY: all clean install template load save generate_pdf generate_fake_resume generate_yaml_and_pdf
.PHONY: build test-release release clean-build check-version

all: $(PDF_FILE)

# Development commands
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

chris: new_style
	$(PYTHON) -m resumate.cli generate_pdf data/cwatkins/chris2.yaml

generate_fake: new_style
	$(PYTHON) -m resumate.cli generate_fake $(RESUME_YAML)
	$(PYTHON) -m resumate.cli generate_pdf $(RESUME_YAML)

xtract: template
	$(PYTHON) -m resumate.cli extract "$(TEMPLATE_PDF_FILE)"

install:
	$(PIP) install -r requirements.txt

# Package building and PyPI release
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build-deps:
	$(PIP) install --upgrade pip setuptools wheel twine build

build: clean-build
	@echo "Building $(PACKAGE_NAME) version $(VERSION)..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "Build complete. Files in dist/:"
	@ls -la dist/

check: build
	twine check dist/*

test-install: build
	$(PIP) uninstall -y $(PACKAGE_NAME) || true
	$(PIP) install dist/*.whl
	resumate list_templates

test-release: check
	@echo "Uploading to TestPyPI..."
	twine upload --repository testpypi dist/*
	@echo "Test with: pip install --index-url https://test.pypi.org/simple/ $(PACKAGE_NAME)"

release: check
	@echo "Releasing $(PACKAGE_NAME) version $(VERSION) to PyPI..."
	@echo "Files to upload:"
	@ls -la dist/
	@read -p "Are you sure you want to upload to PyPI? [y/N] " confirm && [ "$$confirm" = "y" ]
	twine upload dist/*
	@echo "Released! Install with: pip install $(PACKAGE_NAME)"

tag-release:
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin v$(VERSION)

full-release: build check test-install release tag-release
	@echo "Full release complete!"

# Development helpers
dev-install:
	$(PIP) install -e .

check-version:
	@echo "Current version: $(VERSION)"
	@echo "PyPI versions:"
	@$(PIP) index versions $(PACKAGE_NAME) 2>/dev/null || echo "Package not yet on PyPI"

clean: clean-build
	rm -rf $(RESUME_DIR)

# Help target
help:
	@echo "Resumate Makefile"
	@echo ""
	@echo "Development targets:"
	@echo "  make install          - Install dependencies"
	@echo "  make dev-install      - Install package in development mode"
	@echo "  make chris            - Generate Chris's resume"
	@echo "  make generate_fake    - Generate fake resume for testing"
	@echo ""
	@echo "Build & Release targets:"
	@echo "  make clean-build      - Clean build artifacts"
	@echo "  make build            - Build package distributions"
	@echo "  make check            - Check package with twine"
	@echo "  make test-install     - Test install locally"
	@echo "  make test-release     - Upload to TestPyPI"
	@echo "  make release          - Upload to PyPI (will prompt for confirmation)"
	@echo "  make full-release     - Build, test, release, and tag"
	@echo ""
	@echo "Utility targets:"
	@echo "  make check-version    - Show current version and PyPI versions"
	@echo "  make clean            - Clean all generated files"