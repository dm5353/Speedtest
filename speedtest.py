import argparse
import sys
import time
import requests


def measure_speed(url: str, iterations: int = 10) -> None:
    total_bytes = 0
    total_time = 0.0

    with requests.Session() as session:
        session.headers.update({"User-Agent": "SpeedTest-CLI/1.0"})

        for i in range(1, iterations + 1):
            start_time = time.perf_counter()
            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()
                content = response.content
            except requests.RequestException as e:
                print(f"Ошибка при выполнении запроса #{i}: {e}", file=sys.stderr)
                sys.exit(1)

            total_time += time.perf_counter() - start_time
            total_bytes += len(content)

    avg_time = total_time / iterations
    avg_bytes = total_bytes / iterations
    speed_mbps = (avg_bytes * 8) / (avg_time * 1_000_000)

    print(f"\nСкорость скачивания: {speed_mbps:.2f} Мбит/с\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Консольный скрипт для замера скорости скачивания."
    )
    parser.add_argument(
        "url", help="URL файла для скачивания (например, тяжёлая картинка)"
    )
    args = parser.parse_args()

    measure_speed(args.url)


if __name__ == "__main__":
    main()
