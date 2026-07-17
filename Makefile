PYTHON ?= python3
SKILLS_CLI_VERSION ?= 1.5.9
VERSION ?= v0.1.0

.PHONY: test list package

test:
	bash scripts/test.sh

list:
	npx -y skills@$(SKILLS_CLI_VERSION) add . --list

package:
	$(PYTHON) scripts/package_release.py --version $(VERSION) --output-dir dist
