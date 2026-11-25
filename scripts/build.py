#!/usr/bin/env python3
"""Render the landing page from content/site.json. No dependencies."""

from __future__ import annotations

import hashlib
import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "site.json"
TEMPLATE = ROOT / "templates" / "index.html"
REQUIRED_SERVICES = ("supper", "prep", "events", "catering")


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def versioned(rel: str) -> str:
    path = ROOT / rel.split("?", 1)[0]
    if not path.is_file():
        raise SystemExit(f"missing image: {rel}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
    return f"{rel}?v={digest}"


def load() -> dict:
    site = json.loads(CONTENT.read_text())
    ids = [item["id"] for item in site["services"]]
    if ids != list(REQUIRED_SERVICES):
        raise SystemExit(f"services must be {REQUIRED_SERVICES}, got {ids}")
    if site["social"]["instagram"] != "https://www.instagram.com/amycooksit/":
        raise SystemExit("Instagram URL drifted from the published account")
    if not site["phone_e164"].startswith("+"):
        raise SystemExit("phone_e164 must include the country code")
    for event in site["events"]:
        for key in ("date", "title", "blurb", "alt"):
            if not str(event.get(key, "")).strip():
                raise SystemExit(f"event missing {key}: {event!r}")
        image = event.get("image")
        if image and not (ROOT / image).is_file():
            raise SystemExit(f"event image missing: {image}")
    return site


def services(site: dict) -> str:
    blocks = []
    for item in site["services"]:
        blocks.append(
            "<article class=\"service\">"
            f"<span class=\"number\">{esc(item['number'])}</span>"
            f"<h3>{esc(item['name'])}</h3>"
            f"<p>{esc(item['promise'])}</p>"
            f"<p>{esc(item['detail'])}</p>"
            f"<a href=\"#{esc(item['id'])}\">{esc(item['price_label'])}</a>"
            "</article>"
        )
    return "".join(blocks)


def tiers(site: dict) -> str:
    rows = []
    for item in site["tiers"]:
        rows.append(
            "<article class=\"price-row\">"
            f"<h3>{esc(item['name'])}</h3>"
            f"<p class=\"price\">{esc(item['price'])}<small class=\"unit\">{esc(item['unit'])}</small></p>"
            f"<p>{esc(item['detail'])}</p>"
            "</article>"
        )
    return "".join(rows)


def weeks(site: dict) -> str:
    blocks = []
    for index, week in enumerate(site["weeks"]):
        dishes = "".join(
            "<li class=\"dish\">"
            f"<i>{esc(kind)}</i><b>{esc(name)}</b><span>{esc(note)}</span>"
            "</li>"
            for kind, name, note in week["dishes"]
        )
        opened = " open" if index == 0 else ""
        blocks.append(
            f"<details{opened}>"
            f"<summary><span>Week {esc(week['number'])}</span>{esc(week['name'])}</summary>"
            f"<p>{esc(week['note'])}</p><ol>{dishes}</ol></details>"
        )
    return "".join(blocks)


def events(site: dict) -> str:
    if not site["events"]:
        return (
            "<div class=\"book-empty\">"
            "<p class=\"kicker\">The Austin book</p>"
            "<h2>Photographs land after the night.</h2>"
            "<p>A picture and a few lines go here once a table has happened. "
            "The page stays quiet until then, on purpose.</p>"
            "</div>"
        )
    cards = []
    for event in sorted(site["events"], key=lambda item: item["date"], reverse=True):
        image = event.get("image")
        media = (
            f"<img src=\"{esc(versioned(image))}\" alt=\"{esc(event['alt'])}\" loading=\"lazy\">"
            if image
            else ""
        )
        cards.append(
            "<article class=\"event\">"
            f"{media}<div><p class=\"kicker\">{esc(event['date'])}</p>"
            f"<h3>{esc(event['title'])}</h3><p>{esc(event['blurb'])}</p></div></article>"
        )
    return f"<div class=\"events\">{''.join(cards)}</div>"


def offers(site: dict) -> str:
    options = [
        f"{item['name']} — {item['price']}"
        for item in site["tiers"]
    ]
    options.extend(
        f"{item['name']} — quote"
        for item in site["services"]
        if item["id"] != "supper"
    )
    return "".join(f"<option>{esc(option)}</option>" for option in options)


def tiktok(site: dict, footer: bool) -> str:
    url = site["social"].get("tiktok")
    if not url:
        return ""
    label = "TikTok"
    if footer:
        return f" · <a href=\"{esc(url)}\" rel=\"me noopener noreferrer\">{label}</a>"
    return (
        f"<a class=\"button quiet\" href=\"{esc(url)}\" "
        f"rel=\"me noopener noreferrer\">{label}</a>"
    )


def jsonld(site: dict) -> str:
    same_as = [site["social"]["instagram"]]
    if site["social"].get("tiktok"):
        same_as.append(site["social"]["tiktok"])
    payload = {
        "@context": "https://schema.org",
        "@type": "FoodEstablishment",
        "name": site["name"],
        "url": site["url"],
        "telephone": site["phone_e164"],
        "image": site["url"] + versioned(site["hero"]["image"]),
        "servesCuisine": ["Latin American", "Caribbean", "American"],
        "areaServed": {
            "@type": "City",
            "name": site["area"]["city"],
            "address": {
                "@type": "PostalAddress",
                "addressRegion": site["area"]["region"],
                "postalCode": site["area"]["postal"],
                "addressCountry": "US",
            },
        },
        "sameAs": same_as,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def render(site: dict) -> str:
    hero = site["hero"]
    sms = "sms:" + site["phone_e164"]
    page = TEMPLATE.read_text().replace("@@TITLE@@", esc(site["title"]))
    replacements = {
        "@@DESCRIPTION@@": esc(site["description"]),
        "@@OG_IMAGE@@": esc(site["url"] + versioned(hero["image"])),
        "@@JSONLD@@": jsonld(site),
        "@@LOGO@@": esc(versioned("assets/images/logo.jpg")),
        "@@INSTAGRAM@@": esc(site["social"]["instagram"]),
        "@@INSTAGRAM_HANDLE@@": "@amycooksit",
        "@@KICKER@@": esc(hero["kicker"]),
        "@@TITLE_LEAD@@": esc(hero["title_lead"]),
        "@@TITLE_EM@@": esc(hero["title_em"]),
        "@@TITLE_CLOSE@@": esc(hero["title_close"]),
        "@@LEDE@@": esc(hero["lede"]),
        "@@SMS@@": esc(sms),
        "@@HERO@@": esc(versioned(hero["image"])),
        "@@HERO_ALT@@": esc(hero["image_alt"]),
        "@@HERO_CREDIT@@": esc(hero["image_credit"]),
        "@@SERVICES@@": services(site),
        "@@TIERS@@": tiers(site),
        "@@WEEKS@@": weeks(site),
        "@@EVENTS@@": events(site),
        "@@KITCHEN@@": "".join(f"<li>{esc(item)}</li>" for item in site["kitchen"]),
        "@@PHONE@@": esc(site["phone_display"]),
        "@@TIKTOK@@": tiktok(site, footer=False),
        "@@TIKTOK_FOOTER@@": tiktok(site, footer=True),
        "@@OFFERS@@": offers(site),
        "@@ARCHIVE_HREF@@": esc(site["archive"]["href"]),
        "@@ARCHIVE_LABEL@@": esc(site["archive"]["label"]),
    }
    for key, value in replacements.items():
        page = page.replace(key, value)
    leftover = [token for token in page.split("@@") if token.isupper() or token[:1].isupper()]
    if "@@" in page:
        raise SystemExit("unreplaced template token in index.html")
    banned = ("Marcia", "914-471", "lorem", "TODO", "Felicia")
    found = [word for word in banned if word in page]
    if found:
        raise SystemExit(f"public page contains private or placeholder text: {found}")
    return page + ("\n" if not page.endswith("\n") else "")


def write_support(site: dict) -> None:
    (ROOT / ".nojekyll").write_text("")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://amycooksit.com/sitemap.xml\n"
    )
    (ROOT / "sitemap.xml").write_text(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        "  <url><loc>https://amycooksit.com/</loc></url>\n"
        "</urlset>\n"
    )
    (ROOT / "404.html").write_text(
        "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>That page is not on the table · Amy Cooks It</title>"
        "<link rel=\"stylesheet\" href=\"assets/css/site.css\">"
        "<body><main class=\"wrap section\"><p class=\"kicker\">404</p>"
        "<h1>Not on<br><em>the table.</em></h1>"
        "<p class=\"lede\">That page is not plated. The kitchen is still here.</p>"
        "<p><a class=\"button\" href=\"/\">Back to Amy Cooks It</a></p></main></body></html>\n"
    )


def main() -> None:
    site = load()
    page = render(site)
    check = "--check" in sys.argv
    current = (ROOT / "index.html").read_text() if (ROOT / "index.html").exists() else ""
    if check and current != page:
        raise SystemExit("index.html is stale. Run python3 scripts/build.py")
    if not check:
        (ROOT / "index.html").write_text(page)
        write_support(site)
    print("ok" if check else "wrote index.html")


if __name__ == "__main__":
    main()
