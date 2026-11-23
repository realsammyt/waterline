"""Dependency-free checks for stranded links and accidental private content."""
from pathlib import Path
import re
from urllib.parse import unquote

root = Path(__file__).resolve().parent.parent
private = re.compile(
    r"chatgpt\.com/(?:space|library)|library-file|visualize:|sandbox:|"
    r"\.codex/|/workspace/|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    re.I,
)
text_files = (".md", ".html", ".svg")
allowed_host = ("https://www.waterfrontoronto.ca/", "https://www.w3.org/")
for item in root.rglob("*"):
    assert not item.is_symlink(), item
    if not item.is_file() or item.suffix not in text_files:
        continue
    source = item.read_text(encoding="utf-8")
    assert not private.search(source), f"Private content in {item.name}"
    if item.suffix == ".md":
        targets = re.findall(r"\]\(([^ )]+)\)", source)
    else:
        targets = re.findall(r'(?:href|src)="([^"]+)"', source)
    for target in targets:
        if target.startswith(("#", "data:", *allowed_host)):
            continue
        target_path = (item.parent / unquote(target.split("#", 1)[0])).resolve()
        assert target_path.is_relative_to(root) and target_path.is_file(), (item.name, target)
    if item.suffix == ".svg":
        assert "<image " not in source, f"Embedded raster in {item.name}"
        assert item.with_suffix(".png").is_file(), f"Missing diagram export for {item.name}"
    if item.suffix == ".html":
        assert "connect-src 'none'" in source
        assert not re.search(r"\b(?:fetch\(|WebSocket|EventSource|getUserMedia|sendBeacon)", source)
print("Public text, local links, offline HTML and diagram pairing checks passed.")
