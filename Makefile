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

# Agent Plugins 1.0 package (VS Code / Copilot CLI / Copilot app)
PACKAGE_DIR        := .github/plugins/cloudfronts-site-agents
INSTALLER          := $(PYTHON) agent-plugins/install_locations.py
COPILOT_MKT        := $(HOME)/.copilot/local-marketplaces/cloudfronts-local

.PHONY: help install build serve stop clean rebuild assemble snapshot parity check \
        plugin plugin-build plugin-validate plugin-install plugin-uninstall plugin-reinstall plugin-list \
        install-agents uninstall-agents agents-status claude-install claude-uninstall \
        vscode-install vscode-uninstall copilot-install copilot-uninstall

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

serve: ## bundle exec jekyll serve --livereload at http://127.0.0.1:4000
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

plugin-build: ## Regenerate agents/ and skills/ from $(PACKAGE_DIR)/com.github.copilot/agents/*.agent.md
	$(PYTHON) agent-plugins/build_plugin.py

plugin-validate: ## claude plugin validate on the marketplace and the plugin
	claude plugin validate $(PLUGIN_MARKETPLACE)
	claude plugin validate $(PLUGIN_DIR)

plugin-install: plugin ## Register the local marketplace and install at project scope
	-claude plugin marketplace add $(PLUGIN_MARKETPLACE) --scope $(PLUGIN_SCOPE)
	claude plugin install $(PLUGIN_ID) --scope $(PLUGIN_SCOPE)
	@$(INSTALLER) normalize-claude

plugin-uninstall: ## Uninstall the plugin and remove the marketplace from project scope
	-claude plugin uninstall $(PLUGIN_ID) --scope $(PLUGIN_SCOPE)
	-claude plugin marketplace remove $(MARKETPLACE_NAME) --scope $(PLUGIN_SCOPE)

plugin-reinstall: plugin-uninstall plugin-install ## Uninstall then install (picks up manifest changes)

plugin-list: ## Show the installed plugin and its components
	claude plugin list | grep -A4 '$(PLUGIN_NAME)' || true
	claude plugin details $(PLUGIN_NAME)

##@ Install agents into every project location
install-agents: plugin claude-install vscode-install ## Build the Claude plugin, install it (project scope), and install the VS Code package into .github/agents, .github/skills and .vscode
	@echo
	@$(MAKE) --no-print-directory agents-status

uninstall-agents: vscode-uninstall claude-uninstall ## Remove everything install-agents created in this project

agents-status: ## Show where the agents are installed
	@$(INSTALLER) status
	@claude plugin list 2>/dev/null | grep -A4 '$(PLUGIN_NAME)' || echo "claude plugin: not installed"

claude-install: plugin-install ## Alias: install the Claude Code plugin at project scope (.claude/settings.json)

claude-uninstall: plugin-uninstall ## Alias: uninstall the Claude Code plugin from project scope

vscode-install: ## Copy package agents/skills into .github/agents and .github/skills; register $(PACKAGE_DIR) in .vscode/settings.json chat.pluginLocations
	@$(INSTALLER) install

vscode-uninstall: ## Remove the generated .github/agents and .github/skills copies and the .vscode registration
	@$(INSTALLER) uninstall

copilot-install: ## GitHub Copilot CLI: install the package via a local wrapper marketplace (CLI installs are user-level; see package README)
	@command -v copilot >/dev/null || { echo "copilot CLI not found; skipping"; exit 0; }
	mkdir -p "$(COPILOT_MKT)/plugins"
	ln -sfn "$(CURDIR)/$(PACKAGE_DIR)" "$(COPILOT_MKT)/plugins/$(PLUGIN_NAME)"
	printf '%s\n' '{' '  "name": "cloudfronts-local",' '  "owner": { "name": "Cloud Fronts Group" },' '  "plugins": [' \
	  '    { "name": "$(PLUGIN_NAME)", "source": "./plugins/$(PLUGIN_NAME)", "version": "0.1.0" }' '  ]' '}' > "$(COPILOT_MKT)/marketplace.json"
	-copilot plugin marketplace add "$(COPILOT_MKT)"
	copilot plugin install $(PLUGIN_NAME)@cloudfronts-local || copilot plugin update $(PLUGIN_NAME)
	copilot plugin list | grep -i '$(PLUGIN_NAME)' || true

copilot-uninstall: ## GitHub Copilot CLI: remove the plugin and the local wrapper marketplace
	-copilot plugin uninstall $(PLUGIN_NAME)
	-copilot plugin marketplace remove cloudfronts-local
	rm -rf "$(COPILOT_MKT)"
