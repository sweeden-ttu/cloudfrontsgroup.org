# cloudfronts-site-agents

Four site-maintenance roles for cloudfrontsgroup.org, packaged as a plugin.

| Role | Agent | Skill (slash command) |
|------|-------|-----------------------|
| Jekyll Site Expert | `@agent-cloudfronts-site-agents:jekyll-site-expert` | `/cloudfronts-site-agents:jekyll-site-expert` |
| Site Design Critic | `@agent-cloudfronts-site-agents:site-design-critic` | `/cloudfronts-site-agents:site-design-critic` |
| Site Content Editor | `@agent-cloudfronts-site-agents:site-content-editor` | `/cloudfronts-site-agents:site-content-editor` |
| Social Media Distributor | `@agent-cloudfronts-site-agents:social-media-distributor` | `/cloudfronts-site-agents:social-media-distributor` |

## Install

Claude Code, from the repository root:

```
claude plugin marketplace add ./agent-plugins
claude plugin install cloudfronts-site-agents@cloudfronts-agents
```

Or load for one session only: `claude --plugin-dir ./agent-plugins/plugins/cloudfronts-site-agents`.

VS Code: Chat > Open Customizations > Plugins > "+" > enter the folder path
`agent-plugins/plugins/cloudfronts-site-agents` (or the marketplace folder `agent-plugins`).

## Editing

Do not edit `agents/` or `skills/` here. The source of truth is
`.github/plugins/cloudfronts-site-agents/com.github.copilot/agents/*.agent.md` (VS Code custom
agent format, with handoffs; that folder is itself the Agent Plugins 1.0 package VS Code and
Copilot CLI install, see its README). After changing those, run:

```
python3 agent-plugins/build_plugin.py
claude plugin validate ./agent-plugins
```

The generator maps VS Code tool names to Claude tool names and turns handoffs into a
"Suggested next steps" section. Bump `version` in `.claude-plugin/plugin.json` so installed
copies pick up the change on `claude plugin update`.
