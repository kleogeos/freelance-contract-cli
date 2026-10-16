import json
import subprocess
import sys
import tempfile
import os

PY = sys.executable
SCRIPT = "contract.py"


def run(*args):
    r = subprocess.run([PY, SCRIPT, *args], capture_output=True, text=True)
    return r


def write_json(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


def test_basic_contract_renders():
    path = write_json({"freelancer": "Jane Doe", "client": "Acme Corp"})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "Jane Doe" in r.stdout
    assert "Acme Corp" in r.stdout
    assert "not legal advice" in r.stdout


def test_missing_freelancer_fails_cleanly():
    path = write_json({"client": "Acme Corp"})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 1
    assert "freelancer" in r.stderr
    assert "Traceback" not in r.stderr


def test_missing_client_fails_cleanly():
    path = write_json({"freelancer": "Jane Doe"})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 1
    assert "client" in r.stderr


def test_ip_ownership_freelancer_variant():
    path = write_json({"freelancer": "Jane Doe", "client": "Acme Corp", "ip_ownership": "freelancer"})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "non-exclusive, perpetual license" in r.stdout


def test_ip_ownership_custom_text():
    path = write_json({"freelancer": "Jane Doe", "client": "Acme Corp", "ip_ownership": "Shared 50/50 ownership."})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "Shared 50/50 ownership." in r.stdout


def test_empty_scope_shows_placeholder():
    path = write_json({"freelancer": "Jane Doe", "client": "Acme Corp", "scope": []})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "scope to be filled in" in r.stdout


def test_html_escaping_in_names():
    path = write_json({"freelancer": "<script>alert(1)</script>", "client": "Acme Corp"})
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "<script>alert(1)</script>" not in r.stdout
    assert "&lt;script&gt;" in r.stdout


def test_output_to_file():
    path = write_json({"freelancer": "Jane Doe", "client": "Acme Corp"})
    out_path = path + ".html"
    r = run(path, "-o", out_path)
    assert r.returncode == 0, r.stderr
    assert os.path.exists(out_path)
    content = open(out_path).read()
    assert "Jane Doe" in content
    os.unlink(path)
    os.unlink(out_path)


def test_example_json_from_repo():
    r = run("example.json")
    assert r.returncode == 0, r.stderr
    assert "Acme Corp" in r.stdout
    assert "the State of California" in r.stdout


if __name__ == "__main__":
    failures = 0
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
    if failures:
        print(f"{failures} failure(s)")
        sys.exit(1)
    print(f"All {len(tests)} tests passed")
