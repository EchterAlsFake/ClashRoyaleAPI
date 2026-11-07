"""Build Markdown references and a fragment for the existing Server documentation portal."""

import html
import inspect
import json
from pathlib import Path

from clashroyaleapi import Client, models


def main():
    reference = json.loads(Path("docs/api-reference.json").read_text())
    endpoints = [
        "# Endpoint reference",
        "",
        "All 30 operations use GET. Query arguments are keyword-only.",
        "",
    ]
    sections = []
    for op in reference["operations"]:
        method = op["python_method"]
        signature = str(inspect.signature(getattr(Client, method)))
        text = f"## {method}\n\n`{op['method']} {op['path']}`\n\n```python\nawait client.{method}{signature}\n```\n\n{op['description']}\n"
        if any(p["name"] == "after" for p in op["parameters"]):
            text += f"\nAsync iterator: `client.iter_{method}(...)`.\n"
        endpoints.append(text)
        sections.append(
            f'<section class="section" id="{method}"><h2>{method}</h2><pre><code>{html.escape(op["method"] + " " + op["path"])}</code></pre><pre><code>{html.escape(method + signature)}</code></pre><p>{html.escape(op["description"])}</p></section>'
        )
    Path("docs/endpoints.md").write_text("\n".join(endpoints).rstrip() + "\n")
    model_lines = [
        "# Response models",
        "",
        "All fields are optional unless stated otherwise. Unknown fields are retained.",
        "",
    ]
    model_sections = []
    for name in models.__all__:
        cls = getattr(models, name)
        fields = "\n".join(f"{k}: {v.annotation}" for k, v in cls.model_fields.items())
        model_lines += [f"## {name}", "", "```text", fields, "```", ""]
        model_sections.append(
            f'<section class="section" id="model-{name}"><h2>{name}</h2><pre><code>{html.escape(fields)}</code></pre></section>'
        )
    Path("docs/models.md").write_text("\n".join(model_lines))
    # Render Markdown using a small build-time dependency, keeping runtime lean.
    import markdown

    guide = markdown.markdown(Path("docs/guide.md").read_text(), extensions=["fenced_code"])
    readme = markdown.markdown(Path("README.md").read_text(), extensions=["fenced_code"])
    nav = '<a href="#getting-started" class="nav-link">Getting started</a><a href="#guide" class="nav-link">User guide</a>'
    nav += "".join(
        f'<a href="#{o["python_method"]}" class="nav-link">{o["python_method"]}</a>'
        for o in reference["operations"]
    )
    nav += "".join(f'<a href="#model-{n}" class="nav-link">{n}</a>' for n in models.__all__)
    # README links to repository Markdown remain useful from the portal.
    readme = readme.replace(
        'href="docs/', 'href="https://github.com/EchterAlsFake/ClashRoyaleAPI/blob/main/docs/'
    )
    fragment = "\n".join(
        f"<!-- SLOT:{k} = {v} -->"
        for k, v in {
            "TITLE": "ClashRoyaleAPI",
            "HERO_TITLE": "ClashRoyaleAPI",
            "HERO_SUBTITLE": "Async Python client for all 30 documented official Clash Royale API endpoints.",
            "VERSION": "1.0.1",
            "GITHUB_URL": "https://github.com/EchterAlsFake/ClashRoyaleAPI",
            "PYPI_PACKAGE": "async-royale-client",
        }.items()
    )
    fragment += "\n<!-- BEGIN:SIDEBAR_NAV -->\n" + nav + "\n<!-- END:SIDEBAR_NAV -->\n"
    fragment += (
        '<!-- BEGIN:MAIN_CONTENT -->\n<section id="getting-started">'
        + readme
        + '</section><section id="guide">'
        + guide
        + "</section>"
        + "".join(sections + model_sections)
        + "\n<!-- END:MAIN_CONTENT -->\n"
    )
    Path("docs/clashroyaleapi.html").write_text(fragment)


if __name__ == "__main__":
    main()
