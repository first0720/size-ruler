#!/usr/bin/env python3
"""의류 사이즈 페이지 생성기.

신발과 구조가 달라서 별도 생성기로 둔다.
신발은 "발 길이 하나 → 사이즈 하나"지만, 옷은 부위별 치수를 봐야 한다.

핵심 원칙: 남성복 숫자는 실제 신체 치수라 근거가 명확하지만,
여성복 44/55/66은 표준이 없다. 없는 표를 지어내지 않는다.
"""
import json
import os

PAGES = [
    {
        "slug": "clothing-size-men",
        "name": "남성 의류 사이즈",
        "title": "남자 옷 사이즈표 — 95·100·105가 뜻하는 것과 S/M/L 환산",
        "desc": "한국 남성복 사이즈 숫자는 가슴둘레(cm)입니다. 95·100·105를 S/M/L, "
                "US·EU 사이즈로 환산하고 재는 법까지 정리했습니다.",
        "eyebrow": "상의 · 하의 · 실측 기준",
        "h1": "숫자가 <em>곧 내 몸 치수</em>입니다",
        "verdict_top": "핵심",
        "verdict": "상의 숫자 = 가슴둘레 cm",
        "verdict_sub": "95를 입는다면 가슴둘레가 95cm라는 뜻입니다. 하의 인치 숫자는 허리둘레 인치입니다. "
                       "남성복은 이 규칙만 알면 대부분 해결됩니다.",
        "tables": [
            {
                "h2": "상의 사이즈",
                "intro": "숫자는 가슴둘레(cm)를 그대로 쓴 값입니다. 브랜드가 달라도 이 기준은 거의 흔들리지 않습니다.",
                "caption": "오버핏·슬림핏 등 핏에 따라 같은 숫자라도 여유량이 다릅니다.",
                "head": ["한국", "가슴둘레", "알파벳", "US", "EU"],
                "rows": [
                    ["85", "85cm 내외", "XS", "XS", "44"],
                    ["90", "90cm 내외", "S", "S", "46"],
                    ["95", "95cm 내외", "M", "M", "48"],
                    ["100", "100cm 내외", "L", "L", "50"],
                    ["105", "105cm 내외", "XL", "XL", "52"],
                    ["110", "110cm 내외", "XXL", "XXL", "54"],
                    ["115", "115cm 내외", "XXXL", "XXXL", "56"],
                ],
                "highlight": 0,
            },
            {
                "h2": "하의 사이즈",
                "intro": "바지의 인치 숫자는 허리둘레를 인치로 표기한 값입니다. 1인치는 2.54cm입니다.",
                "caption": "청바지는 브랜드별 편차가 커서 실측 허리단면을 보는 편이 정확합니다.",
                "head": ["인치", "허리둘레", "한국", "알파벳", "US"],
                "rows": [
                    ["28", "71cm", "76", "S", "28"],
                    ["30", "76cm", "82", "M", "30"],
                    ["32", "81cm", "87", "L", "32"],
                    ["34", "86cm", "92", "XL", "34"],
                    ["36", "91cm", "97", "XXL", "36"],
                    ["38", "97cm", "102", "XXXL", "38"],
                ],
                "highlight": 0,
            },
        ],
        "body": [
            ("가슴둘레 재는 법",
             "겨드랑이 바로 아래, 가슴에서 가장 두꺼운 부분을 수평으로 한 바퀴 돌려 잽니다. "
             "숨을 크게 들이쉬거나 내쉬지 말고 평상시 호흡 상태에서 재세요. "
             "줄자가 등 쪽에서 처지지 않도록 거울을 보며 확인하는 게 좋습니다."),
            ("표기 사이즈보다 실측이 정확합니다",
             "온라인 상품 페이지에는 대부분 '어깨너비·가슴단면·총장' 같은 실측이 적혀 있습니다. "
             "가슴단면은 옷을 평평하게 놓고 잰 한쪽 폭이라, 가슴둘레와 비교하려면 2를 곱해야 합니다. "
             "표기 사이즈가 애매할 때는 이 실측과 집에 있는 잘 맞는 옷을 비교하는 게 가장 확실합니다."),
            ("해외 직구는 어깨너비를 먼저 보세요",
             "미국·유럽 브랜드는 같은 M이라도 어깨와 소매가 한국 체형보다 길게 나옵니다. "
             "가슴둘레만 맞추면 어깨가 흘러내리는 경우가 생깁니다. "
             "총장과 소매길이도 함께 확인하고, 애매하면 한 사이즈 내리는 쪽이 낫습니다."),
        ],
        "sources": ["한국 성인 남성복 치수 표기 관행(가슴둘레 기준)", "국내 유통 브랜드 사이즈 조견표 다수"],
        "faq": [
            ("남자 100 사이즈는 알파벳으로 뭔가요?",
             "L입니다. 100은 가슴둘레 100cm를 뜻하며, 대체로 US·EU의 L에 해당합니다."),
            ("95와 100 중에 뭘 골라야 하나요?",
             "가슴둘레를 재서 가까운 쪽을 고르세요. 97cm처럼 중간이면 원하는 핏으로 결정합니다. 딱 맞게 입으려면 95, 여유 있게 입으려면 100입니다."),
            ("바지 32인치는 몇 cm인가요?",
             "허리둘레 약 81cm입니다. 인치에 2.54를 곱하면 됩니다."),
            ("오버핏은 사이즈를 올려야 하나요?",
             "오버핏은 이미 여유량을 넣어 설계된 옷이라 정사이즈가 기본입니다. 표기 사이즈를 또 올리면 과하게 커집니다."),
        ],
        "related": [
            ("/clothing-size-women/", "여성 의류 사이즈", "44·55·66이 표준이 아닌 이유"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
    },
    {
        "slug": "clothing-size-women",
        "name": "여성 의류 사이즈",
        "title": "여자 옷 사이즈 44·55·66 — 정확한 환산표가 없는 이유",
        "desc": "여성복 44·55·66·77은 국가 표준이 아니라 브랜드마다 기준이 다릅니다. "
                "통용되는 대응과 함께, 실측으로 고르는 방법을 정리했습니다.",
        "eyebrow": "44 · 55 · 66 · 77",
        "h1": "이 숫자에는 <em>표준이 없습니다</em>",
        "verdict_top": "먼저 알아둘 것",
        "verdict": "44·55·66은 브랜드마다 다릅니다",
        "verdict_sub": "남성복 숫자와 달리 여성복 숫자는 신체 치수를 뜻하지 않습니다. "
                       "아래 표는 통용되는 대응일 뿐이며, 실제 구매는 실측으로 확인해야 합니다.",
        "tables": [
            {
                "h2": "통용되는 대응",
                "intro": "여러 쇼핑몰이 공통적으로 쓰는 대응입니다. 참고용이며, 브랜드에 따라 한 단계씩 어긋납니다.",
                "caption": "이 표만 믿고 주문하지 마세요. 아래 실측 방법을 함께 보시길 권합니다.",
                "head": ["한국", "알파벳", "US", "EU", "가슴둘레 참고"],
                "rows": [
                    ["44", "XS", "0~2", "32~34", "80cm 내외"],
                    ["55", "S", "4", "36", "85cm 내외"],
                    ["66", "M", "6~8", "38", "90cm 내외"],
                    ["77", "L", "10~12", "40", "95cm 내외"],
                    ["88", "XL", "14", "42", "100cm 내외"],
                ],
                "highlight": 0,
            },
        ],
        "body": [
            ("왜 표준이 없을까",
             "남성복 숫자는 가슴둘레를 그대로 쓰지만, 여성복의 44·55·66은 신체 치수와 직접 연결되지 않는 "
                "관습적인 호칭입니다. 국가가 정한 표기 규칙이 아니다 보니 브랜드가 각자 기준을 잡았고, "
                "그 결과 같은 55라도 매장마다 실제 크기가 다릅니다."),
            ("그래서 실측을 봐야 합니다",
             "온라인 상품 페이지의 '가슴단면·어깨너비·총장·소매길이'가 유일하게 신뢰할 수 있는 값입니다. "
                "가슴단면은 옷을 눕혀 놓고 잰 한쪽 폭이므로, 몸의 가슴둘레와 비교하려면 2를 곱하세요. "
                "여기에 여유량 4~6cm를 더한 값이 편하게 맞는 범위입니다."),
            ("가장 확실한 방법은 옷장에 있습니다",
             "지금 가지고 있는 옷 중 가장 잘 맞는 것을 골라 평평하게 펴고 가슴단면·어깨너비·총장을 재세요. "
                "그 숫자를 상품 페이지 실측과 비교하면 표기 사이즈가 무엇이든 실패하지 않습니다. "
                "사이즈 숫자를 맞추는 게 아니라 치수를 맞추는 것이 핵심입니다."),
            ("해외 직구는 체형 차이를 고려하세요",
             "미국·유럽 브랜드는 어깨와 기장이 한국 체형보다 크게 나옵니다. "
                "가슴둘레만 맞으면 어깨가 넘어가거나 소매가 길어질 수 있습니다. "
                "애매하면 한 사이즈 내리되, 어깨너비만은 반드시 확인하세요."),
        ],
        "sources": ["국내 쇼핑몰 사이즈 조견표 다수", "여성복 치수 표기가 표준화되지 않았다는 업계 공통 안내"],
        "faq": [
            ("여자 55는 알파벳으로 뭔가요?",
             "일반적으로 S에 대응합니다. 다만 브랜드마다 기준이 달라서, 같은 55라도 실제 크기는 차이가 납니다."),
            ("44·55·66 사이에 정확한 환산표가 있나요?",
             "없습니다. 국가 표준이 아니라 브랜드별 관습이라 정확한 환산은 불가능합니다. 실측을 확인하는 방법뿐입니다."),
            ("실측에서 가슴단면이 뭔가요?",
             "옷을 평평하게 놓고 겨드랑이 아래를 가로로 잰 한쪽 폭입니다. 몸의 가슴둘레와 비교하려면 2를 곱하세요."),
            ("프리사이즈는 어떤 크기인가요?",
             "대체로 55~66 사이를 겨냥하지만 이것도 브랜드마다 다릅니다. 반드시 실측을 확인하세요."),
        ],
        "related": [
            ("/clothing-size-men/", "남성 의류 사이즈", "숫자가 곧 가슴둘레 cm"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
    },
]


def build(p):
    tables = ""
    for t in p["tables"]:
        head = "".join(f'<th scope="col">{h}</th>' for h in t["head"])
        rows = ""
        for r in t["rows"]:
            cells = ""
            for i, v in enumerate(r):
                if i == t["highlight"]:
                    cells += f'<th scope="row">{v}</th>'
                else:
                    cells += f"<td>{v}</td>"
            rows += f"<tr>{cells}</tr>\n          "
        tables += f"""
  <section>
    <h2>{t['h2']}</h2>
    <p>{t['intro']}</p>
    <div class="scroller">
      <table class="pick-table">
        <caption>{t['caption']}</caption>
        <thead>
          <tr>{head}</tr>
        </thead>
        <tbody>
          {rows.rstrip()}
        </tbody>
      </table>
    </div>
  </section>
"""

    body = "".join(f"<h3>{h}</h3>\n    <p>{x}</p>\n    " for h, x in p["body"])

    faq = "".join(
        f'<details{" open" if i == 0 else ""}>\n      <summary>{q}</summary>\n'
        f"      <p>{a}</p>\n    </details>\n    "
        for i, (q, a) in enumerate(p["faq"]))

    rel = "".join(
        f'<a href="{href}">{name}<span>{sub}</span></a>\n      '
        for href, name, sub in p["related"])

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in p["faq"]]
    }, ensure_ascii=False, indent=2)


    bc = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "사이즈 자",
             "item": "https://sizeruler.com/"},
            {"@type": "ListItem", "position": 2, "name": p['name'],
             "item": f"https://sizeruler.com/{p['slug']}/"},
        ]
    }, ensure_ascii=False, indent=2)

    srcs = " · ".join(p["sources"])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="https://sizeruler.com/{p['slug']}/">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://sizeruler.com/{p['slug']}/">
