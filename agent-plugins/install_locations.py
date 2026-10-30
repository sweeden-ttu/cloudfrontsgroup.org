#!/usr/bin/env python3
"""
Install (or remove) the site agents into every project-level location the editors read.

  python3 agent-plugins/install_locations.py install
  python3 agent-plugins/install_locations.py uninstall
  python3 agent-plugins/install_locations.py status
  python3 agent-plugins/install_locations.py normalize-claude   # make .claude/settings.json path relative

What "install" does, all inside this repository:
  .github/agents/<name>.agent.md     copies of the Agent Plugins package agents (native VS Code /
                                     Copilot CLI / Copilot app workspace location)
  .github/skills/<name>/SKILL.md     copies of the package skills (workspace skills location)
  .vscode/settings.json              chat.plugins.enabled = true and chat.pluginLocations pointing
                                     at the Agent Plugins package (absolute path; VS Code does not
                                     expand variables here, so re-run on each machine)
Claude Code is covered separately by `claude plugin install --scope project` (see the Makefile),
which records the plugin in .claude/settings.json. Nothing is written to ~/.

Generated files are tracked in .github/agents/.generated and .github/skills/.generated so that
"uninstall" removes only what this script created.
"""
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE = ROOT / '.github' / 'plugins' / 'cloudfronts-site-agents'
PKG_AGENTS = PACKAGE / 'com.github.copilot' / 'agents'
PKG_SKILLS = PACKAGE / 'skills'
WS_AGENTS = ROOT / '.github' / 'agents'
WS_SKILLS = ROOT / '.github' / 'skills'
VSCODE_SETTINGS = ROOT / '.vscode' / 'settings.json'
CLAUDE_SETTINGS = ROOT / '.claude' / 'settings.json'
CLAUDE_MARKETPLACE = 'cloudfronts-agents'
CLAUDE_MARKETPLACE_PATH = './agent-plugins'
MANIFEST = '.generated'


def _sync(src_items, dest_dir, kind):
    """Copy src_items into dest_dir, remove previously generated items that no longer exist."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    manifest = dest_dir / MANIFEST
    previous = set(manifest.read_text().split()) if manifest.exists() else set()
    current = set()
    for src in src_items:
        dest = dest_dir / src.name
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        current.add(src.name)
        print(f'  {kind}: {dest.relative_to(ROOT)}')
    for stale in sorted(previous - current):
        target = dest_dir / stale
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
        elif target.exists():
            target.unlink()
        print(f'  removed stale {kind}: {target.relative_to(ROOT)}')
    manifest.write_text('\n'.join(sorted(current)) + '\n')


def _remove_generated(dest_dir, kind):
    manifest = dest_dir / MANIFEST
    if not manifest.exists():
        print(f'  {kind}: nothing generated in {dest_dir.relative_to(ROOT)}')
        return
    for name in manifest.read_text().split():
        target = dest_dir / name
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
        elif target.exists():
            target.unlink()
        print(f'  removed {kind}: {target.relative_to(ROOT)}')
    manifest.unlink()
    if not any(dest_dir.iterdir()):
        dest_dir.rmdir()


# ---- .vscode/settings.json (JSON with comments; edit textually so comments survive) ----

def _strip_jsonc(text):
    text = re.sub(r'(?m)^\s*//.*$', '', text)
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    return text


def _vscode_set_plugin_location(enable):
    path_key = str(PACKAGE)
    text = VSCODE_SETTINGS.read_text() if VSCODE_SETTINGS.exists() else '{\n}\n'
    data = json.loads(_strip_jsonc(text))
    locations = dict(data.get('chat.pluginLocations', {}))
    if enable:
        locations[path_key] = True
    else:
        locations.pop(path_key, None)

    block_re = re.compile(r'(?ms)^(\s*)"chat\.pluginLocations"\s*:\s*\{.*?\}\s*,?\s*\n')
    rendered = ''
    if locations:
        inner = ',\n'.join(f'    {json.dumps(k)}: {json.dumps(v)}' for k, v in locations.items())
        rendered = f'  "chat.pluginLocations": {{\n{inner}\n  }},\n'

    if block_re.search(text):
        text = block_re.sub(rendered, text, count=1)
    elif rendered:
        anchor = re.compile(r'(?m)^(\s*"chat\.plugins\.enabled"\s*:\s*true\s*,\s*\n)')
        if anchor.search(text):
            text = anchor.sub(lambda m: m.group(1) + rendered, text, count=1)
        else:
            text = text.replace('{\n', '{\n  "chat.plugins.enabled": true,\n' + rendered, 1)
    if enable and '"chat.plugins.enabled"' not in text:
        text = text.replace('{\n', '{\n  "chat.plugins.enabled": true,\n', 1)
    # keep the file valid: no trailing comma before the closing brace
    text = re.sub(r',(\s*\n\s*\}\s*)$', r'\1', text)
    json.loads(_strip_jsonc(text))  # raise if we broke it
    VSCODE_SETTINGS.write_text(text)
    state = 'registered' if enable else 'unregistered'
    print(f'  .vscode/settings.json: chat.pluginLocations {state} {path_key}')


def install():
    if not PKG_AGENTS.exists():
        sys.exit(f'package agents not found: {PKG_AGENTS}')
    print('Installing workspace agents and skills from', PACKAGE.relative_to(ROOT))
    _sync(sorted(PKG_AGENTS.glob('*.agent.md')), WS_AGENTS, 'agent')
    _sync(sorted(p for p in PKG_SKILLS.iterdir() if p.is_dir()), WS_SKILLS, 'skill')
    _vscode_set_plugin_location(True)


def uninstall():
    print('Removing generated workspace agents and skills')
    _remove_generated(WS_AGENTS, 'agent')
    _remove_generated(WS_SKILLS, 'skill')
    if VSCODE_SETTINGS.exists():
        _vscode_set_plugin_location(False)


def normalize_claude():
    """Keep the Claude marketplace path repo-relative so .claude/settings.json works in any clone."""
    if not CLAUDE_SETTINGS.exists():
        print('  .claude/settings.json: not present (run `claude plugin install --scope project` first)')
        return
    data = json.loads(CLAUDE_SETTINGS.read_text())
    src = data.get('extraKnownMarketplaces', {}).get(CLAUDE_MARKETPLACE, {}).get('source', {})
    if src.get('source') == 'directory' and src.get('path') != CLAUDE_MARKETPLACE_PATH:
        src['path'] = CLAUDE_MARKETPLACE_PATH
        CLAUDE_SETTINGS.write_text(json.dumps(data, indent=2) + '\n')
        print(f'  .claude/settings.json: marketplace path normalized to {CLAUDE_MARKETPLACE_PATH}')
    else:
        print('  .claude/settings.json: marketplace path already relative')


def status():
    for label, d in (('agents', WS_AGENTS), ('skills', WS_SKILLS)):
        m = d / MANIFEST
        names = m.read_text().split() if m.exists() else []
        print(f'{label}: {len(names)} generated in {d.relative_to(ROOT)}' + (': ' + ', '.join(names) if names else ''))
    if VSCODE_SETTINGS.exists():
        data = json.loads(_strip_jsonc(VSCODE_SETTINGS.read_text()))
        print('chat.plugins.enabled:', data.get('chat.plugins.enabled'))
        print('chat.pluginLocations:', json.dumps(data.get('chat.pluginLocations', {}), indent=2))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'install'
    {'install': install, 'uninstall': uninstall, 'status': status, 'normalize-claude': normalize_claude}[cmd]()
