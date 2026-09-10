"""Quality gates for the static site: accessibility, security, and links."""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.images: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.has_main = False
        self.has_doctype = False

    def handle_decl(self, declaration: str) -> None:
        if declaration.lower() == "doctype html":
            self.has_doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        self.tags.append((tag, attributes))
        if tag == "img":
            self.images.append(attributes)
        if tag == "a":
            self.links.append(attributes)
        if tag == "main":
            self.has_main = True


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def check_site(root: Path) -> list[str]:
    failures: list[str] = []
    index_path = root / "index.html"
    if not index_path.is_file():
        return ["index.html no existe"]

    parser = SiteParser()
    parser.feed(index_path.read_text(encoding="utf-8"))
    tags = parser.tags
    html = next((attrs for tag, attrs in tags if tag == "html"), {})
    title = next((attrs for tag, attrs in tags if tag == "title"), None)
    main = next((attrs for tag, attrs in tags if tag == "main"), {})

    if not parser.has_doctype:
        fail("Falta <!doctype html>", failures)
    if html.get("lang") != "es":
        fail("html debe declarar lang=es", failures)
    if title is None:
        fail("Falta un title", failures)
    if not parser.has_main or not main.get("id"):
        fail("main debe existir y tener id", failures)
    if not any(link.get("href") == f"#{main['id']}" for link in parser.links):
        fail("Falta un skip link hacia main", failures)

    for image in parser.images:
        source = image.get("src", "")
        if not image.get("alt"):
            fail(f"Imagen sin alt: {source}", failures)
        if not image.get("width") or not image.get("height"):
            fail(f"Imagen sin dimensiones explicitas: {source}", failures)

    external_urls: set[str] = set()
    for link in parser.links:
        href = link.get("href", "")
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https"}:
            external_urls.add(href)
            if parsed.scheme != "https":
                fail(f"Enlace externo inseguro (no HTTPS): {href}", failures)
            if link.get("target") == "_blank" and "noopener" not in link.get("rel", ""):
                fail(f"Enlace _blank sin rel=noopener: {href}", failures)
        elif parsed.scheme:
            fail(f"Esquema de enlace no permitido: {href}", failures)
        else:
            local_file = (root / parsed.path.lstrip("/")).resolve()
            if not str(local_file).startswith(str(root.resolve())):
                fail(f"Ruta local fuera del proyecto: {href}", failures)
            elif not local_file.is_file() and parsed.path not in {"", "/"}:
                fail(f"Recurso local inexistente: {href}", failures)

    for tag, attrs in tags:
        source = attrs.get("src") if tag in {"script", "img"} else attrs.get("href") if tag == "link" else None
        if not source or not source.startswith("http"):
            continue
        if not source.startswith("https://"):
            fail(f"Recurso externo inseguro (no HTTPS): {source}", failures)
        external_urls.add(source)

    for url in sorted(external_urls):
        request = Request(url, headers={"User-Agent": "Ejemplo-1-CI-link-check/1.0"})
        try:
            with urlopen(request, timeout=20) as response:
                if response.status >= 400:
                    fail(f"Enlace responde HTTP {response.status}: {url}", failures)
        except (HTTPError, URLError, TimeoutError) as error:
            fail(f"No se pudo verificar {url}: {error}", failures)

    return failures


def main() -> int:
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = arguments.parse_args().root.resolve()
    failures = check_site(root)
    if failures:
        print("CI FAILED")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("CI PASSED: accesibilidad estructural, seguridad de enlaces y recursos verificados")
    return 0


if __name__ == "__main__":
    sys.exit(main())