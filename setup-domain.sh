#!/usr/bin/env bash
# 배포 전 도메인 교체 스크립트
#
# 사용법:  ./setup-domain.sh sizeruler.kr
#
# canonical, og:url, sitemap.xml, robots.txt에 박혀 있는 example.com을
# 실제 도메인으로 한 번에 바꾼다. 손으로 하면 반드시 빠지는 곳이 생긴다.

set -euo pipefail

if [ $# -ne 1 ]; then
  echo "사용법: $0 <도메인>"
  echo "예시:   $0 sizeruler.kr"
  echo "        (https:// 없이, www 없이 입력)"
  exit 1
fi

DOMAIN="$1"

# grep은 매칭이 0건이면 exit 1을 낸다. pipefail과 겹치면 스크립트가 조용히 종료되므로
# || true로 감싼다. 교체 성공 시 정확히 이 경로를 탄다.
count_remaining() {
  grep -ro 'example\.com' \
    --include='*.html' --include='*.xml' --include='*.txt' --include='*.py' . \
    2>/dev/null | wc -l | tr -d ' ' || true
}

# 입력값 검증 — 스킴이나 슬래시가 붙어 있으면 canonical이 깨진다
if [[ "$DOMAIN" == http* ]] || [[ "$DOMAIN" == */* ]]; then
  echo "오류: 도메인만 입력하세요. https:// 나 경로는 빼야 합니다."
  echo "  잘못: https://sizeruler.kr/"
  echo "  올바름: sizeruler.kr"
  exit 1
fi

if [[ ! "$DOMAIN" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)+$ ]]; then
  echo "오류: 도메인 형식이 아닙니다: $DOMAIN"
  exit 1
fi

BEFORE=$(count_remaining)

if [ "$BEFORE" -eq 0 ]; then
  echo "example.com이 없습니다. 이미 교체됐거나 다른 도메인이 들어가 있습니다."
  grep -rho 'https://[a-zA-Z0-9.-]*' --include='*.xml' . | sort -u | head
  exit 0
fi

echo "example.com $BEFORE 곳을 $DOMAIN 으로 교체합니다."

# 생성기(build_models.py)도 같이 바꿔야 다음 실행 때 되돌아가지 않는다
grep -rl 'example\.com' \
  --include='*.html' --include='*.xml' --include='*.txt' --include='*.py' . \
  | xargs sed -i.bak "s|example\.com|${DOMAIN}|g"

find . -name '*.bak' -delete

AFTER=$(count_remaining)

if [ "$AFTER" -ne 0 ]; then
  echo "실패: example.com이 $AFTER 곳 남아 있습니다."
  grep -rn 'example\.com' --include='*.html' --include='*.xml' --include='*.txt' --include='*.py' .
  exit 1
fi

echo "완료. 교체 결과 확인:"
grep -rh 'rel="canonical"' --include='*.html' . | sed 's/^[[:space:]]*/  /'
echo
echo "  sitemap.xml:"
grep '<loc>' sitemap.xml | sed 's/^/  /'
echo
echo "다음: git add -A && git commit -m \"도메인 설정: ${DOMAIN}\" && git push origin main"
