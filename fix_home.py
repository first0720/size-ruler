# -*- coding: utf-8 -*-
"""
fix_home.py — index.html(홈) 정리 (한 번만 실행)
1) 목록 아래 깨진 안내문·중복 태그 제거 (실제 화면에 보이던 문제)
2) 크록스 카드 닫는 태그 + 260 숫자 복구
3) 빠져 있던 모델 카드 4개 추가 (조던 1, 슈퍼스타, 에어맥스 97, 젤카야노 14)
4) '다른 사이즈도 찾으시나요'에 뉴발란스 발볼 가이드 링크 추가
바꾸기 전 index.html.backup 을 남깁니다.
"""
import os, sys, shutil, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = "index.html"
if not os.path.exists(T):
    print("index.html이 이 폴더에 없습니다. 저장소 폴더(size-ruler 안쪽)에 넣고 실행하세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

raw = open(T, "rb").read().decode("utf-8-sig")
crlf = "\r\n" in raw
text = raw.replace("\r\n", "\n")
done, missing = [], []

def swap(label, old, new, must=True):
    global text
    if new and new in text and old not in text:
        return
    if old in text:
        text = text.replace(old, new, 1); done.append(label)
    elif must:
        missing.append(label)

# 1) 깨진 꼬리 제거
JUNK_START = '\n    </div>\n    <div class="brand-pick up">260</div>\n\n    <div class="brand-pick up">260</div>\n  </div>|'
if JUNK_START in text:
    s = text.index(JUNK_START)
    end_marker = '<p class="note-band">모델명을 누르면 발볼별 상세 가이드로 이동합니다.'
    e = text.index(end_marker, s)
    text = text[:s] + '\n\n    </div>\n    ' + text[e:]
    done.append("깨진 안내문·중복 태그 제거")
elif '지금 커서 위치' not in text:
    pass
else:
    missing.append("깨진 안내문 제거")

# 2) 크록스 카드 복구
swap("크록스 카드 복구",
'<span class="src">근거: 크록스 공식 사이즈 차트 · 착용 후기 다수</span></div>\n  <div class="brand" data-offset="0">',
'''<span class="src">근거: 크록스 공식 사이즈 차트 · 착용 후기 다수</span></div>
    </div>
    <div class="brand-pick up">260</div>
  </div>

  <div class="brand" data-offset="0">''')

# 3) 빠진 카드 4개 추가
def card(slug, name, offset, note, src):
    pick = 270 + offset
    cls = "brand-pick" if offset == 0 else "brand-pick up"
    return (f'  <div class="brand" data-offset="{offset}">\n'
            f'    <div>\n'
            f'      <div class="brand-name"><a href="/{slug}/">{name}</a></div>\n'
            f'      <div class="brand-note">{note}\n'
            f'        <span class="src">근거: {src}</span></div>\n'
            f'    </div>\n'
            f'    <div class="{cls}">{pick}</div>\n'
            f'  </div>\n')

NEW = "\n" + "\n".join([
    card("nike-air-jordan-1", "나이키 에어 조던 1", 0,
         "정사이즈. 길이는 표기대로 나옵니다. 앞코 높이가 낮아 발등이 높거나 발볼이 넓으면 반 사이즈 업.",
         "나이키 공식 사이즈 가이드 · KREAM 조던 1 상품 정보 · 착용 후기 다수"),
    card("adidas-superstar", "아디다스 슈퍼스타", -5,
         "반 사이즈(5mm) 다운. 고무 쉘토가 앞으로 길게 뻗어 표기보다 길게 나옵니다. 발볼이 넓으면 정사이즈.",
         "아디다스 공식 사이즈 가이드 · KREAM 슈퍼스타 상품 정보 · 착용 후기 다수"),
    card("nike-air-max-97", "나이키 에어맥스 97", 5,
         "반 사이즈(5mm) 업. 길이보다 폭이 문제입니다. 발볼이 넓으면 한 사이즈 업, 칼발이면 정사이즈도 가능합니다.",
         "나이키 공식 사이즈 가이드 · KREAM 에어맥스 97 상품 정보 · 착용 후기 다수"),
    card("asics-gel-kayano-14", "아식스 젤카야노 14", 0,
         "정사이즈. 길이는 표기대로입니다. 앞코 폭이 좁은 편이라 발볼이 넓으면 반 사이즈 업.",
         "아식스 공식 사이즈 차트(mm·US) · KREAM 젤카야노 14 상품 정보 · 착용 후기 다수"),
]) + "\n"

TAIL = '''    <div class="brand-pick">270</div>
  </div>


    </div>
    <p class="note-band">'''
if "/nike-air-jordan-1/" in text:
    pass
elif TAIL in text:
    text = text.replace(TAIL, '''    <div class="brand-pick">270</div>
  </div>
''' + NEW + '''
    </div>
    <p class="note-band">''', 1)
    done.append("빠진 모델 카드 4개 추가")
else:
    missing.append("모델 카드 4개 추가 위치")

# 4) 발볼 가이드 링크
swap("발볼 가이드 링크 추가",
'<a href="/clothing-size-women/">여성 의류 사이즈<span>44·55·66에 정확한 환산표가 없는 이유</span></a>',
'<a href="/clothing-size-women/">여성 의류 사이즈<span>44·55·66에 정확한 환산표가 없는 이유</span></a>\n      '
'<a href="/newbalance-width/">뉴발란스 발볼 D·2E·4E<span>길이는 맞는데 옆이 눌린다면</span></a>')

if missing:
    print("다음 부분을 찾지 못해 아무것도 바꾸지 않았습니다:")
    for m in missing: print("  -", m)
    print("index.html을 다시 보내주세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

# 구조 점검
open_n, close_n = text.count("<div"), text.count("</div>")
if open_n != close_n:
    print(f"태그 수가 맞지 않아 저장하지 않았습니다 (여는 div {open_n}, 닫는 div {close_n}).")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)
cards = len(re.findall(r'brand-name"><a href="/', text))

if done:
    shutil.copyfile(T, T + ".backup")
    out = text.replace("\n", "\r\n") if crlf else text
    open(T, "w", encoding="utf-8", newline="").write(out)
    print("수정 완료:")
    for d in done: print("  -", d)
    print(f"\n모델 카드 {cards}개, div 태그 {open_n}쌍 균형 확인")
    print("원본은 index.html.backup 으로 남겨뒀습니다.")
else:
    print("이미 모두 수정되어 있습니다.")
print("\n끝! 이제 GitHub Desktop에서 Commit -> Push origin 하세요.")
