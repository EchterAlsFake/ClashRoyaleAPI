"""Extract the official rendered Swagger export; never commit browser HTML or credentials."""

import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def snake(value):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def main():
    source = Path(sys.argv[1])
    soup = BeautifulSoup(source.read_text(), "html.parser")
    operations = []
    schemas = {}
    for block in soup.select(".opblock"):
        operation = block["id"].split("-", 2)[2]
        path = block.select_one(".opblock-summary-path")["data-path"]
        params = []
        for row in block.select("tr[data-param-name]"):
            params.append(
                {
                    "name": row["data-param-name"],
                    "in": row["data-param-in"],
                    "type": row.select_one(".parameter__type").get_text(" ", strip=True),
                    "required": bool(row.select_one(".parameter__name.required")),
                }
            )
        response = block.select_one('tr.response[data-code="200"]')
        title = response.select_one(".model-title__text") if response else None
        response_type = title.get_text(strip=True) if title else "APIModel"
        # Some array model titles use a different class.
        if response_type == "APIModel" and response:
            title = response.select_one(".model-title")
            if title:
                response_type = title.get_text(" ", strip=True).split()[-1]
        desc = block.select_one(".opblock-description-wrapper")
        summary = block.select_one(".opblock-summary-description").get_text(" ", strip=True)
        operations.append(
            {
                "operation_id": operation,
                "method": "GET",
                "path": path,
                "python_method": snake(operation),
                "parameters": params,
                "response": response_type,
                "summary": summary,
                "description": desc.get_text(" ", strip=True) if desc else summary,
            }
        )
        if response:
            for model in response.select("span.model"):
                table = model.select_one(":scope > span > span.inner-object > table.model")
                if table is None:
                    continue
                title = model.select_one(".model-title__text")
                if title is None:
                    continue
                fields = {}
                for row in table.select(":scope > tbody > tr.property-row"):
                    cells = row.find_all("td", recursive=False)
                    if len(cells) != 2:
                        continue
                    typ = cells[1].select_one(".prop-type, .model-title__text")
                    fields[cells[0].get_text(strip=True)] = (
                        typ.get_text(strip=True) if typ else "object"
                    )
                if fields:
                    schemas[title.get_text(strip=True)] = fields
    out = {
        "source": "Official developer.clashroyale.com rendered Swagger UI export",
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "limitations": [
            "Collapsed models omit nested field definitions.",
            "Leaderboard leagues references missing definition List.",
        ],
        "operations": operations,
        "schemas": schemas,
    }
    Path("docs/api-reference.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"Imported {len(operations)} operations and {len(schemas)} expanded models")


if __name__ == "__main__":
    main()
