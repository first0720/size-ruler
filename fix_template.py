# -*- coding: utf-8 -*-
"""
fix_template.py — build_models.py 템플릿 수정 (한 번만 실행)
1) 오타: 괜찰 -> 괜찮
2) 조사: '{이름}는 정사이즈라' -> 받침에 따라 '은/는' 자동 선택
3) 다른 모델: 3개 -> 6개 (같은 브랜드 먼저)
수정 후 build_models.py, build_sitemap.py 실행, 이 파일은 스스로 삭제.
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
TARGET = "build_models.py"

if not os.path.exists(TARGET):
    print("build_models.py가 이 폴더에 없습니다. 저장소 폴더(size-ruler 안쪽)에 넣고 다시 실행하세요.")
    input("Enter를 누르면 닫힙니다."); sys.exit(1)

with open(TARGET, "rb") as f:
    raw = f.read()
text = raw.decode("utf-8-sig")
crlf = "\r\n" in text
text = text.replace("\r\n", "\n")
changed = []

# 1) 오타
if "괜찰" in text:
    text = text.replace("괜찰", "괜찮")
    changed.append("오타 수정 (괜찰 -> 괜찮)")

# 2) 조사 함수 추가 + 템플릿 교체
JOSA_FUNC = '''def eun_neun(word):
    """단어 끝 글자의 받침을 보고 '은' 또는 '는'을 돌려준다. 숫자·영문도 읽는 소리로 판단."""
    ch = word.strip()[-1]
    if "가" <= ch <= "힣":
        return "은" if (ord(ch) - 0xAC00) % 28 else "는"
    if ch.isdigit():
        return "는" if ch in "2459" else "은"   # 이·사·오·구 = 받침 없음
    if ch.upper() in "LMNR":                    # 엘·엠·엔·알 = 받침 있음
        return "은"
    return "는"


def build(m, others):'''
if "def eun_neun(" not in text:
    if "def build(m, others):" not in text:
        print("build 함수 위치를 못 찾았습니다. 파일을 다시 보내주세요."); input(); sys.exit(1)
    text = text.replace("def build(m, others):", JOSA_FUNC, 1)
    changed.append("조사 함수 추가")

OLD = "f\"{m['name']}는 정사이즈라"
NEW = "f\"{m['name']}{eun_neun(m['name'])} 정사이즈라"
if OLD in text:
    text = text.replace(OLD, NEW)
    changed.append("정사이즈 안내 문장 조사 자동화")

# 3) 다른 모델 개수
if "others = (siblings + rest)[:3]" in text:
    text = text.replace("others = (siblings + rest)[:3]", "others = (siblings + rest)[:6]")
    changed.append("다른 모델 3개 -> 6개")

if not changed:
    print("이미 모두 수정되어 있습니다. 바꿀 것이 없습니다.")
else:
    out = text.replace("\n", "\r\n") if crlf else text
    with open(TARGET, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("수정 완료:")
    for c in changed:
        print("  -", c)

print("\n페이지 재생성 중...")
py = sys.executable
r1 = subprocess.run([py, "build_models.py"], capture_output=True, text=True, encoding="utf-8")
if r1.returncode != 0:
    print("build_models.py 실행 오류:\n", r1.stderr); input(); sys.exit(1)
print("  모델 페이지", r1.stdout.count("wrote"), "개 생성")
if os.path.exists("build_sitemap.py"):
    subprocess.run([py, "build_sitemap.py"], capture_output=True, text=True, encoding="utf-8")
    print("  사이트맵 갱신")

try:
    os.remove(os.path.abspath(__file__))
    print("\nfix_template.py는 할 일을 마쳐서 삭제했습니다.")
except Exception:
    pass
print("\n끝! 이제 GitHub Desktop에서 Commit -> Push origin 하세요.")
