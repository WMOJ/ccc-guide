import os
import subprocess

test_dir = "tests"
names = sorted(name[:-4] for name in os.listdir(test_dir) if name.endswith(".txt"))

for base in names:
    with open(f"{test_dir}/{base}.txt") as f:
        official_input = f.read()
    with open(f"{test_dir}/{base}.out") as f:
        official_output = f.read()

    result = subprocess.run(
        ["pypy3", "sol.py"],
        input=official_input,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout == official_output:
        print(base, "matches")
    else:
        print(base, "does NOT match")
