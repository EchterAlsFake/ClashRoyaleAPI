"""Build task-oriented docs using the existing EAF portal's colors and components."""

from __future__ import annotations

import html
import inspect
import json
import types
from pathlib import Path
from typing import Any, Union, get_args, get_origin

import markdown
from bs4 import BeautifulSoup
from pygments import lex
from pygments.lexers import BashLexer, PowerShellLexer, PythonLexer, TextLexer
from pygments.token import Token

from clashroyaleapi import Client, __version__, models

GROUPS = {
    "players": ("Players", "Profiles, upcoming chests and recent battles."),
    "clans": ("Clans & river races", "Find clans, read their members and follow clan wars."),
    "cards": ("Cards", "Browse the card catalog, including preserved supportItems data."),
    "tournaments": ("Tournaments", "Search player-created tournaments and fetch details."),
    "locations": (
        "Locations & rankings",
        "Regions, seasons, historical rankings and Path of Legend.",
    ),
    "events": ("Events", "Current in-game events and their descriptions."),
    "leaderboards": (
        "Leaderboards",
        "Discover leaderboard IDs and fetch their ranked player entries.",
    ),
    "globaltournaments": (
        "Global tournaments",
        "Global tournament metadata, when an event is advertised.",
    ),
}
PARAMETERS = {
    "player_tag": "Player tag from an in-game profile or a clan member. A leading # is optional.",
    "clan_tag": "Clan tag returned by search_clans() or a player profile. A leading # is optional.",
    "tournament_tag": "Tournament tag returned by search_tournaments(); for global rankings, use the global event identifier.",
    "leaderboard_id": "Leaderboard ID returned by get_leaderboards().",
    "league_id": "League ID advertised by a leaderboard. Available leagues depend on the current event.",
    "location_id": 'Location ID from get_locations(). Ranking routes also accept "global"; clan-search location_id is an integer.',
    "season_id": 'Season identifier such as "2026-10" from get_seasons(). Legacy Trophy Road rankings require a historical season.',
    "name": "Search text of at least three characters. Upstream search ordering is unspecified.",
    "limit": "Requested page size, not a total result cap. Follow a returned cursor for another page.",
    "after": "Cursor for the next page. Cannot be combined with before.",
    "before": "Cursor for the previous page. Cannot be combined with after.",
    "min_members": "Minimum clan member count.",
    "max_members": "Maximum clan member count; must be at least min_members.",
    "min_score": "Minimum clan score.",
}
SAMPLES = {
    "player_tag": '"#J92CYLP28"',
    "clan_tag": '"#88Q2JCVL"',
    "tournament_tag": '"#2GG80C0Q"',
    "leaderboard_id": "170000019",
    "league_id": "1",
    "location_id": '"global"',
    "season_id": '"2026-10"',
}


def escaped(value: Any) -> str:
    return html.escape(str(value), quote=True)


def highlight(source: str, language: str = "python") -> str:
    lexer = {"python": PythonLexer, "bash": BashLexer, "powershell": PowerShellLexer}.get(
        language, TextLexer
    )(stripnl=False, ensurenl=False)
    mapping = [
        (Token.Comment, "comment"),
        (Token.Literal.String, "string"),
        (Token.Literal.Number, "number"),
        (Token.Keyword.Constant, "constant"),
        (Token.Keyword, "keyword"),
        (Token.Name.Function, "function"),
        (Token.Name.Class, "class"),
        (Token.Name.Builtin, "builtin"),
        (Token.Name.Decorator, "decorator"),
        (Token.Operator, "operator"),
    ]
    result = []
    for kind, value in lex(source, lexer):
        color = next((name for token, name in mapping if kind in token), None)
        if color is None and kind in Token.Name and value[:1].isupper():
            color = "class"
        result.append(
            f'<span class="token-{color}">{escaped(value)}</span>' if color else escaped(value)
        )
    return "".join(result)


def code_window(source: str, language: str = "python") -> str:
    return (
        f'<div class="code-window"><div class="code-header"><span>{escaped(language)}</span>'
        '<button type="button" class="code-copy-btn" onclick="copyCode(this)" aria-label="Copy code">Copy</button>'
        f'</div><pre><code class="language-{escaped(language)}">{highlight(source, language)}</code></pre></div>'
    )


def type_name(annotation: Any) -> str:
    if isinstance(annotation, str):
        return annotation.replace("models.", "").replace("clashroyaleapi.models.", "")
    if annotation is type(None):
        return "None"
    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        return " | ".join(type_name(arg) for arg in get_args(annotation))
    if origin:
        return f"{getattr(origin, '__name__', str(origin))}[{', '.join(type_name(arg) for arg in get_args(annotation))}]"
    return getattr(annotation, "__name__", str(annotation).replace("typing.", ""))


