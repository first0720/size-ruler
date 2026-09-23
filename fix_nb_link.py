# -*- coding: utf-8 -*-
"""
fix_nb_link.py — 뉴발란스 모델 페이지에서 발볼 가이드로 링크 (한 번만 실행)
build_models.py 템플릿의 '발볼별 가이드' 섹션 아래에,
슬러그가 newbalance- 로 시작하는 모델에만 안내 한 줄을 넣는다.
수정 후 build_models.py 실행. 이 파일은 스스로 삭제.
"""
import os, sys, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = "build_models.py"
if not os.path.exists(T):
    print("build_models.py가 이 폴더에 없습니다. 저장소 폴더(size-ruler 안쪽)에 넣고 실행하세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

text = open(T, "rb").read().decode("utf-8-sig")
crlf = "\r\n" in text
text = text.replace("\r\n", "\n")
done = []

# 1) 링크 문구 만들기 (뉴발란스 모델에만)
OLD_W = '''    widths = "".join(
        f'<div class="width-row"><dt>{w}</dt><dd>{t}</dd></div>\\n      '
        for w, t in m["widths"])'''
NEW_W = OLD_W + '''

    width_note = ""
    if m["slug"].startswith("newbalance-"):
        width_note = (
            '\\n    <p class="width-guide-link">뉴발란스는 같은 길이에서도 폭을 고를 수 있습니다. '
            '<a href="/newbalance-width/">D·2E·4E 발볼 가이드</a>에서 '
            '내 발 너비에 맞는 폭을 mm로 확인하세요.</p>')'''

if "width_note" in text:
    pass
elif OLD_W in text:
    text = text.replace(OLD_W, NEW_W, 1); done.append("뉴발란스 판별 문구 추가")
else:
    print("widths 부분을 찾지 못했습니다. build_models.py를 다시 보내주세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

# 2) 템플릿에 끼워넣기
OLD_S = """    <h2>발볼별 가이드</h2>
    <dl class="width-grid">
      {widths.rstrip()}
    </dl>
  </section>"""
NEW_S = """    <h2>발볼별 가이드</h2>
    <dl class="width-grid">
      {widths.rstrip()}
    </dl>{width_note}
  </section>"""
if "{width_note}" in text:
    pass
elif OLD_S in text:
    text = text.replace(OLD_S, NEW_S, 1); done.append("발볼별 가이드 섹션에 링크 삽입")
else:
    print("발볼별 가이드 섹션을 찾지 못했습니다. build_models.py를 다시 보내주세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

if done:
    out = text.replace("\n", "\r\n") if crlf else text
    open(T, "w", encoding="utf-8", newline="").write(out)
    print("수정 완료:")
    for d in done: print("  -", d)
else:
    print("이미 수정되어 있습니다.")

print("\n페이지 재생성 중...")
r = subprocess.run([sys.executable, "build_models.py"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("build_models.py 실행 오류:\n", r.stderr); input(); sys.exit(1)
print("  모델 페이지", r.stdout.count("wrote"), "개 생성")

n = 0
for d in os.listdir("."):
    p = os.path.join(d, "index.html")
    if d.startswith("newbalance-") and os.path.exists(p):
        if "/newbalance-width/" in open(p, encoding="utf-8").read():
            n += 1
print(f"  뉴발란스 페이지 {n}개에 링크 확인")

try:
    os.remove(os.path.abspath(__file__))
    print("\nfix_nb_link.py는 할 일을 마쳐서 삭제했습니다.")
except Exception:
    pass
print("\n끝! 이제 GitHub Desktop에서 Commit -> Push origin 하세요.")
