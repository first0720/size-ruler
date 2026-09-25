#!/usr/bin/env python3
"""주제별 가이드 페이지 생성기.

모델 페이지(build_models.py)·의류 페이지(build_clothing.py)와 구조가 달라
별도 생성기로 둔다. 특정 모델이 아니라 '발볼 표기' 같은 개념을 설명하는 페이지.

수치 근거
- 뉴발란스 폭별 발 너비(mm): 뉴발란스 공개 폭 차트 정리본
- JIS(일본 규격) 발 너비: 미즈노 공식 사이즈 안내표
두 규격은 기준이 다르다(미국식=발 너비, JIS=발 둘레). 섞어 쓰지 않는다.
- 미국·유럽 사이즈 비교표: build_models.py의 브랜드 공식표(나이키·아디다스·뉴발란스·반스·컨버스)를
  그대로 가져온다. 여기서 숫자를 다시 적지 않는다.
"""
import json
import os

from build_models import (MODELS, NIKE_MAP, ADIDAS_MAP, NB_MAP, VANS_MAP,
                          CONVERSE_MAP, num)

# (브랜드, KR mm -> (US 남성, US 여성, UK, EU)) — 남성·남녀공용 공식표
BRANDS = [("나이키", NIKE_MAP), ("아디다스", ADIDAS_MAP), ("뉴발란스", NB_MAP),
          ("반스", VANS_MAP), ("컨버스", CONVERSE_MAP)]

# 여성 전용 상품 공식표. KR mm -> (US 여성, EU). 같은 mm라도 남녀공용표와 0.5~1 다르다.
NIKE_W = {215: (4.5, 35), 220: (5, 35.5), 225: (5.5, 36), 230: (6, 36.5), 235: (6.5, 37.5),
          240: (7, 38), 245: (7.5, 38.5), 250: (8, 39), 255: (8.5, 40), 260: (9, 40.5),
          265: (9.5, 41), 270: (10, 42)}  # 나이키 코리아 여성 신발 사이즈 차트
NB_W = {220: (5, 35), 225: (5.5, 36), 230: (6, 36.5), 235: (6.5, 37), 240: (7, 37.5),
        245: (7.5, 38), 250: (8, 39), 255: (8.5, 40), 260: (9, 40.5), 265: (9.5, 41),
        270: (10, 41.5)}  # 뉴발란스 공식 사이즈 가이드 여성 표 (Length cm)

CHART_SOURCES = ["나이키 코리아 남성·여성 신발 사이즈 차트", "아디다스 공식 신발 사이즈 차트(adidas.com)",
                 "뉴발란스 공식 사이즈 가이드(newbalance.com)", "반스 공식 사이즈 차트(vans.com)",
                 "컨버스 공식 척테일러 사이즈 차트(converse.com)"]


def by_mm(col, mms):
    """KR mm 줄마다 브랜드별 값(col: 0=US 남성, 1=US 여성, 3=EU)."""
    return [[f"{mm}mm"] + [num(m.get(mm, ("—",) * 4)[col]) for _, m in BRANDS] for mm in mms]


def eu_to_mm(eus, charts):
    """EU 숫자마다 공식표에서 정확히 그 숫자가 붙은 mm. charts: [(표, EU 열 번호)]."""
    rows = []
    for eu in eus:
        row = [f"EU {eu}"]
        for chart, col in charts:
            hits = [mm for mm, v in sorted(chart.items()) if eu in str(v[col]).split("·")]
            row.append(" / ".join(f"{h}mm" for h in hits) or "—")
        rows.append(row)
    return rows