def signature(method: Any) -> tuple[str, str]:
    sig = inspect.signature(method)
    args = []
    keyword_only = False
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.kind == inspect.Parameter.KEYWORD_ONLY and not keyword_only:
            args.append("*")
            keyword_only = True
        value = f"{name}: {type_name(param.annotation)}"
        if param.default is not inspect.Parameter.empty:
            value += f" = {param.default!r}"
        args.append(value)
    result = type_name(sig.return_annotation)
    source = f"{method.__name__}({', '.join(args)}) -> {result}"
    if len(source) > 85:
        source = f"{method.__name__}(\n    " + ",\n    ".join(args) + f",\n) -> {result}"
    return source, result


def section(anchor: str, title: str, body: str) -> str:
    return f'<section class="section"><span class="section-anchor" id="{anchor}"></span><h2>{escaped(title)}</h2>{body}</section>'


def render_guide() -> tuple[str, list[tuple[str, str]]]:
    soup = BeautifulSoup(
        markdown.markdown(
            Path("docs/getting-started.md").read_text(encoding="utf-8"),
            extensions=["fenced_code", "tables", "attr_list"],
        ),
        "html.parser",
    )
    for pre in list(soup.select("pre")):
        code = pre.select_one("code")
        classes = code.get("class", [])
        language = next(
            (c.removeprefix("language-") for c in classes if c.startswith("language-")), "text"
        )
        pre.replace_with(BeautifulSoup(code_window(code.get_text(), language), "html.parser"))
    for table in list(soup.select("table")):
        wrapper = soup.new_tag("div", attrs={"class": "table-wrapper"})
        table.wrap(wrapper)
    parts, nav = [], []
    current = None
    for node in list(soup.contents):
        if getattr(node, "name", None) == "h2":
            anchor = node["id"]
            nav.append((anchor, node.get_text()))
            current = soup.new_tag("section", attrs={"class": "section"})
            current.append(soup.new_tag("span", attrs={"class": "section-anchor", "id": anchor}))
            del node["id"]
            current.append(node.extract())
            parts.append(current)
        elif current is not None:
            current.append(node.extract())
    return "\n".join(str(p) for p in parts), nav


def usage(operation: dict[str, Any]) -> str:
    method = operation["python_method"]
    sig = inspect.signature(getattr(Client, method))
    args = [
        SAMPLES[n]
        for n, p in sig.parameters.items()
        if n != "self" and p.default is inspect.Parameter.empty
    ]
    if method.startswith("search_"):
        args.append('name="royale"')
    if "limit" in sig.parameters:
        args.append("limit=10")
    if method == "get_location":
        args = ['"57000094"']
    if method == "get_global_tournament_ranking":
        args[0] = '"#758209"'
    if method == "get_top_player_league_season_rankings":
        args[0] = '"2022-09"'
    return f"result = await client.{method}({', '.join(args)})"


