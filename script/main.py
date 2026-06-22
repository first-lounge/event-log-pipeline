from generate_events import generate
from load_events import insert_raw
from transform_events import insert_events
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="이벤트 생성기 스크립트")
    parser.add_argument("-s", "--size", type=int, default=1000, help="생성할 데이터 개수")
    args = parser.parse_args()

    print(f"==== 이벤트 {args.size}건 생성 중... ====")
    data = generate(args.size)
    print(f"  생성 완료: {len(data)}건\n")

    print("==== [1/2] raw_events 적재(Load) 시작 ====")
    result = insert_raw(data)
    if result is None:
        print("  Load 실패", file=sys.stderr)
        sys.exit(1)
    print(f"  Load 완료: raw_events {result}건\n")

    print("==== [2/2] 정규화 변환(Transform) 시작 ====")
    cnts = insert_events()
    if cnts is None:
        print("  Transform 실패", file=sys.stderr)
        sys.exit(1)
    print(f"  Transform 완료: events {cnts['events']} / "
          f"click {cnts['click']} / purchase {cnts['purchase']} / error {cnts['error']}\n")

    print("==== 모든 작업이 완료되었습니다 ====")


if __name__ == "__main__":
    main()