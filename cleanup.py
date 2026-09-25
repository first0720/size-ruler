# cleanup.py - sizeruler 정리 도구 (한 번 실행)
# 사용법: build_models.py 가 있는 폴더에 넣고   python cleanup.py
# 하는 일:
#   1) 404.html 을 build_models.py 의 MODELS 기준으로 다시 만든다 (모델 전부 + 애드센스 + 개인정보 링크)
#   2) build_models.py / build_clothing.py 템플릿 푸터에 개인정보처리방침 링크를 넣는다 (없을 때만)
#   3) 손으로 만든 페이지(kids-shoe-size, kids-clothing-size, ring-size) 푸터에도 같은 링크를 넣는다
#   4) build_models.py, build_clothing.py, build_sitemap.py 를 실행한다
import ast, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ADS = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
       '?client=ca-pub-8018650083353602" crossorigin="anonymous"></script>')
PRIV = '<p class="disclaimer"><a href="/privacy/">개인정보처리방침</a></p>'
EXTRA = [
    ("/kids-shoe-size/", "아동 신발 사이즈", "발 길이 + 10mm"),
    ("/kids-clothing-size/", "아동 의류 사이즈", "숫자 = 아이 키(cm)"),
    ("/ring-size/", "반지 호수", "둘레 − 43 = 호수"),
    ("/clothing-size-men/", "남성 의류 사이즈", "95·100·105와 S/M/L 환산"),
    ("/clothing-size-women/", "여성 의류 사이즈", "44·55·66 알아보기"),
]


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(path, text, nl="\n"):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", nl))


def load_models():
    src, _ = read(os.path.join(ROOT, "build_models.py"))
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "MODELS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError("build_models.py 에서 MODELS 를 찾지 못했습니다")


def build_404(models):
    links = ['<a href="/">전체 신발 사이즈 환산표<span>mm · US · UK · EU · JP</span></a>']
    for m in models:
        links.append(f'<a href="/{m["slug"]}/">{m["name"]}<span>{m["verdict"]}</span></a>')
    for href, name, sub in EXTRA:
        links.append(f'<a href="{href}">{name}<span>{sub}</span></a>')
    body = "\n      ".join(links)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지를 찾을 수 없습니다 — 사이즈 자</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>

<header class="masthead">
  <div class="wrap mark">
    <b><a href="/" style="text-decoration:none;color:inherit">사이즈 자</a></b>
    <span>404</span>
  </div>
</header>

<main class="wrap">
  <div class="hero">
    <p class="eyebrow">찾을 수 없는 주소</p>
    <h1>이 눈금은 <em>자에 없습니다</em></h1>
    <p class="lede">주소가 바뀌었거나 잘못 입력됐습니다. 찾으시던 사이즈 정보는 아래에 있습니다.</p>
  </div>

  <section style="padding-top:10px">
    <h2>모델별 사이즈 가이드</h2>
    <div class="related">
      {body}
    </div>
  </section>
</main>

<footer class="wrap">
  <div>사이즈 자 — 신발 사이즈 환산표</div>
  {PRIV}
</footer>

</body>
</html>
"""


def patch_footer(path, label):
    """</footer> 앞에 개인정보 링크를 넣는다. 이미 있으면 건너뜀."""
    if not os.path.exists(path):
        print(f"  - {label}: 파일 없음, 건너뜀")
        return
    src, nl = read(path)
    if "/privacy/" in src:
        print(f"  - {label}: 이미 링크 있음, 건너뜀")
        return
    if "</footer>" not in src:
        print(f"  - {label}: </footer> 를 찾지 못해 건너뜀")
        return
    lines = src.split("\n")
    idx = next(i for i, l in enumerate(lines) if "</footer>" in l)
    indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
    lines.insert(idx, indent + "  " + PRIV)
    out = "\n".join(lines)
    if path.endswith(".py"):
        compile(out, path, "exec")
    write(path, out, nl)
    print(f"  - {label}: 링크 추가")


def run(script):
    p = os.path.join(ROOT, script)
    if not os.path.exists(p):
        print(f"  - {script}: 없음, 건너뜀")
        return
    print(f"--- {script} 실행 ---")
    r = subprocess.run([sys.executable, p], cwd=ROOT)
    if r.returncode != 0:
        print(f"  ! {script} 실행 중 오류 (위 메시지 확인). 나머지는 계속 진행합니다.")


def main():
    os.chdir(ROOT)
    models = load_models()
    print(f"모델 {len(models)}개 확인")

    print("1) 404.html 재생성")
    write(os.path.join(ROOT, "404.html"), build_404(models))
    print(f"  - 404.html: 모델 {len(models)}개 + 기타 {len(EXTRA)}개 링크")

    print("2) 템플릿 푸터에 개인정보처리방침 링크")
    patch_footer(os.path.join(ROOT, "build_models.py"), "build_models.py")
    patch_footer(os.path.join(ROOT, "build_clothing.py"), "build_clothing.py")

    print("3) 수작업 페이지 푸터에 링크")
    for d in ("kids-shoe-size", "kids-clothing-size", "ring-size"):
        patch_footer(os.path.join(ROOT, d, "index.html"), d)

    print("4) 페이지·사이트맵 재생성")
    run("build_models.py")
    run("build_clothing.py")
    run("build_sitemap.py")

    print("\n=== 완료 === GitHub Desktop에서 Commit → Push origin 하세요.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n!!! 오류:", e)
        print("파일을 바꾸다 실패했다면 GitHub Desktop 에서 Discard changes 로 되돌릴 수 있습니다.")
        sys.exit(1)
