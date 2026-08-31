#!/usr/bin/env python3
"""sitemap.xml 생성기.

폴더를 스캔해서 index.html이 있는 경로를 전부 사이트맵에 넣는다.
카테고리가 늘어나도 이 파일을 고칠 필요가 없다.

실행: python3 build_sitemap.py
"""
import os
import re

DOMAIN_FILE = "index.html"  # 현재 도메인을 여기서 읽는다
EXCLUDE = {"404.html"}


def current_domain():
    """index.html의 canonical에서 도메인을 읽는다."""
    src = open(DOMAIN_FILE, encoding="utf-8").read()
    m = re.search(r'rel="canonical" href="https://([^/"]+)', src)
    if not m:
        raise SystemExit("index.html에서 canonical을 찾지 못했습니다.")
    return m.group(1)


def collect_paths():
    """루트 + index.html을 가진 하위 폴더를 URL 경로로 반환."""
    paths = ["/"]
    for entry in sorted(os.listdir(".")):
        if not os.path.isdir(entry) or entry.startswith("."):
            continue
        if entry in {"__pycache__", "node_modules"}:
            continue
        if os.path.exists(os.path.join(entry, "index.html")):
            paths.append(f"/{entry}/")
    return paths


def main():
    domain = current_domain()
    paths = collect_paths()

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        lines += ["  <url>",
                  f"    <loc>https://{domain}{p}</loc>",
                  "    <changefreq>monthly</changefreq>",
                  f"    <priority>{'1.0' if p == '/' else '0.8'}</priority>",
                  "  </url>"]
    lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: https://{domain}/sitemap.xml\n")

    print(f"sitemap.xml: {len(paths)}개 URL ({domain})")
    for p in paths:
        print("  ", p)


if __name__ == "__main__":
    main()
