#!/usr/bin/env python3
"""의류 사이즈 페이지 생성기.

신발과 구조가 달라서 별도 생성기로 둔다.
신발은 "발 길이 하나 → 사이즈 하나"지만, 옷은 부위별 치수를 봐야 한다.

핵심 원칙: 남성복 숫자는 실제 신체 치수라 근거가 명확하지만,
여성복 44/55/66은 1981년 표기법(55 = 키 155cm·가슴둘레 85cm)에서 나왔고 지금은 공식 기준이 아니다.
없는 표를 지어내지 않는다.
"""
import json
import os

from build_guides import MONCLER_M, RL_MEN, TB_MEN, TB_WOMEN, TNF_M
from build_models import NAV, keep_phrases, stamp

# 1981년 여성복 표기법: 55(키 155cm·가슴둘레 85cm)를 기준으로 키 5cm, 가슴둘레 3cm씩 더하고 뺐다.
# 국가기술표준원 설명(중앙일보 2017-07-26 '44·55 사이즈, 대체 무슨 뜻?'). (사이즈, 키, 가슴둘레)
KS1981_W = [(44 + 11 * i, 150 + 5 * i, 82 + 3 * i) for i in range(5)]

# 남성 상의의 미국 브랜드 알파벳: 톰 브라운 공식표의 한국 표기(XXS 85 ~ XXL 115). 랄프 로렌 코리아(XS 90~)와 같다.
US_M = {k: s for _, s, k, _ in TB_MEN}


def it_size(chest):
    """몽클레어 한국 공식 가이드(남성)에서 몸 가슴둘레가 가장 가까운 이탈리아 사이즈. 같은 거리면 두 숫자."""
    (d1, a), (d2, b) = sorted((abs(c - chest), i) for _, _, c, _, i in MONCLER_M)[:2]
    return str(a) if d1 < d2 else f"{min(a, b)}·{max(a, b)}"

