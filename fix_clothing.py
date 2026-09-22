# -*- coding: utf-8 -*-
"""
fix_clothing.py — 의류 페이지 2개 제목·설명·내용 개선 (한 번만 실행)
Search Console 검색어(95 사이즈, 95cm 인치, 44 55 66 등)에 맞춰 수정.
수정 후 build_clothing.py, build_sitemap.py 실행, 이 파일은 스스로 삭제.
"""
import os, sys, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
TARGET = "build_clothing.py"
if not os.path.exists(TARGET):
    print("build_clothing.py가 이 폴더에 없습니다. 저장소 폴더(size-ruler 안쪽)에 넣고 다시 실행하세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

text = open(TARGET, "rb").read().decode("utf-8-sig")
crlf = "\r\n" in text
text = text.replace("\r\n", "\n")

R = []  # (설명, 원래 문장, 바꿀 문장)

# ── 남성 ─────────────────────────────────────────
R.append(("남성 제목",
'"title": "남자 옷 사이즈표 — 95·100·105가 뜻하는 것과 S/M/L 환산",',
'"title": "남자 옷 사이즈 95·100·105 뜻 — M·L·XL 환산표, 허리 cm↔인치",'))

R.append(("남성 설명",
'''"desc": "한국 남성복 사이즈 숫자는 가슴둘레(cm)입니다. 95·100·105를 S/M/L, "
                "US·EU 사이즈로 환산하고 재는 법까지 정리했습니다.",''',
'''"desc": "남자 95는 M, 100은 L, 105는 XL입니다. 숫자는 가슴둘레 cm라는 뜻입니다. "
                "허리 95cm가 몇 인치인지, 바지 인치↔cm 환산표와 재는 법까지 한 번에 정리했습니다.",'''))

R.append(("남성 핵심 요약",
'''"verdict_sub": "95를 입는다면 가슴둘레가 95cm라는 뜻입니다. 하의 인치 숫자는 허리둘레 인치입니다. "
                       "남성복은 이 규칙만 알면 대부분 해결됩니다.",''',
'''"verdict_sub": "90 = S, 95 = M, 100 = L, 105 = XL, 110 = XXL. "
                       "95를 입는다면 가슴둘레가 95cm라는 뜻입니다. 하의 인치 숫자는 허리둘레 인치입니다. "
                       "남성복은 이 규칙만 알면 대부분 해결됩니다.",'''))

R.append(("하의 표 한국 사이즈 정정",
'''                    ["28", "71cm", "76", "S", "28"],
                    ["30", "76cm", "82", "M", "30"],
                    ["32", "81cm", "87", "L", "32"],
                    ["34", "86cm", "92", "XL", "34"],
                    ["36", "91cm", "97", "XXL", "36"],
                    ["38", "97cm", "102", "XXXL", "38"],
                ],
                "highlight": 0,
            },
        ],''',
'''                    ["28", "71cm", "72", "S", "28"],
                    ["30", "76cm", "76", "M", "30"],
                    ["32", "81cm", "82", "L", "32"],
                    ["34", "86cm", "86", "XL", "34"],
                    ["36", "91cm", "92", "XXL", "36"],
                    ["38", "97cm", "97", "XXXL", "38"],
                ],
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
        ],'''))

R.append(("남성 FAQ 추가",
'''        "faq": [
            ("남자 100 사이즈는 알파벳으로 뭔가요?",''',
'''        "faq": [
            ("남자 95 사이즈는 M인가요?",
             "네, M입니다. 95는 가슴둘레 95cm를 뜻하며 US·EU 기준으로도 대체로 M에 해당합니다. 90은 S, 100은 L입니다."),
            ("허리둘레 95cm는 몇 인치인가요?",
             "약 37.4인치입니다. cm를 2.54로 나누면 됩니다. 바지로는 37~38인치 제품을 보세요."),
            ("L·XL·XXL은 무슨 뜻인가요?",
             "L은 Large, XL은 Extra Large, XXL은 그보다 한 단계 큰 사이즈입니다. 한국 남성복으로는 L = 100, XL = 105, XXL = 110입니다."),
            ("남자 100 사이즈는 알파벳으로 뭔가요?",'''))

# ── 여성 ─────────────────────────────────────────
R.append(("여성 제목",
'"title": "여자 옷 사이즈 44·55·66 — 정확한 환산표가 없는 이유",',
'"title": "여자 옷 사이즈 44·55·66·77 — S·M·L 환산표와 브랜드별 차이",'))

R.append(("여성 설명",
'''"desc": "여성복 44·55·66·77은 국가 표준이 아니라 브랜드마다 기준이 다릅니다. "
                "통용되는 대응과 함께, 실측으로 고르는 방법을 정리했습니다.",''',
'''"desc": "여자 55는 보통 S, 66은 M, 77은 L입니다. 44·55·66·77을 알파벳·US·EU로 환산하고, "
                "브랜드마다 크기가 다른 이유와 실측으로 고르는 법을 정리했습니다.",'''))

R.append(("여성 핵심 요약",
'''"verdict_sub": "남성복 숫자와 달리 여성복 숫자는 신체 치수를 뜻하지 않습니다. "''',
'''"verdict_sub": "보통 44 = XS, 55 = S, 66 = M, 77 = L, 88 = XL로 통합니다. "
                       "다만 남성복 숫자와 달리 여성복 숫자는 신체 치수를 뜻하지 않습니다. "'''))

R.append(("여성 FAQ 추가",
'''            ("여자 55는 알파벳으로 뭔가요?",
             "일반적으로 S에 대응합니다. 다만 브랜드마다 기준이 달라서, 같은 55라도 실제 크기는 차이가 납니다."),''',
'''            ("여자 55는 알파벳으로 뭔가요?",
             "일반적으로 S에 대응합니다. 다만 브랜드마다 기준이 달라서, 같은 55라도 실제 크기는 차이가 납니다."),
            ("66과 77은 알파벳으로 뭔가요?",
             "보통 66은 M, 77은 L로 통합니다. 44는 XS, 88은 XL입니다. 브랜드에 따라 한 단계씩 어긋날 수 있습니다."),'''))

done, skipped, missing = [], [], []
for name, old, new in R:
    if new in text:
        skipped.append(name)
    elif old in text:
        text = text.replace(old, new, 1); done.append(name)
    else:
        missing.append(name)

if missing:
    print("다음 부분을 파일에서 찾지 못해 아무것도 바꾸지 않았습니다:")
    for m in missing: print("  -", m)
    print("build_clothing.py를 다시 보내주세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

if done:
    out = text.replace("\n", "\r\n") if crlf else text
    open(TARGET, "w", encoding="utf-8", newline="").write(out)
    print("수정 완료:")
    for d in done: print("  -", d)
else:
    print("이미 모두 수정되어 있습니다.")

print("\n페이지 재생성 중...")
py = sys.executable
r = subprocess.run([py, "build_clothing.py"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("build_clothing.py 실행 오류:\n", r.stderr); input(); sys.exit(1)
print("  의류 페이지", r.stdout.count("wrote"), "개 생성")
if os.path.exists("build_sitemap.py"):
    subprocess.run([py, "build_sitemap.py"], capture_output=True, text=True, encoding="utf-8")
    print("  사이트맵 갱신")

try:
    os.remove(os.path.abspath(__file__))
    print("\nfix_clothing.py는 할 일을 마쳐서 삭제했습니다.")
except Exception:
    pass
print("\n끝! 이제 GitHub Desktop에서 Commit -> Push origin 하세요.")
