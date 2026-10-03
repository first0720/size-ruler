#!/usr/bin/env python3
"""사이트 검색 페이지(/search/) 생성기.

사이트맵의 페이지 전체를 정적 목록으로 싣고, 입력한 말로 목록을 거르는 작은 스크립트만 붙인다.
JS가 꺼져도 전체 목록이 보인다. 외부 검색 스크립트는 쓰지 않는다(CLAUDE.md 6번).
build_sitemap.py가 끝에 이 파일을 실행한다.
"""
import html
import json
import os
import re

from build_models import BRAND_HUBS, MODELS, NAV

# 줄임말·영문명. 검색어의 띄어쓰기와 기호는 지우고 비교하므로 붙여 쓴 형태만 적으면 된다.
BRAND_ALIASES = {
    "나이키": "nike", "아디다스": "adidas 아디", "뉴발란스": "newbalance nb 뉴발", "반스": "vans", "컨버스": "converse",
    "아식스": "asics", "푸마": "puma", "살로몬": "salomon", "리복": "reebok", "온러닝": "onrunning 온", "어그": "ugg",
    "버켄스탁": "birkenstock 버켄", "팀버랜드": "timberland 팀버", "크록스": "crocs", "닥터마틴": "drmartens 닥마",
    "오니츠카": "onitsukatiger", "미즈노": "mizuno", "호카": "hoka", "킨": "keen", "캐나다구스": "canadagoose",
    "노스페이스": "northface 노페", "파타고니아": "patagonia", "몽클": "moncler 몽클레어", "아크테릭스": "arcteryx 아크",
    "폴로": "polo ralphlauren 랄프로렌", "톰브라운": "thombrowne",
}
MODEL_ALIASES = {
    "nike-air-force-1": "에포 af1 에어포스", "nike-air-jordan-1": "aj1 조던1", "nike-air-jordan-3": "aj3 조던3",
    "nike-air-jordan-4": "aj4 조던4", "nike-air-jordan-11": "aj11 조던11", "nike-dunk-low": "덩크",
    "converse-chuck-taylor": "척테일러 올스타 allstar", "converse-chuck-70": "척70", "vans-old-skool": "올스쿨",
    "vans-sk8-hi": "스케이트하이", "adidas-samba": "삼바og", "adidas-handball-spezial": "스페지알 spezial",
    "nike-zoom-vomero-5": "보메로", "ugg-classic-mini": "어그부츠", "crocs-classic-clog": "크록스",
}
TOPIC_ALIASES = {
    "ring-size": "반지 호수 ring", "bra-size": "브라 브래지어 bra", "hat-size": "모자 cap", "pants-size-women": "바지 청바지 인치",
    "clothing-size-men": "옷 상의 하의 바지 인치", "clothing-size-women": "옷 상의", "kids-clothing-size": "아이옷 유아복 아기옷",
    "kids-shoe-size": "아이신발 유아신발", "foot-length-chart": "발길이 발사이즈", "half-size-up": "반업 반사이즈",
    "sneaker-heel-height": "굽 굽높이 굽높은 키높이 밑창 무게 heel",
}
CLOTHING = {"clothing-size-men", "clothing-size-women", "kids-clothing-size", "pants-size-women", "bra-size", "hat-size",
            "ring-size", "northface-nuptse", "northface-size-chart", "canada-goose-size-chart", "patagonia-size-chart",
            "moncler-size-chart", "arcteryx-size-chart", "polo-ralph-lauren-size", "thom-browne-size-chart"}
SKIP = {"about", "privacy", "search"}
GROUPS = ["신발 모델", "브랜드 사이즈표", "신발 사이즈 안내", "의류·반지·모자"]


def norm(s):
    return re.sub(r"[\s\-·.,'/()]+", "", s.lower())


def pages():
    """사이트맵 순서대로 (분류, 주소, 이름, 설명, 검색어)."""
    sm = open("sitemap.xml", encoding="utf-8").read()
    models, hubs = {m["slug"] for m in MODELS}, set(BRAND_HUBS.values())
    out = []
    for path in re.findall(r"<loc>https://[^/]+(/[^<]*)</loc>", sm):
        slug = path.strip("/")
        if slug in SKIP:
            continue
        f = "index.html" if not slug else f"{slug}/index.html"
        title = html.unescape(re.search(r"<title>(.*?)</title>", open(f, encoding="utf-8").read(), re.S).group(1))
        name, _, sub = title.partition(" — ")
        group = 0 if slug in models else 1 if slug in hubs else 3 if slug in CLOTHING else 2
        words = [name, sub, slug.replace("-", " "), MODEL_ALIASES.get(slug, ""), TOPIC_ALIASES.get(slug, "")]
        words += [a for b, a in BRAND_ALIASES.items() if b in name]
        out.append((group, path, name, sub, " ".join(norm(w) for w in words if w)))
    return out


