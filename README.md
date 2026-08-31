# 사이즈 자 (size-ruler)

> 새 대화나 새 환경에서 작업을 이어간다면 **`CONTEXT.md`를 먼저 읽으세요.**
> 프로젝트 배경, 결정 이유, 남은 작업이 전부 정리돼 있습니다.

발 길이(mm) 기준 신발 사이즈 환산 + 모델별 실제 착용 사이즈 안내 사이트.

## 구조

```
/                        전체 환산표 + 인터랙티브 줄자 + 모델 목록

신발
/nike-air-force-1/       나이키 에어포스 1
/nike-dunk-low/          나이키 덩크 로우
/adidas-samba/           아디다스 삼바
/adidas-gazelle/         아디다스 가젤
/converse-chuck-70/      컨버스 척 70
/converse-chuck-taylor/  컨버스 척테일러 클래식
/newbalance-530/         뉴발란스 530
/newbalance-993/         뉴발란스 993
/vans-old-skool/         반스 올드스쿨

의류
/clothing-size-men/      남성 의류 사이즈
/clothing-size-women/    여성 의류 사이즈

공통
404.html                 없는 주소 안내
style.css                공용 스타일
favicon.svg              파비콘
_headers                 Cloudflare 캐시 설정
```

총 9페이지. 모델 페이지는 `build_models.py`가 생성하므로 직접 수정하지 말 것
(다음 실행 때 덮어써진다). 내용을 고치려면 생성기의 `MODELS`를 고친다.

## 생성기 세 개

| 파일 | 역할 |
|------|------|
| `build_models.py` | 신발 모델 페이지 (`MODELS` 리스트) |
| `build_clothing.py` | 의류 사이즈 페이지 (`PAGES` 리스트) |
| `build_sitemap.py` | 폴더를 스캔해 sitemap.xml + robots.txt 생성 |

## 페이지 추가하는 법

1. 해당 생성기의 리스트에 항목 추가
2. `python3 build_models.py` (또는 `build_clothing.py`) 실행
3. `python3 build_sitemap.py` 실행 — 새 폴더를 자동으로 찾아 넣는다
4. `index.html`과 `404.html`에 링크 추가

`build_sitemap.py`는 index.html의 canonical에서 현재 도메인을 읽으므로,
도메인을 바꾼 뒤에도 그대로 실행하면 된다.

템플릿이 한 곳에 있어서 페이지마다 구조가 어긋나지 않는다.
새 모델을 넣을 때는 **반드시 `sources`를 채울 것.** 근거 없는 항목은 넣지 않는다.

## 도메인

**sizeruler.com** (교체 완료). canonical·og·sitemap·robots·생성기 전부 반영됨.

도메인을 다시 바꿔야 한다면:

```bash
./setup-domain.sh 새도메인.com
python3 build_sitemap.py
```

## 로컬 확인

```bash
python3 -m http.server 8000
```

http://localhost:8000 접속. 하위 경로(`/adidas-samba/`)도 그대로 동작한다.

## 배포

`git push origin main` → Cloudflare Pages 자동 배포. 빌드 명령 없음, 루트 그대로 서빙.
