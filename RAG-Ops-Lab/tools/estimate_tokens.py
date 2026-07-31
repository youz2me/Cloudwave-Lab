#!/usr/bin/env python3
"""임베딩 비용 추정기.

corpus/ 아래 파일들을 청킹했을 때 임베딩에 들어갈 토큰 수와 비용을 어림한다.
정밀한 토크나이저가 아니라 어림값이다(한국어 위주 텍스트 기준 문자수/2로 추정).
비교 목적으로는 충분하다 — 절대값이 아니라 **설계 A vs 설계 B의 차이**를 보는 도구다.

사용 예:
    python3 tools/estimate_tokens.py
    python3 tools/estimate_tokens.py --chunk-size 200 --overlap 30
    python3 tools/estimate_tokens.py --dir my-cleaned-corpus --price 0.02
"""

import argparse
import math
import sys
from pathlib import Path

CHARS_PER_TOKEN = 2.0  # 한국어 위주 텍스트 어림값


def est_tokens(text: str) -> int:
    return max(1, int(len(text) / CHARS_PER_TOKEN))


def chunk_count(tokens: int, chunk_size: int, overlap: int) -> int:
    if tokens <= chunk_size:
        return 1
    step = chunk_size - overlap
    return 1 + math.ceil((tokens - chunk_size) / step)


def main() -> None:
    p = argparse.ArgumentParser(description="임베딩 토큰/비용 추정")
    p.add_argument("--dir", default="corpus", help="대상 디렉터리 (기본: corpus)")
    p.add_argument("--chunk-size", type=int, default=400, help="청크 크기(토큰)")
    p.add_argument("--overlap", type=int, default=50, help="청크 간 오버랩(토큰)")
    p.add_argument("--price", type=float, default=0.02, help="임베딩 단가 (USD / 1M tokens)")
    args = p.parse_args()

    if args.overlap >= args.chunk_size:
        sys.exit("오버랩이 청크 크기보다 크거나 같으면 청킹이 끝나지 않는다.")

    root = Path(args.dir)
    files = sorted(f for f in root.rglob("*") if f.is_file())
    if not files:
        sys.exit(f"{root} 아래에 파일이 없다.")

    print(f"{'파일':<55} {'문자수':>8} {'토큰(추정)':>10} {'청크수':>6} {'임베딩토큰':>10}")
    print("-" * 95)

    total_embed = 0
    total_chunks = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        tokens = est_tokens(text)
        chunks = chunk_count(tokens, args.chunk_size, args.overlap)
        # 오버랩만큼 같은 내용이 중복 임베딩된다 — 이게 오버랩의 비용이다.
        embed_tokens = tokens + (chunks - 1) * args.overlap
        total_embed += embed_tokens
        total_chunks += chunks
        print(f"{str(f.relative_to(root)):<55} {len(text):>8} {tokens:>10} {chunks:>6} {embed_tokens:>10}")

    cost = total_embed / 1_000_000 * args.price
    print("-" * 95)
    print(f"합계: 청크 {total_chunks}개, 임베딩 토큰 약 {total_embed:,}개")
    print(f"1회 전체 색인 비용 추정: ${cost:.4f} (단가 ${args.price}/1M tokens 기준)")
    print()
    print("생각해볼 것: 이 비용은 '1회' 색인 비용이다. 문서가 갱신될 때마다,")
    print("청킹 전략을 바꿔 재색인할 때마다 다시 든다. 그리고 검색 품질이 나쁘면")
    print("LLM 호출 쪽에서 더 큰 비용(긴 컨텍스트, 재질의)이 샌다.")


if __name__ == "__main__":
    main()
