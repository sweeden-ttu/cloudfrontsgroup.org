# Documentation

## Site

- [Writing a blog post](./blog-authoring.md): front matter fields, preview, and how to share posts to social media.
- [Design critique, 2026-10-30](./design-critique-2026-10-30.md): Site Design Critic report with a "Ship this" list and per-page media findings.
- [Media and logo generation prompts](./media-prompts.md): style lock, logo system, and a prompt for every image slot; machine-readable copy in `imagespecs/media-prompts.yml`; the SVG drawing contract is `imagespecs/svg-style-guide.md`.

Reference material kept alongside the cloudfrontsgroup.org site. These pages are repository documentation only; the Jekyll build excludes the `docs/` folder, so nothing here is published to the live site.

## VS Code agent customization

Offline copies of four VS Code documentation articles, captured 2026-10-28, that describe the formats used by the custom agents packaged as a plugin in [`.github/plugins/cloudfronts-site-agents/`](../.github/plugins/cloudfronts-site-agents/) and the instructions file in [`.github/instructions/`](../.github/instructions/). Each page was converted from PDF with [docling](https://github.com/docling-project/docling) and Tesseract OCR, then checked line by line against the PDF text layer and reformatted as GitHub-flavored Markdown (alerts, tables, fenced code, relative cross-links).

| Document | Covers | Source |
|----------|--------|--------|
| [Custom agents in VS Code](./custom-agents-in-vs-code.md) | `.agent.md` files, frontmatter, file locations, handoffs, subagent visibility | [code.visualstudio.com](https://code.visualstudio.com/docs/agent-customization/custom-agents) |
| [Use custom instructions in VS Code](./use-custom-instructions-in-vs-code.md) | `copilot-instructions.md`, `*.instructions.md`, `AGENTS.md`, `CLAUDE.md`, scope and activation | [code.visualstudio.com](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| [Configure agent hooks in Visual Studio Code (Preview)](./configure-agent-hooks.md) | Hook sources, events, command hooks, decisions, agent-scoped hooks | [code.visualstudio.com](https://code.visualstudio.com/docs/agent-customization/hooks) |
| [Agent plugins in VS Code](./agent-plugins-in-vs-code.md) | Installing, enabling, updating plugins, marketplaces, `/plugin` commands | [code.visualstudio.com](https://code.visualstudio.com/docs/agent-customization/agent-plugins) |

Screenshots live in [`images/`](./images/). Links whose targets were not recoverable from the PDFs are left as plain text rather than guessed.

## How these were produced

```bash
# in a Python environment with docling installed
export KMP_DUPLICATE_LIB_OK=TRUE
docling convert <pdf-folder> --from pdf --to md \
  --image-export-mode referenced \
  --ocr --ocr-engine tesseract --ocr-lang eng \
  --tables --table-mode accurate --enrich-code \
  --output <out-folder>
pdftotext -layout <file>.pdf <file>.txt   # reading-order reference for verification
```

The docling output supplied headings, source-section anchors, tables, and code blocks. The `pdftotext` layer supplied the authoritative sentence order, because PDF text runs for inline code often render out of sequence. Cookie-banner text, page footers, and print dates captured by the browser were removed.
