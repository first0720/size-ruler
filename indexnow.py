#!/usr/bin/env python3
"""IndexNow로 네이버·빙에 사이트맵 URL 전체를 알린다. 배포(git push) 후 1~2분 뒤 실행.

키 파일(루트의 <키>.txt)이 사이트에 올라가 있어야 한다. 네이버는 2023-07부터 IndexNow를 지원한다.
실행: python indexnow.py
"""
import glob
import json
import re
import urllib.request

key = next(f[:-4] for f in glob.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", f))
urls = re.findall(r"<loc>(.*?)</loc>", open("sitemap.xml", encoding="utf-8").read())
body = json.dumps({"host": "sizeruler.com", "key": key,
                   "keyLocation": f"https://sizeruler.com/{key}.txt", "urlList": urls}).encode()
for api in ("https://searchadvisor.naver.com/indexnow", "https://api.indexnow.org/indexnow"):
    req = urllib.request.Request(api, body, {"Content-Type": "application/json; charset=utf-8"})
    try:
        print(api, urllib.request.urlopen(req, timeout=20).status, f"({len(urls)}개 URL)")
    except urllib.error.HTTPError as e:
        print(api, e.code, e.read()[:200])