def model_link(slug):
    m = next(x for x in MODELS if x["slug"] == slug)
    return (f"/{slug}/", f"{m['name']} 사이즈", m["verdict"])


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
    {
        "slug": "us-size-chart",
        "name": "미국 신발 사이즈표",
        "title": "미국 신발 사이즈표 — 나이키·아디다스·뉴발란스·컨버스·반스 비교",
        "desc": "같은 270mm라도 나이키·아디다스·뉴발란스·반스는 US 9, 컨버스는 US 8.5입니다. "
                "5개 브랜드 공식 사이즈표로 남성·여성 US 사이즈를 mm별로 비교하고, 240mm 아래에서 나이키만 달라지는 이유를 정리했습니다.",
        "eyebrow": "US · KR 표기 · 5개 브랜드 공식표",
        "h1": "US 9가 <em>모두 270mm는 아닙니다</em>",
        "verdict_top": "핵심",
        "verdict": "270mm = US 9 (나이키·아디다스·뉴발란스·반스), 컨버스만 US 8.5",
        "verdict_sub": "US 사이즈는 국제 표준이 아니라 브랜드가 정합니다. 245mm 이상에서는 컨버스를 뺀 네 브랜드의 숫자가 같고, "
                       "240mm 아래에서는 나이키가 반~한 사이즈 작은 숫자를 씁니다.",
        "tables": [
            {
                "h2": "mm별 US 남성 사이즈",
                "intro": "왼쪽 mm는 상자에 적히는 한국 표기입니다. 같은 줄에서 브랜드마다 US 숫자가 어떻게 달라지는지 보세요.",
                "caption": "각 브랜드 남성·남녀공용 공식 사이즈표의 값입니다. 반스는 US 남성을 6.5(245mm)부터 표기합니다. "
                           "한 칸에 두 값이 있으면 공식표에 두 줄로 나오는 사이즈입니다.",
                "head": ["KR 표기", "나이키", "아디다스", "뉴발란스", "반스", "컨버스"],
                "rows": by_mm(0, range(225, 305, 5)),
                "highlight": 0,
            },
            {
                "h2": "mm별 US 여성 사이즈 — 남녀공용 상품",
                "intro": "에어포스 1·삼바·530처럼 남녀가 같이 신는 상품을 여성 사이즈로 고를 때의 값입니다.",
                "caption": "남녀공용 상품 기준입니다. 반스는 US 여성을 11.5(280mm)까지 표기합니다.",
                "head": ["KR 표기", "나이키", "아디다스", "뉴발란스", "반스", "컨버스"],
                "rows": by_mm(1, range(225, 285, 5)),
                "highlight": 0,
            },
            {
                "h2": "여성 전용 상품은 여성 사이즈표를 씁니다",
                "intro": "여성 전용으로 나온 상품은 브랜드가 여성 사이즈표를 따로 씁니다. 나이키와 뉴발란스 여성표는 같은 mm에 같은 US 여성 숫자를 붙이고, "
                         "245mm 이상에서는 남녀공용표보다 0.5 작습니다.",
                "caption": "나이키 코리아 여성 신발 사이즈 차트, 뉴발란스 공식 사이즈 가이드 여성 표의 값입니다.",
                "head": ["KR 표기", "나이키 여성 전용", "뉴발란스 여성 전용", "나이키 남녀공용", "뉴발란스 남녀공용"],
                "rows": [[f"{mm}mm", num(NIKE_W[mm][0]), num(NB_W[mm][0]),
                          num(NIKE_MAP.get(mm, ("—",) * 4)[1]), num(NB_MAP[mm][1])]
                         for mm in range(220, 275, 5)],
                "highlight": 0,
            },
        ],
        "body": [
            ("US 사이즈는 브랜드가 정하는 숫자입니다",
             "US 9라는 숫자가 모든 브랜드에서 같은 길이를 뜻하지는 않습니다. 나이키·아디다스·뉴발란스·반스는 US 남성 9를 270mm로 표기하지만, "
             "컨버스 공식 차트는 US 남성 9를 27.5cm로 잡습니다. 그래서 컨버스는 같은 mm에서 US 숫자가 반 칸 작습니다. "
             "컨버스가 '크게 나오니 반 사이즈 작게 주문하라'고 안내하는 것도 US로 고를 때의 이야기입니다. "
             "자세한 내용은 <a href=\"/converse-chuck-taylor/\">척테일러 사이즈</a>에 정리했습니다."),
            ("240mm 아래에서는 나이키 숫자가 작아집니다",
             "245mm 이상에서는 컨버스를 뺀 네 브랜드의 US 남성 숫자가 같습니다. 240mm 아래로 내려가면 나이키만 반~한 사이즈 작은 숫자를 씁니다. "
             "230mm가 아디다스·뉴발란스에서는 US 남성 5인데 나이키에서는 4입니다. "
             "나이키 공식표는 235mm와 240mm에 US 사이즈를 두 개씩 붙여 두었으니, 이 구간에서 나이키를 US로 살 때는 상품의 cm 표기를 함께 확인하세요."),
            ("여성 US는 남성보다 1~2 큽니다",
             "남녀공용 상품에서 US 여성은 나이키·뉴발란스·반스가 남성보다 1.5, 아디다스가 1, 컨버스가 2 큽니다. "
             "그래서 230mm 여성은 브랜드에 따라 US 5.5(나이키)부터 6.5(뉴발란스·반스)까지 갈립니다. "
             "여성 전용 상품은 여성 사이즈표를 따로 쓰기 때문에, 나이키 250mm가 남녀공용이면 W8.5, 여성 전용이면 W8입니다."),
            ("해외 직구는 US 숫자보다 cm 표기를 맞추세요",
             "US 숫자는 브랜드마다 뜻이 달라서, 평소 mm를 US로 바꿔 주문하면 반 사이즈씩 어긋나기 쉽습니다. "
             "사이즈 선택지나 상품 태그에 cm(JP) 값이 함께 있으면 그 값을 평소 mm와 맞추세요. "
             "컨버스 태그에는 'US M 8.5 / CM 27'처럼 둘이 같이 적혀 있습니다. "
             "UK·EU도 브랜드마다 다르니 <a href=\"/eu-size-chart/\">유럽 신발 사이즈표</a>를 함께 보세요."),
            ("사이즈 숫자와 핏은 별개입니다",
             "이 표는 같은 길이에 어떤 숫자가 붙는지를 보여줄 뿐, 신었을 때의 핏은 모델마다 다릅니다. 같은 아디다스 안에서도 "
             "<a href=\"/adidas-samba/\">삼바</a>는 보통 발볼이면 정사이즈, <a href=\"/adidas-gazelle/\">가젤</a>은 대부분 반 사이즈 업, "
             "<a href=\"/adidas-campus-00s/\">캠퍼스 00s</a>는 반 사이즈 다운입니다. 모델별 결론은 각 모델 페이지에서 확인하세요."),
        ],
        "sources": CHART_SOURCES,
        "faq": [
            ("270mm는 US 사이즈로 몇인가요?",
             "나이키·아디다스·뉴발란스·반스는 US 남성 9, 컨버스는 US 남성 8.5입니다. 남녀공용 상품의 US 여성으로는 아디다스가 10, 나머지 네 브랜드가 10.5입니다."),
            ("US 9는 몇 mm인가요?",
             "나이키·아디다스·뉴발란스·반스는 270mm, 컨버스는 275mm입니다."),
            ("230mm는 US 여성으로 몇인가요?",
             "남녀공용 상품 기준으로 나이키 5.5, 아디다스·컨버스 6, 뉴발란스·반스 6.5입니다. 여성 전용 상품은 나이키·뉴발란스 모두 6입니다."),
            ("250mm는 US 여성으로 몇인가요?",
             "남녀공용 상품이면 나이키·뉴발란스·반스·컨버스 8.5, 아디다스 8입니다. 여성 전용 상품은 나이키·뉴발란스 모두 8입니다."),
            ("컨버스는 왜 반 사이즈 작게 사라고 하나요?",
             "컨버스는 같은 US 숫자를 다른 브랜드보다 5mm 긴 신발에 붙입니다(US 남성 9 = 27.5cm). 그래서 평소 US 숫자로 고르면 반 사이즈 크게 받게 되니 "
             "반 사이즈 내리라고 안내합니다. mm로 고르면 평소 mm 그대로입니다."),
            ("나이키 235·240mm는 왜 US 사이즈가 두 개인가요?",
             "나이키 공식 사이즈표가 235mm에 US 남성 4.5와 5, 240mm에 5.5와 6을 함께 붙여 두었기 때문입니다. 이 구간은 상품의 cm 표기를 함께 확인하세요."),
        ],
        "related_h2": "함께 보면 좋은 페이지",
        "related": [
            ("/eu-size-chart/", "유럽 신발 사이즈표", "EU 38·42는 몇 mm?"),
            model_link("converse-chuck-taylor"),
            model_link("nike-air-force-1"),
            model_link("adidas-samba"),
            ("/newbalance-width/", "뉴발란스 발볼", "D·2E·4E 발 너비"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
        "note": "브랜드 공식표는 바뀔 수 있으니, 구매 전 상품 페이지의 사이즈 표기를 한 번 더 확인하시기 바랍니다.",
    },
    {
        "slug": "eu-size-chart",
        "name": "유럽 신발 사이즈표",
        "title": "유럽 신발 사이즈표 — EU 38·42는 몇 mm? 브랜드별 공식표 비교",
        "desc": "EU 38은 나이키·반스 240mm, 아디다스·뉴발란스 235mm, 컨버스 245mm입니다. 같은 EU 숫자도 브랜드마다 5~10mm 다릅니다. "
                "5개 브랜드 공식 사이즈표로 EU와 mm를 양쪽으로 찾고, 여성 전용 상품이 다른 점도 정리했습니다.",
        "eyebrow": "EU · KR 표기 · 5개 브랜드 공식표",
        "h1": "EU 38이 몇 mm인지는 <em>브랜드가 정합니다</em>",
        "verdict_top": "핵심",
        "verdict": "EU 38 = 235mm(아디다스·뉴발란스) ~ 245mm(컨버스)",
        "verdict_sub": "EU 사이즈에는 국제 표준이 없습니다. EU 42도 나이키·아디다스·뉴발란스는 265mm, 반스·컨버스는 270mm입니다. "
                       "여성 전용 상품은 또 다른 표를 써서, 뉴발란스 여성용 EU 38은 245mm입니다.",
        "tables": [
            {
                "h2": "EU 숫자로 mm 찾기",
                "intro": "해외 사이트에서 EU 사이즈만 보일 때, 브랜드 칸에서 mm를 확인하세요.",
                "caption": "남성·남녀공용 공식표에 정확히 그 EU 숫자가 있는 경우만 적었습니다. "
                           "아디다스는 EU를 ⅓ 단위로 매겨 37·39·41 같은 숫자가 없습니다.",
                "head": ["EU", "나이키", "아디다스", "뉴발란스", "반스", "컨버스"],
                "rows": eu_to_mm(["36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46"],
                                 [(m, 3) for _, m in BRANDS]),
                "highlight": 0,
            },
            {
                "h2": "mm로 EU 찾기",
                "intro": "평소 mm를 알고 있을 때, 브랜드마다 어떤 EU 숫자를 골라야 하는지입니다.",
                "caption": "남성·남녀공용 공식표 기준입니다. 한 칸에 두 값이 있으면 공식표에 두 줄로 나오는 사이즈입니다.",
                "head": ["KR 표기", "나이키", "아디다스", "뉴발란스", "반스", "컨버스"],
                "rows": by_mm(3, range(225, 305, 5)),
                "highlight": 0,
            },
            {
                "h2": "여성 전용 상품은 EU가 다르게 붙습니다",
                "intro": "여성 전용으로 나온 상품은 여성 사이즈표를 씁니다. 같은 EU 숫자라도 남녀공용 상품보다 긴 신발일 수 있습니다.",
                "caption": "나이키 코리아 여성 신발 사이즈 차트, 뉴발란스 공식 사이즈 가이드 여성 표, 두 브랜드 남성표의 값입니다.",
                "head": ["EU", "나이키 여성 전용", "뉴발란스 여성 전용", "나이키 남녀공용", "뉴발란스 남녀공용"],
                "rows": eu_to_mm(["35", "36", "36.5", "37", "37.5", "38", "38.5", "39", "40", "40.5", "41"],
                                 [(NIKE_W, 1), (NB_W, 1), (NIKE_MAP, 3), (NB_MAP, 3)]),
                "highlight": 0,
            },
        ],
        "body": [
            ("EU 사이즈는 국제 표준이 아닙니다",
             "EU 사이즈는 프랑스식 파리 포인트(1포인트 = 6.67mm)에서 온 관습이라 브랜드마다 반올림하는 방식이 다릅니다. "
             "그래서 같은 EU 숫자가 브랜드에 따라 5~10mm 다른 길이에 붙습니다. "
             "EU 38이 아디다스·뉴발란스에서는 235mm, 나이키·반스에서는 240mm, 컨버스에서는 245mm입니다."),
            ("반스·컨버스는 같은 mm에서 EU가 작습니다",
             "270mm에 붙는 EU는 나이키·뉴발란스 42.5, 아디다스 42⅔인데 반스·컨버스는 42입니다. "
             "거꾸로 보면 같은 EU 42가 반스·컨버스에서는 5mm 더 긴 신발입니다. "
             "다른 브랜드에서 쓰던 EU 숫자로 반스·컨버스를 사면 반 사이즈 크게 받게 됩니다."),
            ("아디다스는 ⅓ 단위를 씁니다",
             "아디다스 공식표의 EU는 40, 40⅔, 41⅓, 42처럼 ⅓씩 올라갑니다. 해외 사이트에서 '42 2/3'으로 보이는 사이즈가 270mm로, "
             "다른 브랜드의 EU 42.5와 같은 길이입니다. 그래서 아디다스에는 EU 37·39·41·43·45가 없습니다."),
            ("여성 전용 상품은 여성 사이즈표를 봐야 합니다",
             "같은 브랜드라도 여성 전용 상품은 여성 사이즈표를 따로 씁니다. 270mm가 나이키 남성표에서는 EU 42.5, 여성표에서는 42이고, "
             "뉴발란스는 남성 42.5, 여성 41.5입니다. 반대로 EU 38을 고르면 뉴발란스 남녀공용은 235mm, 여성 전용은 245mm로 10mm 차이가 납니다. "
             "여성용을 EU로 고를 때는 그 상품이 여성 전용인지 먼저 확인하세요."),
            ("EU로만 파는 브랜드는 따로 확인하세요",
             "버켄스탁처럼 EU 숫자로만 파는 브랜드는 위 다섯 브랜드와 기준이 또 다를 수 있습니다. "
             "<a href=\"/birkenstock-boston/\">버켄스탁 보스턴 사이즈</a>처럼 모델 페이지가 있으면 그쪽을 참고하세요. "
             "US 기준 비교는 <a href=\"/us-size-chart/\">미국 신발 사이즈표</a>에 있습니다."),
        ],
        "sources": CHART_SOURCES,
        "faq": [
            ("EU 38은 몇 mm인가요?",
             "남성·남녀공용 공식표 기준으로 아디다스·뉴발란스 235mm, 나이키·반스 240mm, 컨버스 245mm입니다. "
             "여성 전용 상품은 나이키 240mm, 뉴발란스 245mm입니다."),
            ("EU 37은 몇 mm인가요?",
             "뉴발란스 225mm, 반스·컨버스 235mm입니다. 나이키·아디다스 남성표에는 EU 37이 없고, 가장 가까운 값은 "
             "나이키 235mm(EU 36.5·37.5), 아디다스 230mm(37⅓)입니다. 여성 전용 상품은 뉴발란스 235mm입니다."),
            ("EU 42는 몇 mm인가요?",
             "나이키·아디다스·뉴발란스는 265mm, 반스·컨버스는 270mm입니다."),
            ("EU 44는 몇 mm인가요?",
             "나이키·아디다스·뉴발란스는 280mm, 반스·컨버스는 285mm입니다."),
            ("270mm는 EU로 몇인가요?",
             "나이키·뉴발란스 42.5, 아디다스 42⅔, 반스·컨버스 42입니다. 여성 전용 상품이면 나이키 42, 뉴발란스 41.5입니다."),
            ("아디다스 42 2/3는 몇 mm인가요?",
             "270mm입니다. 아디다스 공식표에서 US 남성 9, UK 8.5와 같은 사이즈입니다."),
        ],
        "related_h2": "함께 보면 좋은 페이지",
        "related": [
            ("/us-size-chart/", "미국 신발 사이즈표", "US 9가 모두 270mm는 아닙니다"),
            model_link("vans-old-skool"),
            model_link("converse-chuck-70"),
            model_link("birkenstock-boston"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
        "note": "브랜드 공식표는 바뀔 수 있으니, 구매 전 상품 페이지의 사이즈 표기를 한 번 더 확인하시기 바랍니다.",
    },
    {
        "slug": "about",
        "name": "사이트 소개",
        "title": "사이즈 자 소개 — 사이즈 정보를 모으고 검증하는 방법",
        "desc": "사이즈 자는 신발·의류 사이즈를 모델 단위로 정리하는 사이트입니다. 어떤 출처를 얼마나 믿는지, "
                "공식표와 착용 후기가 다를 때 어떻게 정하는지, 정보를 어떻게 고치는지 정리했습니다.",
        "eyebrow": "ABOUT · 검증 원칙",
        "h1": "모든 숫자에 <em>출처를 붙입니다</em>",
        "verdict_top": "원칙",
        "verdict": "브랜드가 아니라 모델 단위로, 출처가 있는 정보만",
        "verdict_sub": "'나이키는 크게 나온다' 같은 브랜드 단위 결론은 쓰지 않습니다. "
                       "같은 브랜드 안에서도 모델마다 정사이즈와 반업이 갈리기 때문입니다.",
        "tables": [
            {
                "h2": "출처를 믿는 순서",
                "intro": "같은 모델을 두고 출처끼리 말이 다르면 위쪽을 따릅니다. 아래쪽 출처의 의견은 발볼이나 착용법 같은 조건으로 남깁니다.",
                "caption": "각 페이지 아래의 '근거'에 실제로 참고한 출처를 적어 둡니다.",
                "head": ["순서", "출처", "예"],
                "rows": [["1", "브랜드 공식 안내", "공식 사이즈표, 상품 페이지의 사이즈 안내"],
                         ["2", "리셀 플랫폼 사이즈 팁", "KREAM 사이즈 팁"],
                         ["3", "실측 리뷰·착용자 투표", "RunRepeat 실측과 착용자 투표"],
                         ["4", "커뮤니티 다수 의견", "여러 곳에서 반복되는 착용 후기"]],
                "highlight": 0,
            },
        ],
        "body": [
            ("공식 안내와 후기가 다르면 공식을 따릅니다",
             "컨버스 척 70은 국내 후기에서 반업 의견이 많았지만, 컨버스 공식 차트는 척 70을 크게 나오는 모델로 분류합니다. "
             "이럴 때 결론은 공식 안내를 따르고, 후기는 '발볼이 넓으면 반업'처럼 조건으로 남깁니다."),
            ("근거를 못 찾으면 싣지 않습니다",
             "사이즈 정보를 추측으로 채우지 않습니다. 근거가 약한 항목은 출처에 '커뮤니티 의견'이라고 밝히고, "
             "근거를 찾지 못한 모델은 페이지를 만들지 않습니다."),
            ("환산표도 브랜드 공식표를 씁니다",
             "US·UK·EU 숫자는 브랜드마다 다릅니다. 나이키·아디다스·뉴발란스·반스·컨버스 모델은 각 브랜드 공식 사이즈표의 값을 쓰고, "
             "공식표를 아직 대조하지 못한 브랜드는 표 아래에 일반 환산표라고 적습니다. 브랜드끼리의 차이는 "
             "<a href=\"/us-size-chart/\">미국 신발 사이즈표</a>와 <a href=\"/eu-size-chart/\">유럽 신발 사이즈표</a>에 모았습니다."),
            ("정보는 계속 고칩니다",
             "브랜드가 사이즈표를 바꾸거나 새 근거가 나오면 수정합니다. 2026년 9월에는 컨버스 척 70의 결론을 공식 차트 기준으로 바꾸고, "
             "모델 페이지의 US·UK·EU 환산을 브랜드 공식표로 교체했습니다."),
            ("광고와 개인정보",
             "사이즈 자는 구글 애드센스 광고로 운영합니다. 방문 기록과 쿠키를 어떻게 다루는지는 "
             "<a href=\"/privacy/\">개인정보처리방침</a>에 적어 두었습니다."),
        ],
        "sources": ["브랜드 공식 사이즈표", "리셀 플랫폼 사이즈 팁", "실측 리뷰", "착용 후기"],
        "faq": [
            ("사이즈 정보는 어디서 가져오나요?",
             "브랜드 공식 사이즈표와 상품 페이지 안내를 먼저 보고, 없으면 KREAM 사이즈 팁, 실측 리뷰와 착용자 투표, "
             "여러 곳에서 반복되는 착용 후기 순으로 찾습니다. 각 페이지 아래에 실제로 참고한 근거를 적습니다."),
            ("브랜드 전체가 크게 나온다는 말은 왜 없나요?",
             "같은 브랜드 안에서도 모델마다 결과가 다르기 때문입니다. 아디다스만 해도 삼바는 보통 발볼이면 정사이즈, "
             "가젤은 대부분 반 사이즈 업, 캠퍼스 00s는 반 사이즈 다운입니다."),
            ("여기 나온 사이즈가 나에게 꼭 맞나요?",
             "권장 사이즈는 많은 사람에게 통하는 경향이지 모든 발에 맞는 답은 아닙니다. 발볼·발등 높이·양말 두께에 따라 달라질 수 있으니, "
             "비싼 신발은 매장에서 신어 보고 사는 것을 권합니다."),
        ],
        "related_h2": "둘러보기",
        "related": [
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
            ("/us-size-chart/", "미국 신발 사이즈표", "브랜드별 US 비교"),
            ("/eu-size-chart/", "유럽 신발 사이즈표", "브랜드별 EU 비교"),
            ("/privacy/", "개인정보처리방침", "쿠키와 광고"),
        ],
        "note": "사이즈 정보는 일반적인 착용 경향이며, 개인의 발 모양에 따라 결과가 다를 수 있습니다.",
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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
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
    <h2>{p.get('related_h2', '다른 사이즈 가이드')}</h2>
    <div class="related">
      {rel.rstrip()}
    </div>
  </section>

</main>

<footer class="wrap">
  <div>사이즈 자 — {p['name']}</div>
  <p class="disclaimer">근거: {srcs}. {p.get('note', '폭 표기와 실제 치수는 모델·생산 시기에 따라 달라질 수 있으므로, 구매 전 상품 페이지의 표기를 확인하시기 바랍니다.')}</p>
  <p class="disclaimer"><a href="/about/">사이트 소개</a> · <a href="/privacy/">개인정보처리방침</a></p>
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