SCRIPT = """<script>
(function(){
  var q=document.getElementById("q"), count=document.getElementById("count");
  var cards=[].slice.call(document.querySelectorAll("#results a[data-k]")), groups=document.querySelectorAll("#results section");
  function norm(s){ return s.toLowerCase().replace(/[\\s\\-·.,'\\/()]+/g,""); }
  var names=cards.map(function(a){ return norm(a.firstChild.textContent); });
  function run(){
    var words=q.value.split(/\\s+/).map(norm).filter(Boolean), shown=0;
    cards.forEach(function(a,i){
      var k=a.getAttribute("data-k"), ok=words.every(function(w){ return k.indexOf(w)>=0; });
      a.style.display=ok?"":"none"; if(ok) shown++;
      // 이름에 검색어가 다 들어 있는 페이지를 묶음 맨 앞으로
      a.style.order=ok&&words.length&&words.every(function(w){ return names[i].indexOf(w)>=0; })?"-1":"";
    });
    groups.forEach(function(g){
      g.style.display=g.querySelector('a[data-k]:not([style*="none"])')?"":"none";
    });
    if(!shown&&words.every(function(w){ return /^\\d+$/.test(w); })&&words.length){
      count.innerHTML='사이즈 숫자는 <a href="/">신발 사이즈 환산표</a>나 <a href="/foot-length-chart/">발 길이로 사이즈 찾기</a>에서 찾으세요.';
      return;
    }
    count.textContent=!words.length?"전체 "+cards.length+"개 페이지":shown?shown+"개 페이지":"찾는 페이지가 없습니다. 모델명이나 브랜드로 다시 찾아보세요.";
  }
  var p=new URLSearchParams(location.search).get("q");
  if(p) q.value=p;
  q.addEventListener("input",run);
  run();
})();
</script>"""


def build():
    rows = pages()
    secs = ""
    for i, g in enumerate(GROUPS):
        cards = "".join(f'      <a href="{p}" data-k="{html.escape(k)}">{html.escape(n)}<span>{html.escape(s)}</span></a>\n'
                        for gi, p, n, s, k in rows if gi == i)
        secs += f"""  <section>
    <h2>{g}</h2>
    <div class="related">
{cards}    </div>
  </section>

"""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>사이트 검색 — 사이즈 자</title>
<meta name="description" content="사이즈 자의 신발 모델·브랜드 사이즈표·의류·반지 페이지를 이름으로 찾습니다.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://sizeruler.com/search/">
<meta name="theme-color" content="#FFCE00">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v=5">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8018650083353602" crossorigin="anonymous"></script>
</head>
<body>

<header class="masthead">
  <div class="wrap mark">
    <b><a href="/" style="text-decoration:none;color:inherit">사이즈 자</a></b>
    {NAV}
  </div>
</header>

<main class="wrap">

  <p class="crumb"><a href="/">전체 환산표</a> / 검색</p>

  <div class="hero">
    <p class="eyebrow">페이지 {len(rows)}개</p>
    <h1>찾는 <em>사이즈</em>를 검색하세요</h1>
  </div>

  <form class="entry" role="search" action="/search/" onsubmit="return false">
    <label for="q">검색어</label>
    <input id="q" name="q" type="search" autocomplete="off" placeholder="삼바, 뉴발 993, 반지"
           style="width:min(100%,24rem);font-family:inherit;font-size:18px" aria-describedby="count">
  </form>
  <p id="count" aria-live="polite">전체 {len(rows)}개 페이지</p>

  <div id="results">
{secs}  </div>

</main>

<footer class="wrap">
  <div>사이즈 자 — 검색</div>
  <p class="disclaimer"><a href="/about/">사이트 소개</a> · <a href="/privacy/">개인정보처리방침</a></p>
</footer>

{SCRIPT}

</body>
</html>
"""


def main():
    os.makedirs("search", exist_ok=True)
    with open("search/index.html", "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote search/index.html")


if __name__ == "__main__":
    rows = pages()
    keys = {p: k for _, p, _, _, k in rows}
    # 줄임말·영문·띄어쓰기 없이 찾아도 맞는 페이지가 걸린다
    assert "에포" in keys["/nike-air-force-1/"] and "nike" in keys["/nike-air-force-1/"]
    assert "뉴발" in keys["/newbalance-993/"] and "993" in keys["/newbalance-993/"]
    assert norm("척 70") in keys["/converse-chuck-70/"] and "반지" in keys["/ring-size/"]
    assert all(r[1] not in ("/about/", "/privacy/", "/search/") for r in rows)
    main()
