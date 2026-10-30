# Makefile for cloudfrontsgroup.org
#
# Jekyll is LOCAL PREVIEW ONLY. GitHub Pages serves this repo as raw files
# (.nojekyll). Root pages are assembled by _build/build.py from _partials/ + _pages/.
# Run `make help` for the target list.

SHELL        := /bin/bash
.DEFAULT_GOAL := help

# Ruby comes from rbenv (.ruby-version); prepend its shims so `bundle` resolves.
export PATH := $(HOME)/.rbenv/shims:$(HOME)/.rbenv/bin:/opt/homebrew/bin:$(PATH)
export JEKYLL_ENV ?= development

BUNDLE   := bundle
JEKYLL   := $(BUNDLE) exec jekyll
PYTHON   := python3
HOST     := 127.0.0.1
PORT     := 4000
LR_PORT  := 35729

PLUGIN_MARKETPLACE := ./agent-plugins
PLUGIN_NAME        := cloudfronts-site-agents
MARKETPLACE_NAME   := cloudfronts-agents
PLUGIN_ID          := $(PLUGIN_NAME)@$(MARKETPLACE_NAME)
PLUGIN_DIR         := $(PLUGIN_MARKETPLACE)/plugins/$(PLUGIN_NAME)
PLUGIN_SCOPE       := project

.PHONY: help install build serve stop clean rebuild assemble snapshot parity check \
        plugin plugin-build plugin-validate plugin-install plugin-uninstall plugin-reinstall plugin-list

##@ Help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: make <target>\n"} \
	     /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 } \
	     /^##@/ { printf "\n%s\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo

##@ Jekyll (local preview)
install: ## bundle install — Jekyll and dependencies from the Gemfile
	$(BUNDLE) install

build: ## bundle exec jekyll build — one-shot build into _site/
	$(JEKYLL) build --trace

serve: ## bundle exec jekyll serve --livereload at http://$(HOST):$(PORT)
	$(JEKYLL) serve --livereload --incremental --trace --host $(HOST) --port $(PORT)

stop: ## Kill whatever is listening on the serve and livereload ports
	-lsof -ti tcp:$(PORT) | xargs kill 2>/dev/null
	-lsof -ti tcp:$(LR_PORT) | xargs kill 2>/dev/null
	@echo "Jekyll server stopped."

clean: ## bundle exec jekyll clean — remove _site/ and .jekyll-cache/
	$(JEKYLL) clean

rebuild: clean build ## clean then build

##@ Site assembly and parity
assemble: ## python3 _build/build.py — regenerate root HTML from _pages/ + _partials/
	$(PYTHON) _build/build.py

snapshot: ## Copy current root HTML into _baseline/ before a Jekyll migration
	$(PYTHON) scripts/compare_build.py snapshot

parity: build ## jekyll build, then diff _site/ against _baseline/ (whitespace-normalized)
	$(PYTHON) scripts/compare_build.py compare

check: assemble parity ## assemble pages, build, and run the parity check

##@ Agent plugin (cloudfronts-site-agents)
plugin: plugin-build plugin-validate ## Regenerate and validate the plugin

plugin-build: ## Regenerate agents/ and skills/ from .github/agents/*.agent.md
	$(PYTHON) agent-plugins/build_plugin.py

plugin-validate: ## claude plugin validate on the marketplace and the plugin
	claude plugin validate $(PLUGIN_MARKETPLACE)
	claude plugin validate $(PLUGIN_DIR)

plugin-install: plugin ## Register the local marketplace and install at project scope
	-claude plugin marketplace add $(PLUGIN_MARKETPLACE) --scope $(PLUGIN_SCOPE)
	claude plugin install $(PLUGIN_ID) --scope $(PLUGIN_SCOPE)
	@$(PYTHON) - <<-'PY'
		# Keep the marketplace path repo-relative so .claude/settings.json works in any clone.
		import json, pathlib
		p = pathlib.Path('.claude/settings.json'); s = json.loads(p.read_text())
		m = s.get('extraKnownMarketplaces', {}).get('$(MARKETPLACE_NAME)', {}).get('source', {})
		if m.get('source') == 'directory' and m.get('path') != '$(PLUGIN_MARKETPLACE)':
		    m['path'] = '$(PLUGIN_MARKETPLACE)'; p.write_text(json.dumps(s, indent=2) + '\n')
		    print('normalized marketplace path to $(PLUGIN_MARKETPLACE)')
	PY

plugin-uninstall: ## Uninstall the plugin and remove the marketplace from project scope
	-claude plugin uninstall $(PLUGIN_ID) --scope $(PLUGIN_SCOPE)
	-claude plugin marketplace remove $(MARKETPLACE_NAME) --scope $(PLUGIN_SCOPE)

plugin-reinstall: plugin-uninstall plugin-install ## Uninstall then install (picks up manifest changes)

plugin-list: ## Show the installed plugin and its components
	claude plugin list | grep -A4 '$(PLUGIN_NAME)' || true
	claude plugin details $(PLUGIN_NAME)
