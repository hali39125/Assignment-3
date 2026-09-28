
import csv
import random
import statistics
import time

from assignment3 import (
    deterministic_quicksort,
    randomized_quicksort,
)


def make_inputs(n):
    rng = random.Random(2026 + n)

    return {
        "random": [rng.randrange(0, n * 10) for _ in range(n)],
        "sorted": list(range(n)),
        "reverse": list(range(n - 1, -1, -1)),
        "repeated": [7] * n,
    }


def measure(func, values, randomized=False, repetitions=3):
    times = []

    for trial in range(repetitions):
        start = time.perf_counter()

        if randomized:
            result = func(values, seed=trial + 100)
        else:
            result = func(values)

        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

        assert result == sorted(values)

    return (
        statistics.mean(times),
        min(times),
        max(times),
    )


def main():
    sizes = [100, 500, 1000]
    algorithms = [
        ("Deterministic", deterministic_quicksort, False),
        ("Randomized", randomized_quicksort, True),
    ]

    results = []

    for n in sizes:
        for distribution, values in make_inputs(n).items():
            for name, func, randomized in algorithms:
                mean, minimum, maximum = measure(
                    func, values, randomized
                )

                results.append({
                    "n": n,
                    "distribution": distribution,
                    "algorithm": name,
                    "repetitions": 3,
                    "mean_ms": round(mean, 4),
                    "min_ms": round(minimum, 4),
                    "max_ms": round(maximum, 4),
                })

                print(
                    f"{n:5} | {distribution:9} | {name:13} | "
                    f"mean={mean:.4f} ms"
                )

    with open("benchmark_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\nResults saved to benchmark_results.csv")


if __name__ == "__main__":
    main()