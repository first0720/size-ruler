# add_models.py - sizeruler 모델 일괄 추가 도구
# 사용법: 이 파일과 batch 파일을 size-ruler 폴더(build_models.py 있는 곳)에 넣고
#         명령창에서   python add_models.py
# 하는 일: batch 파일의 모델 데이터를 build_models.py에, 카드를 index.html에 넣고
#         build_models.py / build_sitemap.py 를 실행한 뒤 batch 파일을 지웁니다.
import ast, glob, os, re, subprocess, sys, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD, INDEX = "build_models.py", "index.html"
MARK = "SIZERULER_BATCH"


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(path, text, nl):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", nl))


def find_batches():
    found, me = [], os.path.abspath(__file__)
    for p in sorted(glob.glob(os.path.join(ROOT, "*.py"))):
        if os.path.abspath(p) == me or os.path.basename(p).startswith("build_"):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                first = f.readline()
        except Exception:
            continue
        if MARK in first:
            found.append(p)
    return found


def load_batch(path):
    name = "batch_" + re.sub(r"\W", "_", os.path.basename(path))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MODELS_BLOCK.strip("\n"), mod.CARDS_BLOCK.strip("\n")


def split_models(block):
    """'    {' 로 시작하는 모델 블록 단위로 나누고 slug를 뽑는다. 문법도 검증."""
    out = []
    for ch in re.split(r"(?m)^(?=    \{[ \t]*$)", block):
        ch = ch.strip("\n")
        if not ch:
            continue
        d = ast.literal_eval("(" + ch.strip().rstrip(",") + ")")
        if not isinstance(d, dict) or "slug" not in d:
            raise ValueError("모델 블록 형식이 이상합니다")
        out.append((d["slug"], ch))
    return out


def split_cards(block):
    out = []
    for ch in re.split(r'(?m)^(?=[ \t]*<div class="brand" data-offset=)', block):
        ch = ch.strip("\n")
        if not ch:
            continue
        m = re.search(r'href="/([^/"]+)/"', ch)
        if not m:
            raise ValueError("카드 블록에서 링크를 찾을 수 없습니다")
        out.append((m.group(1), ch))
    return out


def insert_models(src, models):
    lines = src.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith("MODELS = [")), None)
    if start is None:
        raise ValueError("build_models.py 에서 'MODELS = [' 를 찾지 못했습니다")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "]"), None)
    if end is None:
        raise ValueError("build_models.py 에서 MODELS 리스트의 끝 ']' 를 찾지 못했습니다")
    j = end - 1
    while j > start and not lines[j].strip():
        j -= 1
    if not lines[j].rstrip().endswith(",") and not lines[j].rstrip().endswith("["):
        lines[j] = lines[j].rstrip() + ","
    new = []
    for _, ch in models:
        new.extend(ch.split("\n"))
    lines[end:end] = new
    out = "\n".join(lines)
    compile(out, BUILD, "exec")  # 문법 검증 (실행은 안 함)
    return out


def insert_cards(html, cards):
    lines = html.split("\n")
    anchor = next((i for i, l in enumerate(lines)
                   if 'class="note-band"' in l and "모델명을 누르면" in l), None)
    if anchor is None:
        anchor = next((i for i, l in enumerate(lines) if 'class="note-band"' in l), None)
    if anchor is None:
        raise ValueError("index.html 에서 모델 목록 끝(note-band)을 찾지 못했습니다")
    close = next((i for i in range(anchor - 1, -1, -1) if lines[i].strip() == "</div>"), None)
    if close is None:
        raise ValueError("index.html 에서 모델 목록을 닫는 </div> 를 찾지 못했습니다")
    new = []
    for _, ch in cards:
        new.extend(ch.split("\n"))
        new.append("")
    lines[close:close] = new
    return "\n".join(lines)


def main():
    os.chdir(ROOT)
    for f in (BUILD, INDEX):
        if not os.path.exists(f):
            raise SystemExit(f"[오류] {f} 가 없습니다. 이 파일을 size-ruler 폴더(build_models.py 있는 곳)에 넣고 실행하세요.")
    batches = find_batches()
    if not batches:
        raise SystemExit("[안내] 처리할 batch 파일이 없습니다. batch 파일을 이 폴더에 넣고 다시 실행하세요.")

    src, nl_py = read(BUILD)
    html, nl_html = read(INDEX)
    added = []
    for bp in batches:
        mb, cb = load_batch(bp)
        all_models = split_models(mb)
        all_cards = split_cards(cb)
        models = [(s, ch) for s, ch in all_models if f'"slug": "{s}"' not in src]
        cards = [(s, ch) for s, ch in all_cards if f'href="/{s}/"' not in html]
        skipped = [s for s, _ in all_models if f'"slug": "{s}"' in src]
        if models:
            src = insert_models(src, models)
        if cards:
            html = insert_cards(html, cards)
        added += [s for s, _ in models]
        msg = f"[{os.path.basename(bp)}] 모델 {len(models)}개, 홈 카드 {len(cards)}개 추가"
        if skipped:
            msg += f" (이미 있어 건너뜀: {', '.join(skipped)})"
        print(msg)

    write(BUILD, src, nl_py)
    write(INDEX, html, nl_html)

    print("\n--- build_models.py 실행 ---")
    subprocess.run([sys.executable, "build_models.py"], check=True)
    if os.path.exists("build_sitemap.py"):
        print("\n--- build_sitemap.py 실행 ---")
        subprocess.run([sys.executable, "build_sitemap.py"], check=True)

    for bp in batches:
        os.remove(bp)

    print("\n=== 완료 ===")
    if added:
        print("추가된 모델:", ", ".join(added))
    print("다음: GitHub Desktop 에서 Commit -> Push origin 하세요.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code)
    except Exception as e:
        print("[오류]", type(e).__name__, e)
        print("파일이 바뀌었다면 GitHub Desktop 에서 'Discard changes' 로 되돌릴 수 있습니다. 이 화면을 캡처해서 보내주세요.")
    input("\n엔터를 누르면 닫힙니다.")
