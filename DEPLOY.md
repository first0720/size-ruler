# 배포 가이드

처음부터 끝까지 한 시간이면 끝납니다. 순서대로 하세요.

---

## 0. 준비물

| 항목 | 비용 | 비고 |
|------|------|------|
| 도메인 | 연 1~2만원 | 가비아, 호스팅케이알, Cloudflare Registrar |
| GitHub 계정 | 무료 | |
| Cloudflare 계정 | 무료 | Pages는 개인 사용에 무료 |

**도메인 고르는 법.** 짧고 영문이고 `.com`/`.kr`이면 충분합니다. 키워드를 억지로 넣을 필요는 없습니다
(`shoe-size-conversion-korea.com` 같은 건 오히려 신뢰도가 떨어져 보입니다).
`sizeruler.kr`, `sizeja.com` 정도면 좋습니다.

---

## 1. 도메인 교체

**이걸 안 하면 구글이 색인을 거부합니다.** canonical 태그가 존재하지 않는 도메인을
가리키고 있기 때문입니다. 가장 흔하고 가장 치명적인 실수입니다.

```bash
cd size-ruler
./setup-domain.sh 내도메인.kr
```

`https://` 없이, `www` 없이, 슬래시 없이 도메인만 입력하세요.
스크립트가 canonical·og·sitemap·robots·생성기까지 22곳을 한 번에 바꾸고 결과를 출력합니다.
출력된 canonical 목록에 내 도메인이 제대로 찍혔는지 눈으로 확인하세요.

---

## 2. 로컬에서 마지막 확인

```bash
python3 -m http.server 8000
```

http://localhost:8000 에서 확인할 것:

- [ ] 줄자 눈금을 눌렀을 때 환산값이 바뀌는가
- [ ] 모델명을 눌렀을 때 상세 페이지로 이동하는가
- [ ] 상세 페이지에서 "전체 환산표"로 돌아와지는가
- [ ] 휴대폰 화면 크기로 줄여도 표가 가로 스크롤되는가
- [ ] 없는 주소(`/asdf/`)를 쳤을 때 404 페이지가 뜨는가

---

## 3. GitHub 저장소

```bash
git init
git add -A
git commit -m "사이즈 자 초기 배포"
git branch -M main
```

GitHub에서 새 저장소를 만든 뒤(README 추가 옵션은 체크 해제):

```bash
git remote add origin https://github.com/<사용자명>/size-ruler.git
git push -u origin main
```

**공개(Public)로 만들어도 됩니다.** 소스에 비밀이 없고, 나중에 애드센스 심사에서
사이트 소유를 증명할 때 오히려 편합니다.

---

## 4. Cloudflare Pages 연결

1. Cloudflare 대시보드 → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. GitHub 계정 연동 후 `size-ruler` 저장소 선택
3. 빌드 설정 — **여기가 중요합니다**

   | 항목 | 값 |
   |------|-----|
   | Framework preset | **None** |
   | Build command | **비워둘 것** |
   | Build output directory | `/` |

   빌드 도구가 없는 순수 정적 사이트입니다. 프레임워크를 잘못 고르면 빌드가 실패합니다.

4. **Save and Deploy** → 1분 내 `<프로젝트명>.pages.dev` 주소가 발급됩니다

이 시점에 임시 주소로 사이트가 이미 살아 있습니다. 열어서 확인하세요.

---

## 5. 도메인 연결

Pages 프로젝트 → **Custom domains** → **Set up a domain** → 내 도메인 입력.

**도메인을 Cloudflare에서 산 경우** 자동으로 연결됩니다.

**다른 곳(가비아 등)에서 산 경우** 두 가지 방법이 있습니다.

- **권장:** 도메인 등록업체에서 네임서버를 Cloudflare 것으로 변경 (Cloudflare가 안내하는 두 주소).
  반영에 최대 24시간 걸립니다.
- **간단:** 등록업체 DNS 관리에서 CNAME 레코드를 `<프로젝트명>.pages.dev`로 추가.

HTTPS 인증서는 Cloudflare가 자동 발급합니다. 따로 할 일이 없습니다.

**`www`도 같이 등록하세요.** `www.내도메인.kr`을 추가하고 리다이렉트되게 두면,
두 주소가 각각 색인되어 순위가 갈리는 문제를 막을 수 있습니다.

---

## 6. 구글 서치콘솔 등록

**이걸 해야 비로소 검색에 나옵니다.** 배포만 하고 여기서 멈추는 경우가 많은데,
등록을 안 하면 몇 달이 지나도 검색에 안 잡힐 수 있습니다.

1. https://search.google.com/search-console 접속
2. **속성 추가** → **도메인** 방식 선택 (URL 접두어보다 이쪽이 낫습니다)
3. 안내하는 TXT 레코드를 DNS에 추가 → 확인
4. 왼쪽 메뉴 **Sitemaps** → `sitemap.xml` 입력 → 제출
5. 상단 검색창에 내 도메인 입력 → **색인 생성 요청**

메인 페이지 하나만 요청해도 나머지는 내부 링크를 타고 발견됩니다.

---

## 7. 네이버 서치어드바이저 등록

국내 트래픽이 목표라면 필수입니다.

1. https://searchadvisor.naver.com 접속
2. 사이트 등록 → 소유확인(HTML 태그 또는 파일 업로드)
3. **요청 → 사이트맵 제출** → `sitemap.xml`
4. **요청 → 웹페이지 수집** → 메인 URL

네이버는 구글보다 색인이 느리고 보수적입니다. 조급해하지 마세요.

---

## 8. 이후 일정

| 시점 | 할 일 |
|------|-------|
| 배포 직후 | 서치콘솔 색인 요청 |
| 1~2주 | 서치콘솔 **페이지** 메뉴에서 9개가 다 색인됐는지 확인 |
| 2~4주 | 검색 결과에 노출 시작. **실적** 메뉴에서 유입 키워드 확인 |
| 색인 확인 후 | 애드센스 신청 |

**색인이 안 되고 있다면** 서치콘솔의 "페이지" → "색인이 생성되지 않음"에서 이유를 알려줍니다.
가장 흔한 원인이 canonical 오류인데, 1단계를 제대로 했다면 발생하지 않습니다.

---

## 9. 애드센스 (색인 확인 후)

1. https://adsense.google.com 가입 → 사이트 추가
2. 발급받은 스크립트를 각 페이지 `</head>` 앞에 삽입
   - `build_models.py` 템플릿에 넣고 재실행하면 모델 페이지 8개에 한 번에 들어갑니다
   - `index.html`, `404.html`은 직접 넣으세요
3. 심사 대기 (보통 1~4주)

**광고를 과하게 넣지 마세요.** 상단 1개, 표 아래 1개면 충분합니다.
콘텐츠보다 광고가 많으면 정책 위반으로 거절됩니다.

---

## 이후 업데이트하는 법

```bash
# 모델 추가/수정
vi build_models.py        # MODELS 리스트 편집
python3 build_models.py   # 페이지 + sitemap 재생성

git add -A
git commit -m "뉴발란스 574 추가"
git push origin main      # 1분 뒤 자동 반영
```

배포는 `git push`가 전부입니다. Cloudflare CLI 같은 걸 쓰지 마세요.
