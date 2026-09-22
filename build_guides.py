#!/usr/bin/env python3
"""주제별 가이드 페이지 생성기.

모델 페이지(build_models.py)·의류 페이지(build_clothing.py)와 구조가 달라
별도 생성기로 둔다. 특정 모델이 아니라 '발볼 표기' 같은 개념을 설명하는 페이지.

수치 근거
- 뉴발란스 폭별 발 너비(mm): 뉴발란스 공개 폭 차트 정리본
- JIS(일본 규격) 발 너비: 미즈노 공식 사이즈 안내표
두 규격은 기준이 다르다(미국식=발 너비, JIS=발 둘레). 섞어 쓰지 않는다.
"""
import json
import os

PAGES = [
    {
        "slug": "newbalance-width",
        "name": "뉴발란스 발볼",
        "title": "뉴발란스 발볼 D·2E·4E 뜻 — 내 발볼은 어디에 맞을까",
        "desc": "뉴발란스 남성 D는 표준, 2E는 넓음, 4E는 아주 넓음입니다. "
                "발 너비를 mm로 재서 고르는 법, 한국식 2E 표기와 다른 점, 국내에서 2E·4E 구하는 법을 정리했습니다.",
        "eyebrow": "B · D · 2E · 4E · 6E",
        "h1": "길이가 맞는데 <em>옆이 눌린다면</em>",
        "verdict_top": "핵심",
        "verdict": "남성 D = 표준, 2E = 넓음, 4E = 아주 넓음",
        "verdict_sub": "여성은 B가 표준, D가 넓음, 2E가 아주 넓음입니다. 같은 길이에서 한 단계 올라갈 때 "
                       "발 너비가 3~4mm 넓어집니다. 길이는 그대로입니다.",
        "tables": [
            {
                "h2": "남성 폭별 발 너비",
                "intro": "뉴발란스는 폭마다 들어가는 발 너비를 공개합니다. 발 길이에 맞는 줄에서, "
                         "내 발 너비에 가장 가까운 폭을 고르면 됩니다.",
                "caption": "발 너비는 발볼에서 가장 넓은 부분을 좌우로 잰 직선 길이입니다. 둘레가 아닙니다.",
                "head": ["내 발 길이", "B (좁음)", "D (표준)", "2E (넓음)", "4E (아주 넓음)"],
                "rows": [
                    ["250mm", "96mm", "99mm", "103mm", "106mm"],
                    ["255mm", "97mm", "100mm", "104mm", "107mm"],
                    ["260mm", "98mm", "101mm", "105mm", "108mm"],
                    ["265mm", "99mm", "102mm", "106mm", "109mm"],
                    ["270mm", "100mm", "104mm", "107mm", "110mm"],
                    ["275mm", "101mm", "105mm", "108mm", "111mm"],
                    ["280mm", "102mm", "106mm", "109mm", "113mm"],
                    ["285mm", "103mm", "107mm", "110mm", "114mm"],
                    ["290mm", "104mm", "108mm", "111mm", "115mm"],
                    ["295mm", "105mm", "109mm", "113mm", "116mm"],
                    ["300mm", "106mm", "110mm", "114mm", "117mm"],
                ],
                "highlight": 0,
            },
            {
                "h2": "여성 폭별 발 너비",
                "intro": "여성 라인은 같은 글자라도 뜻이 다릅니다. 여성 D는 넓음이고, 남성 D처럼 표준이 아닙니다.",
                "caption": "우먼스 모델(WR·WL로 시작하는 모델번호)에 해당합니다.",
                "head": ["내 발 길이", "2A (좁음)", "B (표준)", "D (넓음)", "2E (아주 넓음)"],
                "rows": [
                    ["220mm", "78mm", "81mm", "85mm", "88mm"],
                    ["225mm", "79mm", "83mm", "86mm", "89mm"],
                    ["230mm", "80mm", "84mm", "87mm", "90mm"],
                    ["235mm", "81mm", "85mm", "88mm", "92mm"],
                    ["240mm", "82mm", "86mm", "89mm", "93mm"],
                    ["245mm", "83mm", "87mm", "90mm", "94mm"],
                    ["250mm", "84mm", "88mm", "92mm", "95mm"],
                    ["255mm", "85mm", "89mm", "93mm", "96mm"],
                    ["260mm", "86mm", "90mm", "94mm", "97mm"],
                    ["265mm", "87mm", "91mm", "95mm", "98mm"],
                    ["270mm", "88mm", "92mm", "96mm", "99mm"],
                ],
                "highlight": 0,
            },
            {
                "h2": "한국에서 쓰는 EE 표기와 비교",
                "intro": "국내 신발에 붙는 E·EE·EEE는 일본 JIS 규격을 따른 표기로, 거기서는 EE가 '보통'입니다. "
                         "같은 발 길이에서 두 기준의 발 너비를 나란히 놓으면 이렇게 됩니다.",
                "caption": "JIS는 발 둘레, 뉴발란스는 발 너비를 기준으로 삼습니다. 아래는 각 규격이 안내하는 발 너비만 비교한 값입니다.",
                "head": ["내 발 길이", "JIS EE (보통)", "JIS EEE (넓음)", "뉴발란스 D", "뉴발란스 2E"],
                "rows": [
                    ["250mm", "102mm", "104mm", "99mm", "103mm"],
                    ["260mm", "104mm", "106mm", "101mm", "105mm"],
                    ["270mm", "107mm", "109mm", "104mm", "107mm"],
                    ["280mm", "109mm", "111mm", "106mm", "109mm"],
                ],
                "highlight": 0,
            },
        ],
        "body": [
            ("발 너비 재는 법",
             "종이를 바닥에 깔고 그 위에 서서 발을 따라 선을 그립니다. 앉아서 재면 실제보다 좁게 나오니 "
             "반드시 체중을 실은 상태로 재세요. 그린 선에서 좌우로 가장 넓은 두 지점 사이의 직선 거리가 발 너비입니다. "
             "엄지발가락 뿌리와 새끼발가락 뿌리를 잇는 선이라고 보면 됩니다. 양발을 모두 재서 큰 쪽을 기준으로 삼으세요."),
            ("한국식 '보통'과 뉴발란스 D는 같지 않습니다",
             "국내 신발에 EE로 표기된 폭은 일본 JIS 규격을 따른 것이고, 그 규격에서 남성 EE는 '보통'입니다. "
             "그런데 발 길이 250mm 기준으로 JIS EE의 발 너비는 102mm, 뉴발란스 D는 99mm입니다. "
             "평소 '내 발볼은 보통'이라고 생각했던 사람이 뉴발란스 D에서 옆이 눌린다고 느끼는 이유가 여기 있습니다. "
             "표에서 보듯 뉴발란스 2E가 오히려 한국에서 말하는 보통~넓음에 가깝습니다."),
            ("폭이 모자랄 때 길이를 올리는 건 임시방편입니다",
             "발볼이 눌린다고 반 사이즈(5mm) 올리면 폭은 1~2mm 늘어나는 데 그치고 길이만 5mm 남습니다. "
             "그러면 뒤꿈치가 헐렁해지고 걸을 때 발이 앞으로 밀려 오히려 앞볼이 더 눌립니다. "
             "폭이 문제라면 길이가 아니라 폭 표기를 바꾸는 것이 맞습니다. "
             "다만 폭 선택지가 없는 모델이라면, 끈을 조여 발등을 잡아주는 쪽이 사이즈 업보다 낫습니다."),
            ("국내에서 2E·4E 구하기",
             "국내 정식 발매 물량은 대부분 D입니다. 2E·4E는 메이드 인 USA 993처럼 일부 모델에서 별도 상품으로 "
             "유통되며, 같은 색상이라도 상품명에 '2E 와이드'처럼 폭이 따로 적혀 있습니다. "
             "상품 페이지에서 모델번호 뒤에 붙는 폭 표기를 확인하세요. 표기가 없으면 D로 보는 편이 안전합니다. "
             "선택지가 없다면 해외 직구나 구매대행에서 폭을 지정해 살 수 있습니다."),
            ("폭보다 앞코 모양이 문제일 때도 있습니다",
             "같은 D라도 앞코가 둥글게 남는 모델은 발볼이 넓어도 편하고, 앞이 좁게 모이는 모델은 폭이 맞아도 새끼발가락이 눌립니다. "
             "뉴발란스 중에서는 993·990·9060처럼 골이 두꺼운 모델이 여유 있는 편이고, "
             "327은 앞이 좁게 빠져 같은 D라도 답답하게 느껴진다는 의견이 많습니다."),
        ],
        "sources": ["뉴발란스 폭별 발 너비 차트", "JIS 규격 발 치수표(미즈노 공식 안내)", "국내 유통 상품 폭 표기 다수"],
        "faq": [
            ("뉴발란스 D는 발볼이 좁은 건가요?",
             "남성 기준으로 D는 표준입니다. 다만 한국에서 '보통'으로 통하는 JIS EE보다는 2~3mm 좁아서, 발볼이 보통인 사람도 눌린다고 느낄 수 있습니다."),
            ("2E와 4E는 얼마나 차이 나나요?",
             "같은 길이에서 발 너비가 3~4mm 차이 납니다. 270mm 기준 2E는 107mm, 4E는 110mm입니다."),
            ("993 4E는 어떤 사람에게 맞나요?",
             "270mm 기준으로 발 너비가 110mm 안팎인 사람입니다. 2E에서도 새끼발가락이 눌리고 발등이 높은 편이라면 4E를 보세요. 발볼이 보통이면 4E는 안에서 발이 놉니다."),
            ("여자 2E는 남자 2E와 같나요?",
             "다릅니다. 여성 2E는 여성 라인에서 가장 넓은 쪽이고, 남성 2E보다 좁습니다. 여성 표준은 B입니다."),
            ("발볼이 넓으면 반 사이즈 업 하면 되나요?",
             "임시방편입니다. 반 업으로 늘어나는 폭은 1~2mm뿐이고 길이만 5mm 남아 뒤꿈치가 헐렁해집니다. 폭 표기를 바꾸는 쪽이 맞습니다."),
            ("국내에서 파는 뉴발란스는 전부 D인가요?",
             "대부분 D입니다. 993 같은 일부 모델은 2E·4E가 별도 상품으로 들어옵니다. 상품명이나 모델번호 뒤 폭 표기를 확인하세요."),
        ],
        "related": [
            ("/newbalance-993/", "뉴발란스 993 사이즈", "D 기준 정사이즈"),
            ("/newbalance-9060/", "뉴발란스 9060 사이즈", "정사이즈, 골이 넓은 편"),
            ("/newbalance-327/", "뉴발란스 327 사이즈", "반 사이즈 다운"),
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
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8018650083353602" crossorigin="anonymous"></script>

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
  <p class="disclaimer">근거: {srcs}. 폭 표기와 실제 치수는 모델·생산 시기에 따라 달라질 수 있으므로, 구매 전 상품 페이지의 표기를 확인하시기 바랍니다.</p>
  <p class="disclaimer"><a href="/privacy/">개인정보처리방침</a></p>
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