PAGES = [
    {
        "slug": "clothing-size-men",
        "name": "남성 의류 사이즈",
        "title": "남자 옷 사이즈 95·100·105 — M·L·XL, 키·가슴둘레 기준표",
        "desc": "남자 95는 M, 100은 L, 105는 XL입니다. 숫자는 가슴둘레 cm이고, 노스페이스 코리아 공식표로 95는 키 165~175cm입니다. "
                "키로 보는 표와 허리 cm↔인치 환산까지 정리했습니다.",
        "eyebrow": "상의 · 하의 · 실측 기준",
        "h1": "숫자가 <em>곧 내 몸 치수</em>입니다",
        "verdict_top": "핵심",
        "verdict": "상의 숫자 = 가슴둘레 cm",
        "verdict_sub": "국내 브랜드는 90 = S, 95 = M, 100 = L, 105 = XL, 110 = XXL입니다. "
                       "95를 입는다면 가슴둘레가 95cm라는 뜻입니다. 미국 브랜드는 알파벳이 한 칸 작아 100이 M입니다. "
                       "키로는 노스페이스 코리아 공식표에서 95가 165~175cm입니다.",
        "tables": [
            {
                "h2": "상의 사이즈",
                "intro": "숫자는 가슴둘레(cm)를 그대로 쓴 값입니다. 알파벳은 국내 브랜드와 미국 브랜드가 한 칸 다릅니다.",
                "caption": "국내 알파벳은 노스페이스 코리아 공식표, 미국 브랜드는 톰 브라운·랄프 로렌 코리아 공식표의 한국 표기, "
                           "이탈리아는 몽클레어 한국 공식 가이드에서 몸 가슴둘레가 가장 가까운 숫자(두 숫자는 그 사이)입니다. "
                           "핏에 따라 같은 숫자라도 여유량이 다릅니다.",
                "head": ["한국", "가슴둘레", "국내 알파벳", "미국 브랜드", "이탈리아"],
                "rows": [[str(k), f"{k}cm 내외", a, US_M[k], it_size(k)] for a, k, _, _ in TNF_M],
                "highlight": 0,
            },
            {
                "h2": "키로 보는 사이즈",
                "intro": "노스페이스 코리아 공식몰 재킷 사이즈 안내의 신장입니다. 키는 참고이고, 고를 때는 가슴둘레가 먼저입니다.",
                "caption": "노스페이스 코리아 공식몰 상품 사이즈 안내(재킷, 2026-09, 화이트라벨 표). "
                           "본 라인 표는 S~XXL만 있고 XXL이 180~185cm입니다.",
                "head": ["한국", "알파벳", "키"],
                "rows": [[str(k), s, f"{b}cm"] for s, k, _, b in TNF_M],
                "highlight": 0,
            },
            {
                "h2": "하의 사이즈",
                "intro": "바지의 인치 숫자는 허리둘레를 인치로 표기한 값입니다. 1인치는 2.54cm이고, "
                         "상품 실측의 허리단면은 둘레의 절반입니다.",
                "caption": "청바지는 브랜드별 편차가 커서 실측 허리단면을 보는 편이 정확합니다.",
                "head": ["인치", "허리둘레", "허리단면"],
                "rows": [[str(i), f"{i * 2.54:.0f}cm", f"{i * 2.54 / 2:.1f}cm"] for i in range(28, 40, 2)],
                "highlight": 0,
            },
            {
                "h2": "cm ↔ 인치 환산",
                "intro": "허리둘레·가슴둘레를 인치로 바꾼 값입니다. cm를 2.54로 나누면 인치가 됩니다. "
                         "예를 들어 허리둘레 95cm는 약 37.4인치입니다.",
                "caption": "바지 인치는 표기값이라 실제 허리둘레와 1~2cm 차이가 날 수 있습니다.",
                "head": ["cm", "인치", "가까운 바지 인치"],
                "rows": [
                    ["70cm", "27.6인치", "28"],
                    ["75cm", "29.5인치", "29~30"],
                    ["80cm", "31.5인치", "31~32"],
                    ["85cm", "33.5인치", "33~34"],
                    ["90cm", "35.4인치", "35~36"],
                    ["95cm", "37.4인치", "37~38"],
                    ["100cm", "39.4인치", "39~40"],
                    ["105cm", "41.3인치", "41~42"],
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
            ("미국 브랜드는 알파벳이 한 칸 작습니다",
             "노스페이스 코리아 공식표는 95를 M으로 적지만, 랄프 로렌 코리아와 톰 브라운 공식표는 95를 S, 100을 M으로 적습니다. "
             "나이키도 같은 M을 미국 표에서는 가슴둘레 37.5~41인치(약 95~104cm), 아시아 표에서는 36~38인치(약 91~97cm)로 "
             "따로 안내합니다. 국내 브랜드에서 M(95)을 입는다면 미국 브랜드는 S부터 보고, 알파벳보다 한국 숫자와 가슴둘레로 고르세요. "
             "브랜드별 표는 <a href=\"/northface-size-chart/\">노스페이스</a>·<a href=\"/polo-ralph-lauren-size/\">폴로 랄프로렌</a>·"
             "<a href=\"/thom-browne-size-chart/\">톰브라운</a> 사이즈표에 정리했습니다."),
        ],
        "sources": ["한국 성인 남성복 치수 표기 관행(가슴둘레 기준)",
                    "노스페이스 코리아 공식몰 상품 사이즈 안내(재킷, 한국 사이즈·알파벳·신장)",
                    "랄프 로렌 코리아 공식몰 상품 사이즈 표(XS·90 ~ XXL·115)",
                    "톰 브라운 공식몰 사이즈 가이드(남성 XXS·85 ~ XXL·115)",
                    "몽클레어 한국 공식 사이즈 가이드(남성 아우터웨어 몸 가슴둘레·이탈리아 사이즈)",
                    "나이키 공식 남성 상의 사이즈표(미국·아시아, 몸 가슴둘레 인치)"],
        "faq": [
            ("남자 95 사이즈는 M인가요?",
             "국내 브랜드는 대부분 M입니다. 95는 가슴둘레 95cm를 뜻하며 노스페이스 코리아 공식표도 95를 M으로 적습니다. "
             "미국 브랜드는 한 칸 작게 적어, 랄프 로렌 코리아와 톰 브라운 공식표에서 95는 S입니다. 알파벳보다 숫자를 보세요."),
            ("미국 M은 한국 몇 사이즈인가요?",
             "100입니다. 랄프 로렌 코리아와 톰 브라운 공식표가 M을 100으로 적고, 나이키 미국 표의 M도 가슴둘레 37.5~41인치(약 95~104cm)입니다. "
             "국내 브랜드의 M(95)보다 한 칸 큽니다."),
            ("남자 95 사이즈는 키 몇 cm인가요?",
             "노스페이스 코리아 공식표로 키 165~175cm입니다. 90은 160~170cm, 100은 170~180cm입니다. 키보다 가슴둘레가 먼저입니다."),
            ("95 사이즈는 몸무게 몇 kg인가요?",
             "이 사이트에서 확인한 공식 사이즈표(노스페이스·파타고니아·랄프 로렌 코리아)는 몸무게 없이 가슴둘레와 키로 안내합니다. "
             "같은 몸무게라도 체형마다 가슴둘레가 달라, 가슴둘레를 재는 편이 정확합니다."),
            ("허리둘레 95cm는 몇 인치인가요?",
             "약 37.4인치입니다. cm를 2.54로 나누면 됩니다. 바지로는 37~38인치 제품을 보세요."),
            ("L·XL·XXL은 무슨 뜻인가요?",
             "L은 Large, XL은 Extra Large, XXL은 그보다 한 단계 큰 사이즈입니다. 국내 남성복으로는 L = 100, XL = 105, XXL = 110이고, "
             "미국 브랜드는 한 칸씩 밀려 L = 105입니다."),
            ("남자 100 사이즈는 알파벳으로 뭔가요?",
             "국내 브랜드는 L입니다(노스페이스 코리아 공식표). 미국 브랜드는 M으로, 랄프 로렌 코리아와 톰 브라운 공식표가 100을 M으로 적습니다."),
            ("95와 100 중에 뭘 골라야 하나요?",
             "가슴둘레를 재서 가까운 쪽을 고르세요. 97cm처럼 중간이면 원하는 핏으로 결정합니다. 딱 맞게 입으려면 95, 여유 있게 입으려면 100입니다."),
            ("바지 32인치는 몇 cm인가요?",
             "허리둘레 약 81cm입니다. 인치에 2.54를 곱하면 됩니다."),
            ("오버핏은 사이즈를 올려야 하나요?",
             "오버핏은 이미 여유량을 넣어 설계된 옷이라 정사이즈가 기본입니다. 표기 사이즈를 또 올리면 과하게 커집니다."),
        ],
        "related": [
            ("/clothing-size-women/", "여성 의류 사이즈", "55는 키 155·가슴 85에서 나온 숫자"),
            ("/hat-size/", "모자 사이즈", "57은 머리둘레 57cm"),
            ("/polo-ralph-lauren-size/", "폴로 사이즈", "M은 100, 보이즈 XL은 키 163~174"),
            ("/thom-browne-size-chart/", "톰브라운 사이즈표", "1은 95, 2는 100"),
            ("/northface-nuptse/", "눕시 사이즈", "095는 옷 가슴둘레 115.6cm"),
            ("/moncler-size-chart/", "몽클레어 사이즈표", "0·1·2·3은 한국 몇?"),
            ("/arcteryx-size-chart/", "아크테릭스 사이즈표", "M은 가슴둘레 102cm"),
            ("/northface-size-chart/", "노스페이스 사이즈표", "95는 M, 100은 L"),
            ("/canada-goose-size-chart/", "캐나다구스 사이즈표", "100은 M, 퓨전 핏은 L"),
            ("/patagonia-size-chart/", "파타고니아 사이즈표", "레트로-X·다운 스웨터 공식 핏"),
            ("/japan-size-chart/", "일본 사이즈표", "LL은 XL, O는 XL"),
            ("/china-size-chart/", "중국 사이즈표", "175/92A 읽는 법"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
    },
    {
        "slug": "clothing-size-women",
        "name": "여성 의류 사이즈",
        "title": "여자 옷 사이즈 44·55·66·77 뜻 — 키·가슴둘레 유래와 S·M·L 환산",
        "desc": "여자 55는 1981년 표기법에서 키 155cm·가슴둘레 85cm를 뜻했습니다. 지금은 공식 기준이 아니라 브랜드마다 다르고, "
                "보통 55는 S, 66은 M, 77은 L로 통합니다. 유래와 실측으로 고르는 법을 정리했습니다.",
        "eyebrow": "44 · 55 · 66 · 77",
        "h1": "55는 <em>키 155·가슴 85</em>에서 나왔습니다",
        "verdict_top": "먼저 알아둘 것",
        "verdict": "44·55·66은 브랜드마다 다릅니다",
        "verdict_sub": "톰 브라운 공식표는 44 = XS, 55 = S, 66 = M, 77 = L, 88 = XL로 적습니다. "
                       "1981년 표기법에서 55는 키 155cm·가슴둘레 85cm였지만 지금은 공식 기준이 아니라, "
                       "같은 55라도 브랜드마다 크기가 다릅니다. 실제 구매는 실측으로 확인하세요.",
        "tables": [
            {
                "h2": "44·55·66의 기준 치수(1981년)",
                "intro": "1980년 20대 여성 평균(키 155cm·가슴둘레 85cm)을 55로 정하고, 키는 5cm, 가슴둘레는 3cm씩 "
                         "더하고 빼서 만든 표기입니다.",
                "caption": "국가기술표준원 설명(중앙일보 2017-07-26 보도). 지금은 공식 사이즈 체계가 아니며, "
                           "브랜드마다 실제 크기가 다릅니다.",
                "head": ["사이즈", "키", "가슴둘레"],
                "rows": [[str(s), f"{h}cm", f"{b}cm"] for s, h, b in KS1981_W],
                "highlight": 0,
            },
            {
                "h2": "미국·이탈리아 사이즈와 비교",
                "intro": "톰 브라운 공식몰 가이드는 한국 44~88을 알파벳·미국·이탈리아 숫자와 나란히 적습니다. 그 값을 그대로 옮겼습니다.",
                "caption": "톰 브라운 공식몰 사이즈 가이드(여성). 출처마다 한 칸씩 다릅니다: 중앙일보(2017)는 미국 4·6을 55, "
                           "8·10을 66과 비교했고, 몽클레어 한국 공식 가이드는 S를 이탈리아 42로 적습니다.",
                "head": ["한국", "알파벳", "미국", "이탈리아"],
                "rows": [[str(k), s, str(us), it] for it, s, k, us in TB_WOMEN if 44 <= k <= 88],
                "highlight": 0,
            },
        ],
        "body": [
            ("왜 지금은 표준이 없을까",
             "44·55·66은 1981년에 정한 표기법에서 나왔습니다. 1980년 20대 여성 평균 키 155cm와 가슴둘레 85cm의 "
                "끝자리를 따 55를 기준으로 삼았습니다. 하지만 80년대 후반부터 평균 체격이 달라지면서 더는 공식 체계가 아니게 됐고, "
                "정부는 1990년부터 옷에 신체 치수를 직접 적도록 권고했습니다. 그래서 지금은 브랜드가 각자 기준을 잡아, "
                "같은 55라도 매장마다 실제 크기가 다릅니다. 남성복 95·100이 지금도 가슴둘레를 뜻하는 것과 다른 점입니다."),
            ("그래서 실측을 봐야 합니다",
             "온라인 상품 페이지의 '가슴단면·어깨너비·총장·소매길이'가 유일하게 신뢰할 수 있는 값입니다. "
                "가슴단면은 옷을 눕혀 놓고 잰 한쪽 폭이므로, 몸의 가슴둘레와 비교하려면 2를 곱하세요. "
                "여기에 여유량 4~6cm를 더한 값이 편하게 맞는 범위입니다."),
            ("가장 확실한 방법은 옷장에 있습니다",
             "지금 가지고 있는 옷 중 가장 잘 맞는 것을 골라 평평하게 펴고 가슴단면·어깨너비·총장을 재세요. "
                "그 숫자를 상품 페이지 실측과 비교하면 표기 사이즈가 무엇이든 실패하지 않습니다. "
                "사이즈 숫자를 맞추는 게 아니라 치수를 맞추는 것이 핵심입니다."),
            ("해외 숫자는 출처마다 한 칸씩 다릅니다",
             "톰 브라운 공식표는 55를 미국 4·이탈리아 40으로 적지만, 몽클레어 한국 공식 가이드는 S를 이탈리아 42로 적고, "
                "중앙일보(2017)는 미국 4·6을 55, 8·10을 66과 비교합니다. 해외 브랜드는 그 브랜드 사이즈표의 가슴둘레(cm)를 "
                "내 몸 치수와 맞춰 고르세요. 브랜드별 표는 <a href=\"/thom-browne-size-chart/\">톰브라운</a>·"
                "<a href=\"/moncler-size-chart/\">몽클레어</a> 사이즈표에 정리했습니다."),
        ],
        "sources": ["국가기술표준원 설명 — 1981년 여성복 치수 표기(중앙일보 2017-07-26 '44·55 사이즈, 대체 무슨 뜻?', 미국 사이즈 비교 포함)",
                    "톰 브라운 공식몰 사이즈 가이드(여성 한국·알파벳·미국·이탈리아 표기)",
                    "몽클레어 한국 공식 사이즈 가이드(여성 아우터웨어)"],
        "faq": [
            ("여자 55는 알파벳으로 뭔가요?",
             "톰 브라운 공식표는 S로 적습니다. 다만 중앙일보(2017)처럼 55를 M으로 보는 곳도 있어, 같은 55라도 브랜드 표를 확인하세요."),
            ("55 사이즈는 미국 몇인가요?",
             "톰 브라운 공식표로 미국 4, 이탈리아 40입니다. 44는 미국 2·이탈리아 38, 66은 미국 6·이탈리아 42입니다. "
             "중앙일보(2017)는 미국 4·6을 55, 8·10을 66과 비교하는 등 출처마다 한 칸쯤 다릅니다."),
            ("66과 77은 알파벳으로 뭔가요?",
             "톰 브라운 공식표로 66은 M, 77은 L입니다. 44는 XS, 88은 XL입니다. 브랜드에 따라 한 단계씩 어긋날 수 있습니다."),
            ("55 사이즈는 키 몇 cm인가요?",
             "1981년 표기법 기준으로 키 155cm·가슴둘레 85cm입니다. 44는 150cm·82cm, 66은 160cm·88cm입니다. "
             "지금은 브랜드마다 달라 실측을 보세요."),
            ("여자 55 사이즈는 몸무게 몇 kg인가요?",
             "1981년 표기법도 키와 가슴둘레로만 정했고 몸무게 기준은 없습니다. 같은 몸무게라도 체형에 따라 맞는 사이즈가 달라, "
             "가슴둘레와 상품 실측으로 고르세요."),
            ("44·55·66 사이에 정확한 환산표가 있나요?",
             "지금은 없습니다. 1981년 표기법(55 = 키 155cm·가슴둘레 85cm)이 있었지만 더는 공식 체계가 아니라, "
             "브랜드마다 기준이 다릅니다. 실측을 확인하는 방법뿐입니다."),
            ("실측에서 가슴단면이 뭔가요?",
             "옷을 평평하게 놓고 겨드랑이 아래를 가로로 잰 한쪽 폭입니다. 몸의 가슴둘레와 비교하려면 2를 곱하세요."),
            ("프리사이즈는 어떤 크기인가요?",
             "대체로 55~66 사이를 겨냥하지만 이것도 브랜드마다 다릅니다. 반드시 실측을 확인하세요."),
        ],
        "related": [
            ("/clothing-size-men/", "남성 의류 사이즈", "숫자가 곧 가슴둘레 cm"),
            ("/pants-size-women/", "여자 바지 사이즈", "26은 허리 66~67cm"),
            ("/bra-size/", "브라 사이즈", "75B는 차이 12.5cm"),
            ("/thom-browne-size-chart/", "톰브라운 사이즈표", "여성 40은 55"),
            ("/northface-nuptse/", "눕시 사이즈", "095는 옷 가슴둘레 115.6cm"),
            ("/moncler-size-chart/", "몽클레어 사이즈표", "0·1·2·3은 한국 몇?"),
            ("/arcteryx-size-chart/", "아크테릭스 사이즈표", "M은 가슴둘레 102cm"),
            ("/northface-size-chart/", "노스페이스 사이즈표", "95는 M, 100은 L"),
            ("/canada-goose-size-chart/", "캐나다구스 사이즈표", "100은 M, 퓨전 핏은 L"),
            ("/patagonia-size-chart/", "파타고니아 사이즈표", "레트로-X·다운 스웨터 공식 핏"),
            ("/japan-size-chart/", "일본 사이즈표", "LL은 XL, O는 XL"),
            ("/china-size-chart/", "중국 사이즈표", "175/92A 읽는 법"),
            ("/", "신발 사이즈 환산표", "mm · US · UK · EU · JP"),
        ],
    },
]


def build(p):
    sections = []
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
        sections.append(f"""
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
""")
    # 첫 표는 넓은 화면에서 결론 옆에 선다
    first_table, rest_tables = sections[0], "".join(sections[1:])
    vlen = len(p["verdict"])
    vcls = " is-xlong" if vlen > 26 else " is-long" if vlen > 14 else ""

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
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v=5">
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
    {NAV}
  </div>
</header>

<main class="wrap">

  <p class="crumb"><a href="/">전체 환산표</a> / {p['name']}</p>

  <div class="lead">

  <div class="hero">
    <p class="eyebrow">{p['eyebrow']}</p>
    <h1>{p['h1']}</h1>
  </div>

  <div class="verdict{vcls}">
    <div class="verdict-top">{p['verdict_top']}</div>
    <div class="verdict-body">
      <strong>{keep_phrases(p['verdict'])}</strong>
      <p>{p['verdict_sub']}</p>
    </div>
  </div>
{first_table}
  </div>
{rest_tables}
  <section class="notes">
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
  <p class="disclaimer">최종 수정 __UPDATED__ · <a href="/about/">사이트 소개</a> · <a href="/privacy/">개인정보처리방침</a></p>
</footer>

</body>
</html>
"""


if __name__ == "__main__":
    assert KS1981_W[1] == (55, 155, 85) and KS1981_W[-1] == (88, 170, 94)
    # 미국 브랜드 알파벳: 톰 브라운과 랄프 로렌 코리아 공식표가 겹치는 칸에서 같다
    assert all(US_M[k] == s for s, k, _, _ in RL_MEN)
    assert [it_size(k) for k in range(85, 120, 5)] == ["42", "44·46", "48", "50", "52", "54", "54·56"]
    men, women = PAGES
    top, pants = men["tables"][0]["rows"], men["tables"][2]["rows"]
    assert top[2] == ["95", "95cm 내외", "M", "S", "48"] and top[3] == ["100", "100cm 내외", "L", "M", "50"]
    assert pants[2] == ["32", "81cm", "40.6cm"] and pants[-1] == ["38", "97cm", "48.3cm"]
    assert [r[:3] for r in women["tables"][1]["rows"]] == [["44", "XS", "2"], ["55", "S", "4"], ["66", "M", "6"],
                                                         ["77", "L", "8"], ["88", "XL", "10"]]
    for p in PAGES:
        os.makedirs(p["slug"], exist_ok=True)
        path = os.path.join(p["slug"], "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(stamp(path, build(p)))
        print("wrote", path)
    print()
    print("사이트맵을 갱신하려면: python3 build_sitemap.py")