<meta property="og:image" content="https://sizeruler.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="사이즈 자">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFCE00">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{bc}
</script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

<header class="masthead">
  <div class="wrap mark">
    <b><a href="/" style="text-decoration:none;color:inherit">사이즈 자</a></b>
    <span>{p['name']}</span>
  </div>
</header>

<main class="wrap">

  <p class="crumb"><a href="/">전체 환산표</a> / {p['name']}</p>

  <div class="hero">
    <p class="eyebrow">{p['eyebrow']}</p>
    <h1>{p['h1']}</h1>
  </div>

  <div class="verdict">
    <div class="verdict-top">{p['verdict_top']}</div>
    <div class="verdict-body">
      <strong>{p['verdict']}</strong>
      <p>{p['verdict_sub']}</p>
    </div>
  </div>
{tables}
  <section>
    <h2>알아둘 점</h2>
    {body.rstrip()}
  </section>

  <section>
    <h2>자주 묻는 것</h2>
    {faq.rstrip()}
  </section>

  <section>
    <h2>다른 사이즈 가이드</h2>
    <div class="related">
      {rel.rstrip()}
    </div>
  </section>

</main>

<footer class="wrap">
  <div>사이즈 자 — {p['name']}</div>
  <p class="disclaimer">근거: {srcs}. 의류 치수는 브랜드와 핏에 따라 편차가 크므로, 구매 전 상품 페이지의 실측 정보를 반드시 확인하시기 바랍니다.</p>
</footer>

</body>
</html>
"""


if __name__ == "__main__":
    for p in PAGES:
        os.makedirs(p["slug"], exist_ok=True)
        path = os.path.join(p["slug"], "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(p))
        print("wrote", path)
    print()
    print("사이트맵을 갱신하려면: python3 build_sitemap.py")
