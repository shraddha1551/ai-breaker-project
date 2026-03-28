import json
import random
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def generate_random_divide_cases(n=5):
    cases = []
    for _ in range(n):
        a = random.choice([10, -5, "abc", None, 0])
        b = random.choice([0, 2, "xyz", None])
        cases.append({"a": a, "b": b})
    return cases


def generate_random_login_cases(n=5):
    cases = []
    for _ in range(n):
        payload = random.choice(
            [
                {},
                {"username": None},
                {"username": ""},
                {"username": "  "},
                {"user": "admin"},
                {"email": "a@b.com"},
                {"username": "admin"},
                {"username": 123},
                {"username": ["x"]},
                {"username": {"name": "x"}},
                {"password": "x"},
            ]
        )
        cases.append(payload)
    return cases


def generate_random_age_cases(n=5):
    cases = []
    for _ in range(n):
        age = random.choice(
            [
                None,
                -1,
                0,
                1,
                25,
                120,
                121,
                200,
                "old",
                3.14,
                True,
                [],
            ]
        )
        payload = random.choice(
            [
                {},
                {"age": age},
                {"years": age},
                {"age": age, "extra": 1},
            ]
        )
        cases.append(payload)
    return cases


results = []


def record_result(endpoint, input_data, status_code, outcome):
    results.append({
        "endpoint": endpoint,
        "input": input_data,
        "status_code": status_code,
        "outcome": outcome
    })


def test_divide():
    print("\nTesting /divide")
    for case in generate_random_divide_cases():
        try:
            r = requests.get(BASE_URL + "/divide", params=case)
            outcome = "failed" if r.status_code >= 400 else "passed"
            print(case, "->", r.status_code, "|", outcome)
            record_result("/divide", case, r.status_code, outcome)
        except Exception as e:
            print("Crash:", case, e)
            record_result("/divide", case, "CRASH", str(e))


def test_login():
    print("\nTesting /login")
    for case in generate_random_login_cases():
        try:
            r = requests.post(BASE_URL + "/login", json=case)
            outcome = "failed" if r.status_code >= 400 else "passed"
            print(case, "->", r.status_code, "|", outcome)
            record_result("/login", case, r.status_code, outcome)
        except Exception as e:
            print("Crash:", case, e)
            record_result("/login", case, "CRASH", str(e))


def test_age():
    print("\nTesting /age-check")
    for case in generate_random_age_cases():
        try:
            r = requests.post(BASE_URL + "/age-check", json=case)
            outcome = "failed" if r.status_code >= 400 else "passed"
            print(case, "->", r.status_code, "|", outcome)
            record_result("/age-check", case, r.status_code, outcome)
        except Exception as e:
            print("Crash:", case, e)
            record_result("/age-check", case, "CRASH", str(e))


def save_backend_logs(timestamp):
    try:
        response = requests.get(BASE_URL + "/logs")
        if response.status_code == 200:
            log_filename = f"outputs/backend_logs_{timestamp}.json"
            with open(log_filename, "w") as file:
                json.dump(response.json(), file, indent=4)
            print(f"Backend logs saved to {log_filename}")
    except Exception as e:
        print("Could not save backend logs:", e)


def show_summary():
    print("\n--- Test Summary ---")
    for item in results:
        print(item)

    import os
    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/results_{timestamp}.json"

    with open(filename, "w") as file:
        json.dump(results, file, indent=4)

    print(f"\nResults saved to {filename}")

    save_backend_logs(timestamp)


if __name__ == "__main__":
    try:
        r = requests.post(BASE_URL + "/clear-logs", timeout=5)
        if r.status_code == 200:
            print("Backend logs cleared before test run\n")
        else:
            print(f"clear-logs returned {r.status_code}, continuing anyway\n")
    except Exception as e:
        print("Could not clear backend logs (is the server running?):", e, "\n")

    test_divide()
    test_login()
    test_age()
    show_summary()
