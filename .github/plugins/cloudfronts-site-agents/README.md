# cloudfronts-site-agents

An [Agent Plugins 1.0](https://agent-plugins.org) package that bundles the custom agents used to maintain [cloudfrontsgroup.org](https://cloudfrontsgroup.org). Install it to get the agents in the **Agent** dropdown of VS Code chat (Copilot harness) and in GitHub Copilot CLI.

## Contents

| Component | Path | What it does |
|-----------|------|--------------|
| Agent | `com.github.copilot/agents/jekyll-modularizer.agent.md` | Coordinates the migration from the Python build to Jekyll layouts, includes and data files |
| Agent | `com.github.copilot/agents/jekyll-page-converter.agent.md` | Subagent-only worker that converts one page to front matter + body |
| Agent | `com.github.copilot/agents/jekyll-site-reviewer.agent.md` | Read-only reviewer: build, output parity, links, metadata, accessibility |
| Agent | `com.github.copilot/agents/ux-layout-judge.agent.md` | Scores layout and UX, recommends concrete CSS/HTML changes |
| Agent | `com.github.copilot/agents/jekyll-site-expert.agent.md` | Jekyll and GitHub Pages engineering help |
| Agent | `com.github.copilot/agents/site-content-editor.agent.md` | Copy review and writing in the site's voice |
| Agent | `com.github.copilot/agents/site-design-critic.agent.md` | Design critique and redesign of components |
| Agent | `com.github.copilot/agents/social-media-distributor.agent.md` | Turns a page or post into a social distribution kit |
| Skill | `skills/jekyll-site-conventions/SKILL.md` | The site's structure, placeholder-to-Liquid mapping and hard rules |

## Install

Pick one. All three are described in [docs/agent-plugins-in-vs-code.md](../../../docs/agent-plugins-in-vs-code.md).

### A. VS Code, from this folder (recommended while developing)

1. Open the Chat view and set **Session Target** to **Copilot**.
2. Select **Open Customizations** in the Chat title bar (or run **Chat: Open Customizations**).
3. Select **Plugins**, then the **+** next to **Workspace**.
4. Enter the absolute path of this folder, for example `/Users/you/cloudfrontsgroup.org/.github/plugins/cloudfronts-site-agents`.

Or run **Chat: Install Plugin from Source** from the Command Palette and paste the same path or the Git URL `https://github.com/sweeden-ttu/cloudfrontsgroup.org`.

### B. GitHub Copilot CLI

```bash
# from the published repository
copilot plugin install sweeden-ttu/cloudfrontsgroup.org:.github/plugins/cloudfronts-site-agents

# or register the repo as a marketplace, then install by qualified name
copilot plugin marketplace add sweeden-ttu/cloudfrontsgroup.org
copilot plugin install cloudfronts-site-agents@cloudfronts
```

VS Code automatically discovers plugins the CLI installs under `~/.copilot/installed-plugins/`.

### C. Workspace recommendation (automatic for teammates)

`.github/copilot/settings.json` in this repository registers the `cloudfronts` marketplace and enables `cloudfronts-site-agents@cloudfronts` by default for Copilot sessions. In the Local harness VS Code shows a one-time notification offering to install it.

## Verify

Open the **Agent Customizations** editor, select **Plugins**, and confirm `cloudfronts-site-agents` is listed and enabled. Then pick **Jekyll Site Reviewer** from the Agent dropdown and ask it to review the current changes. `Jekyll Page Converter` is intentionally hidden from the dropdown (`user-invocable: false`); the Modularizer calls it as a subagent.

## Layout

```text
cloudfronts-site-agents/
├── plugin.json                      Agent Plugins 1.0 manifest
├── README.md
├── skills/
│   └── jekyll-site-conventions/
│       └── SKILL.md
└── com.github.copilot/
    └── agents/
        ├── jekyll-modularizer.agent.md
        ├── jekyll-page-converter.agent.md
        ├── jekyll-site-reviewer.agent.md
        ├── ux-layout-judge.agent.md
        ├── jekyll-site-expert.agent.md
        ├── site-content-editor.agent.md
        ├── site-design-critic.agent.md
        └── social-media-distributor.agent.md
```

Bump `version` in `plugin.json` and in `.github/plugin/marketplace.json` when you change an agent, so installed copies pick up the update via **Check for and Apply Updates**.
