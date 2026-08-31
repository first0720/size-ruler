#!/usr/bin/env python3
"""og:image 생성기 (1200x630).

카톡·슬랙·트위터에 링크를 붙였을 때 보이는 미리보기 이미지.
사이트의 줄자 모티프를 그대로 쓴다.

실행: python3 build_og.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (242, 242, 238)
INK = (21, 21, 15)
TAPE = (255, 206, 0)

CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 상단 줄자 띠
    band_h = 150
    d.rectangle([0, 0, W, band_h], fill=TAPE)
    d.line([(0, band_h), (W, band_h)], fill=INK, width=5)

    # 눈금 — 실제 신발 사이즈 범위(230~300mm)만 표기한다.
    # 존재하지 않는 숫자가 찍히면 사이즈 사이트로서 신뢰를 잃는다.
    tick_f = font(MONO, 22)
    lo, hi, step = 230, 300, 5          # 5mm 단위
    n = (hi - lo) // step               # 눈금 간격 수
    left, right = 40, W - 40
    gap = (right - left) / n
    for i in range(n + 1):
        mm = lo + i * step
        x = left + gap * i
        major = (mm % 10 == 0)
        h = 58 if major else 34
        d.line([(x, band_h - h), (x, band_h)], fill=INK, width=4 if major else 2)
        if major:
            label = str(mm)
            tw = d.textlength(label, font=tick_f)
            # 오른쪽 끝 라벨은 캔버스를 넘어가므로 눈금 왼쪽에 붙인다
            tx = x - tw - 7 if x + tw + 7 > right else x + 7
            d.text((tx, band_h - h - 30), label, font=tick_f, fill=INK)

    # 제목
    title_f = font(CJK, 76)
    sub_f = font(CJK, 30)
    mono_f = font(MONO, 26)

    d.text((60, 230), "신발 사이즈 환산표", font=title_f, fill=INK)
    d.text((60, 340), "mm · US · UK · EU · JP", font=mono_f, fill=(95, 95, 88))
    d.text((60, 400), "브랜드가 아니라 모델별로.", font=sub_f, fill=INK)
    d.text((60, 444), "발볼까지 반영한 실제 착용 사이즈.", font=sub_f, fill=INK)

    # 하단 라인 + 워드마크
    d.line([(60, 540), (W - 60, 540)], fill=INK, width=3)
    d.text((60, 560), "사이즈 자", font=font(CJK, 34), fill=INK)

    img.save("og-image.png", "PNG", optimize=True)
    print("og-image.png 생성 (1200x630)")


if __name__ == "__main__":
    main()
