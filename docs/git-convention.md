# Git 컨벤션

Cloudwave-Lab 저장소의 브랜치·커밋·PR 규칙. Livith-iOS의 `docs/rules/git.md`·`git-branch-strategy.md`를
이 실습 저장소 규모에 맞게 정리한 것이다.

## 브랜치

| 브랜치 | 역할 |
|--------|------|
| `main` | 공유 가능한 상태만. 실습 킷의 기준 소스. |
| 작업 브랜치 | `feat/`·`fix/`·`docs/`·`refactor/`·`setting/`·`chore/` + 설명(있으면 `#이슈번호`) |

- 작업 브랜치 예: `feat/#3-bottleneck-lab`, `fix/pool-waiters-metric`, `docs/git-convention`
- `main`에 직접 push 금지. 작업 브랜치에서 개발 → `main`으로 PR·머지.
- 머지는 **Squash 금지**(히스토리 보존). 머지 후 원격 작업 브랜치 삭제.

## 커밋 메시지

형식: `[Type] 변경 요약`

- 간결체, 50자 이내, 마침표 없음.
- 이슈가 있으면 `[Type] #nn - 변경 요약` 처럼 ` - ` 구분자 하나만 사용.
- 예:
  - `[Feat] 부하 실습용 티켓 예매 서비스 추가`
  - `[Fix] #12 - 커넥션 대기 지표 라벨 누락 수정`
  - `[Chore] Cloudwave-Lab 구조로 재편, .omc 추적 해제`

### Type

| Type | 용도 |
|------|------|
| `Feat` | 기능·실습 킷 추가 |
| `Fix` | 버그·오류 수정 |
| `Docs` | 문서(README, 컨벤션 등) |
| `Refactor` | 동작 변화 없는 구조 개선 |
| `Setting` | 설정·환경 구성(compose, CI 등) |
| `Chore` | 잡일(파일 이동, ignore 정리 등) |
| `Merge` | 머지 커밋 (`[Merge] 브랜치명`) |

## PR

- 제목: `[Type] 작업 설명` (이슈키는 제목에 안 넣음)
- 본문 끝에 연결 이슈: `Resolved: #nn`
- 본문에 무엇을·왜 바꿨는지 두괄식으로. 스크린샷/GIF는 있으면 첨부.

## 게이트

- **커밋·push는 사용자 명시 승인 후에만.** 자동으로 커밋하거나 푸시하지 않는다.
- `main`에 직접 push하지 않는다.
- 세션/툴 상태(`.omc/`), `.DS_Store` 등은 커밋하지 않는다(`.gitignore`로 차단).
