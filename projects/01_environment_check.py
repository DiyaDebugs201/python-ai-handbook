"""Project 1 - Environment check.

Checks that your Python setup is ready for the handbook: the Python version,
a few standard-library modules, and whether named environment variables are SET
(it never prints their values, so secrets stay private).

Run:
    python 01_environment_check.py            # check this machine
    python 01_environment_check.py --demo     # deterministic demo with fake values
Standard library only.
"""
import importlib
import os
import platform
import sys

REQUIRED_MODULES = ["math", "json", "re", "random", "collections", "functools", "itertools"]
MINIMUM_PYTHON = (3, 8)


def check_python(version_info, minimum=MINIMUM_PYTHON):
    """Return (ok, message) for a version tuple such as sys.version_info[:3]."""
    version = tuple(version_info[:3])
    ok = version >= minimum
    needed = ".".join(map(str, minimum))
    return ok, f"Python {'.'.join(map(str, version))} ({'ok' if ok else 'too old, need ' + needed + '+'})"


def check_modules(names):
    """Return a dict of module name -> True/False depending on whether it imports."""
    result = {}
    for name in names:
        try:
            importlib.import_module(name)
            result[name] = True
        except ImportError:
            result[name] = False
    return result


def check_env_vars(names, environ):
    """Return name -> True/False for 'is the variable set and non-empty'. Values are never returned."""
    return {name: bool(environ.get(name)) for name in names}


def build_report(version_info, modules, env_names, environ):
    lines = []
    ok, message = check_python(version_info)
    lines.append(("PASS" if ok else "FAIL") + "  " + message)
    for name, present in check_modules(modules).items():
        lines.append(("PASS" if present else "FAIL") + f"  module {name}")
    for name, is_set in check_env_vars(env_names, environ).items():
        lines.append(("SET  " if is_set else "UNSET") + f"  environment variable {name} (value hidden)")
    failures = sum(1 for line in lines if line.startswith("FAIL"))
    return lines, failures


def run_demo():
    fake_environ = {"MY_SERVICE_API_KEY": "not-a-real-key", "MODEL_NAME": ""}
    lines, failures = build_report((3, 13, 0), REQUIRED_MODULES, ["MY_SERVICE_API_KEY", "MODEL_NAME", "TIMEOUT_SECONDS"], fake_environ)
    print("\n".join(lines))
    print("failures:", failures)
    old_ok, old_message = check_python((3, 6, 9))
    print(old_message)


def main(argv):
    if "--demo" in argv:
        run_demo()
        return 0
    print("Platform:", platform.system(), platform.machine())
    lines, failures = build_report(sys.version_info, REQUIRED_MODULES, ["MY_SERVICE_API_KEY", "MODEL_NAME", "TIMEOUT_SECONDS"], os.environ)
    print("\n".join(lines))
    print("Result:", "all required checks passed" if failures == 0 else f"{failures} check(s) failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