def main():
    reference = json.loads(Path("docs/api-reference.json").read_text(encoding="utf-8"))
    guide, guide_nav = render_guide()
    nav = '<div class="nav-section-title">Getting started</div>'
    nav += "".join(f'<a href="#{a}" class="nav-link">{escaped(t)}</a>' for a, t in guide_nav[:3])
    nav += '<div class="nav-section-title">Using the client</div>'
    nav += "".join(f'<a href="#{a}" class="nav-link">{escaped(t)}</a>' for a, t in guide_nav[3:])
    nav += '<div class="nav-section-title">API reference</div>'
    markdown_reference = [
        "# Endpoint reference",
        "",
        "These signatures describe the API. Usage snippets run inside an async Client context; see [Getting started](getting-started.md).",
        "",
    ]
    groups = []
    for group, (title, description) in GROUPS.items():
        operations = [
            o
            for o in reference["operations"]
            if o["operation_id"]
            and o["path"].split("/")[1] == {"leaderboards": "leaderboard"}.get(group, group)
        ]
        if group == "leaderboards":
            operations = [
                o
                for o in reference["operations"]
                if o["path"].split("/")[1] in ("leaderboard", "leaderboards")
            ]
        nav += f'<div class="nav-collapsible"><a href="#{group}" class="nav-link nav-link-parent" aria-expanded="false">{escaped(title)} <span class="toggle-icon" aria-hidden="true">▼</span></a><div class="nav-sub-links">'
        cards = []
        for op in operations:
            name = op["python_method"]
            nav += f'<a href="#{name}" class="nav-link nav-link-sub">{name}()</a>'
            sig, returns = signature(getattr(Client, name))
            parameters = []
            for pname, param in inspect.signature(getattr(Client, name)).parameters.items():
                if pname == "self":
                    continue
                default = (
                    "Required."
                    if param.default is inspect.Parameter.empty
                    else f"Default: {param.default!r}."
                )
                parameters.append(
                    f'<li class="param-item"><span class="param-name">{pname}</span><span class="param-type">{escaped(type_name(param.annotation))}</span><span class="param-desc">{escaped(PARAMETERS[pname])} {escaped(default)}</span></li>'
                )
            status = ""
            if name in (
                "get_clan_war_log",
                "get_current_war",
                "get_player_ranking",
                "get_global_tournament_ranking",
                "get_leaderboard_league",
            ):
                status = '<p class="info-box note">Check <a href="#availability">upstream availability</a> before using this operation. This example may return an upstream error or an empty result.</p>'
            iterator = ""
            if any(p["name"] == "after" for p in op["parameters"]):
                iterator = f'<p>For automatic paging, use <code>client.iter_{name}(...)</code> with <code>async for</code>. See <a href="#pagination">pages and async iterators</a>.</p>'
            cards.append(
                f'<span class="section-anchor" id="{name}"></span><div class="method-card"><div class="method-header-row"><h3 class="method-title"><code>{name}()</code></h3><div class="method-tags"><span class="tag tag-async">async</span></div></div><p class="method-desc">{escaped(op["summary"])}</p><p><code>GET {escaped(op["path"])}</code></p>{status}<div class="method-signature">{highlight(sig)}</div><h4 class="method-section-title">Parameters</h4><ul class="param-list">{"".join(parameters) or "<li class=param-item>No parameters.</li>"}</ul><h4 class="method-section-title">Returns</h4><span class="returns-tag">{escaped(returns)}</span>{iterator}<h4 class="method-section-title">Usage inside an async Client context</h4>{code_window(usage(op))}</div>'
            )
            markdown_reference += [
                f"## {name}",
                "",
                f"`GET {op['path']}`",
                "",
                "```text",
                sig,
                "```",
                "",
                op["description"],
                "",
                "```python",
                usage(op),
                "```",
                "",
            ]
        nav += "</div></div>"
        groups.append(section(group, title, f"<p>{escaped(description)}</p>" + "".join(cards)))
    Path("docs/endpoints.md").write_text(
        "\n".join(markdown_reference).rstrip() + "\n", encoding="utf-8"
    )
    model_lines = [
        "# Response models",
        "",
        "Fields are optional unless stated otherwise. Unknown fields are retained. See [working with models](getting-started.md#response-models).",
        "",
    ]
    model_cards = []
    for name in models.__all__:
        cls = getattr(models, name)
        rows = []
        model_lines += [f"## {name}", "", "| Attribute | Type | API field |", "| --- | --- | --- |"]
        for field, info in cls.model_fields.items():
            typ = type_name(info.annotation)
            alias = info.alias or field
            rows.append(
                f"<tr><td><code>{escaped(field)}</code></td><td><code>{escaped(typ)}</code></td><td><code>{escaped(alias)}</code></td></tr>"
            )
            model_lines.append(f"| `{field}` | `{typ.replace('|', ' / ')}` | `{alias}` |")
        model_lines.append("")
        table = (
            '<div class="table-wrapper"><table><thead><tr><th>Attribute</th><th>Type</th><th>API field</th></tr></thead><tbody>'
            + "".join(rows)
            + "</tbody></table></div>"
            if rows
            else "<p>Flexible response model. Unknown fields are retained; export them with <code>to_dict()</code>.</p>"
        )
        model_cards.append(
            f'<details class="method-card" id="model-{name}"><summary><code>{name}</code></summary>{table}</details>'
        )
    Path("docs/models.md").write_text("\n".join(model_lines).rstrip() + "\n", encoding="utf-8")
    nav += '<div class="nav-section-title">Data models</div><a href="#response-models" class="nav-link">Working with models</a><a href="#models-reference" class="nav-link">Model field reference</a>'
    model_section = section(
        "models-reference",
        "Model field reference",
        "<p>Expand a model to see its Python attributes, types and original JSON field names. Optional fields may be <code>None</code>. Start with <code>Player</code>, <code>Clan</code>, <code>Item</code> or <code>Page</code>.</p>"
        + "".join(model_cards),
    )
    fragment = "\n".join(
        f"<!-- SLOT:{k} = {v} -->"
        for k, v in {
            "TITLE": "ClashRoyaleAPI",
            "HERO_TITLE": "ClashRoyaleAPI",
            "HERO_SUBTITLE": "Get players, clans, cards and rankings from the official Clash Royale API with a typed, asynchronous Python client.",
            "VERSION": __version__,
            "GITHUB_URL": "https://github.com/EchterAlsFake/ClashRoyaleAPI",
            "PYPI_PACKAGE": "async-royale-client",
            "LICENSE_LABEL": "GPL-3.0-only",
            "ENGINE_URL": "https://github.com/lexiforest/curl_cffi",
            "ENGINE_NAME": "curl_cffi",
            "MCP_BANNER": "",
        }.items()
    )
    fragment += "\n<!-- BEGIN:SIDEBAR_NAV -->\n" + nav + "\n<!-- END:SIDEBAR_NAV -->\n"
    fragment += (
        "<!-- BEGIN:MAIN_CONTENT -->\n"
        + guide
        + "\n"
        + "".join(groups)
        + model_section
        + "\n<!-- END:MAIN_CONTENT -->\n"
    )
    Path("docs/clashroyaleapi.html").write_text(fragment, encoding="utf-8")


if __name__ == "__main__":
    main()
