#!/usr/bin/env python3
"""
Generate the Claude Code plugin from the VS Code agent definitions.

Source of truth: .github/agents/*.agent.md (VS Code custom agent format, with handoffs).
Output:          agent-plugins/plugins/cloudfronts-site-agents/{agents,skills}/

Usage:  python3 agent-plugins/build_plugin.py
Then:   claude plugin validate ./agent-plugins
"""
import re, pathlib, shutil, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '.github' / 'agents'
PLUGIN = ROOT / 'agent-plugins' / 'plugins' / 'cloudfronts-site-agents'
AGENTS = ['jekyll-site-expert', 'site-design-critic', 'site-content-editor', 'social-media-distributor']
TOOLMAP = {'read': ['Read', 'Glob'], 'search': ['Grep', 'Glob'], 'edit': ['Edit', 'Write'],
           'execute': ['Bash'], 'web': ['WebFetch', 'WebSearch'], 'agent': ['Agent'],
           'todo': ['TaskCreate', 'TaskUpdate']}
PLUGIN_NAME = 'cloudfronts-site-agents'

def parse(path):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', path.read_text(), re.S)
    return yaml.safe_load(m.group(1)), m.group(2).rstrip() + '\n'

def claude_tools(vs_tools):
    out = []
    for t in vs_tools or []:
        for c in TOOLMAP.get(t, []):
            if c not in out:
                out.append(c)
    return out

def next_steps(fm, heading):
    if not fm.get('handoffs'):
        return ''
    lines = ['', f'## {heading}',
             'There are no handoff buttons in this harness. End your report by naming the next role to run:']
    for h in fm['handoffs']:
        target = h['agent']
        if target != 'agent':
            slug = target.lower().replace(' ', '-')
            target = f'`{PLUGIN_NAME}:{slug}`' if slug in AGENTS else f'`{target}` (VS Code only; here, describe the task to the default agent)'
        else:
            target = 'the default agent'
        lines.append(f"- **{h['label']}** -> {target}: {h['prompt']}")
    return '\n'.join(lines) + '\n'

def one_line(s):
    return ' '.join(s.split())

def y(value):
    """Render one scalar as a safe single-line YAML value."""
    return yaml.safe_dump(one_line(value), default_style='"', width=10**6).strip()

for d in (PLUGIN / 'agents', PLUGIN / 'skills'):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)

for slug in AGENTS:
    fm, body = parse(SRC / f'{slug}.agent.md')
    tools = claude_tools(fm.get('tools'))
    desc = one_line(fm['description'])

    # --- agent (Claude subagent format) ---
    agent = ['---', f'name: {slug}', f'description: {y(desc)}', 'tools: ' + ', '.join(tools),
             'model: inherit', '---', '', body.rstrip(), '',
             next_steps(fm, 'Suggested next steps').rstrip(), '']
    (PLUGIN / 'agents' / f'{slug}.md').write_text('\n'.join(agent).lstrip('\n'))

    # --- skill (slash command / auto-invoked workflow) ---
    skill_dir = PLUGIN / 'skills' / slug
    skill_dir.mkdir()
    hint = fm.get('argument-hint', '')
    skill = ['---', f'name: {slug}', f'description: {y(desc)}']
    if hint:
        skill.append(f'argument-hint: {y(hint)}')
    skill += ['---', '',
              f'# {fm["name"]}', '',
              f'Request from the user: $ARGUMENTS', '',
              f'Run this workflow yourself for small, focused requests. For anything that touches more than a few files, '
              f'needs a browser session, or would flood the main conversation with build output, delegate the whole '
              f'task to the `{PLUGIN_NAME}:{slug}` subagent with the request above and relay its report.', '',
              body.rstrip(), '', next_steps(fm, 'Suggested next steps').rstrip(), '']
    (skill_dir / 'SKILL.md').write_text('\n'.join(skill))
    print(f'generated agents/{slug}.md and skills/{slug}/SKILL.md  (tools: {", ".join(tools)})')
