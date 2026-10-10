#!/usr/bin/env python3
"""G0D-02 proof of independent *disposable* DDEV toolchains, not PCP execution.

Only runs on an ephemeral GitHub-hosted runner. No Codex inference, user tokens,
PCP Runtime connection, local WSL projects, or G0D-T01 edits are permitted.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

SOURCE_SHA = "39ef13c25b24c4a1b43a720ae53419f479996ed2"
LOCK_SHA256 = "3a3d086be59571b43f05301ab099dc4d710a2ca1da0b25af60341d527f531f2b"
CODEX_VERSION = "0.160.0"
DDEV_VERSION = "1.25.4"
PROJECT_NAMES = ("pcp-g0d02-direct", "pcp-g0d02-pcp")
REPO_NAME = "sonvhse06072/pcp-g0-drupal-fixture"


def run(*args: str, cwd: Path | None = None, timeout: int = 360) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, capture_output=True, text=True,
        check=False, timeout=timeout,
    )
    if result.returncode:
        # Never print the complete environment, credentials or upstream headers.
        reason = (result.stderr or result.stdout).strip().splitlines()[-5:]
        raise RuntimeError(f"probe command failed: {args[0]} (exit {result.returncode}): "
                           + " / ".join(reason)[:650])
    return result.stdout.strip()


def version_matches(observed: str, required: str) -> bool:
    return bool(re.search(r"(?<![0-9])" + re.escape(required) + r"(?![0-9])", observed))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(*, codex: str, ddev: str, arm_details: list[dict]) -> dict:
    """Return a candidate-only report; never self-certify active PCP or inference."""
    assert len(arm_details) == 2
    assert arm_details[0]["arm"] == "direct" and arm_details[1]["arm"] == "pcp"
    assert arm_details[0]["source_sha"] == arm_details[1]["source_sha"] == SOURCE_SHA
    assert arm_details[0]["lock_sha256"] == arm_details[1]["lock_sha256"] == LOCK_SHA256
    assert {x["workspace_id"] for x in arm_details} == {"g0d02-direct", "g0d02-pcp"}
    common = ("php_version", "node_version", "mariadb_version", "composer_version")
    assert all(arm_details[0][k] == arm_details[1][k] for k in common)
    platform = {
        "source_sha": SOURCE_SHA, "composer_lock_sha256": LOCK_SHA256,
        "codex_cli_version": codex, "ddev_version": ddev,
        "os": "github-hosted-ubuntu-24.04",
        **{k: arm_details[0][k] for k in common},
        "browser": "not_applicable_drupal",
    }
    toolchain_id = "g0d02-" + hashlib.sha256(
        json.dumps(platform, sort_keys=True).encode("utf-8")
    ).hexdigest()[:24]
    return {
        "schema": "g0d02-toolchain-preflight-v1",
        "status": "disposable_toolchain_isolation_only",
        "source_sha": SOURCE_SHA,
        "baseline_branch_heads_equal": True,
        "codex_cli_version": codex,
        "toolchain_id": toolchain_id,
        "workspace_identities": [x["workspace_id"] for x in arm_details],
        "ddev_project_names": list(PROJECT_NAMES),
        "independent_database_probe": "PASS",
        "arm_toolchains": arm_details,
        "model_id": None,
        "reasoning_effort": None,
        "provider_authenticated": False,
        "pcp_runtime_connected": False,
        "project_baseline_activated": False,
        "real_pcpxdirect_trials": 0,
        "eligible_for_controlled_benchmark": False,
        "blocked_by": [
            "no_persistently_isolated_PCP_Executor",
            "PCP_ProjectBaseline_PARKED",
            "model_and_effort_unverified",
            "no_authorized_provider_session_or_live_lease_evidence",
        ],
    }


def ensure_github_hosted(source: Path, temp: Path) -> None:
    assert os.environ.get("RUNNER_ENVIRONMENT") == "github-hosted"
    assert os.environ.get("RUNNER_OS") == "Linux"
    assert os.environ.get("GITHUB_REPOSITORY") == REPO_NAME
    assert os.environ.get("GITHUB_EVENT_NAME") == "pull_request"
    assert source.is_dir() and (source / ".git").exists()
    assert temp.is_dir() and not temp.is_symlink()
    assert temp != source and not source.is_relative_to(temp)
    assert "OPENAI_API_KEY" not in os.environ
    assert "CODEX_API_KEY" not in os.environ
    assert "GH_TOKEN" not in os.environ
    assert "GITHUB_TOKEN" not in os.environ


def verify_ddev_registry_empty() -> None:
    output = run("ddev", "list", "-j", timeout=30)
    records = [json.loads(row) for row in output.splitlines() if row.strip()]
    raw = [x["raw"] for x in records if isinstance(x, dict) and isinstance(x.get("raw"), list)]
    assert len(raw) == 1 and raw[0] == [], "DDEV registry must be empty before probe"


def main() -> None:
    source = Path(os.environ["GITHUB_WORKSPACE"]).resolve(strict=True)
    temp = Path(os.environ["RUNNER_TEMP"]).resolve(strict=True)
    ensure_github_hosted(source, temp)
    assert run("git", "-C", str(source), "status", "--porcelain=v1") == ""
    for name in ("benchmark/direct", "benchmark/pcp"):
        sha = run("git", "-C", str(source), "rev-parse", "refs/remotes/origin/" + name)
        assert sha == SOURCE_SHA, f"source ref mismatch: {name}"
    assert sha256_file(source / "composer.lock") == LOCK_SHA256

    binary = temp / "g0d02-codex" / "node_modules/.bin/codex"
    assert binary.is_file()
    codex = run(str(binary), "--version", timeout=15)
    assert version_matches(codex, CODEX_VERSION), "isolated Codex CLI version mismatch"
    ddev = run("ddev", "--version", timeout=15)
    assert version_matches(ddev, DDEV_VERSION), "isolated DDEV version mismatch"
    ensure_github_hosted(source, temp)
    verify_ddev_registry_empty()

    details = []
    for arm, name in zip(("direct", "pcp"), PROJECT_NAMES, strict=True):
        dst = temp / ("g0d02-" + arm)
        assert not dst.exists() and not dst.is_symlink()
        run("git", "clone", "--no-local", "--no-hardlinks", str(source), str(dst))
        assert (dst / ".git").is_dir(), "each arm needs its own Git object store"
        run("git", "-C", str(dst), "checkout", "--detach", SOURCE_SHA)
        assert run("git", "-C", str(dst), "rev-parse", "HEAD") == SOURCE_SHA
        assert run("git", "-C", str(dst), "status", "--porcelain=v1") == ""
        assert sha256_file(dst / "composer.lock") == LOCK_SHA256

        # These DDEV actions are permissible ONLY on this disposable runner and
        # only after confirming its registry contains no prior projects.
        run("ddev", "config", "--project-name=" + name, "--project-type=drupal11",
            "--docroot=web", "--php-version=8.4", "--nodejs-version=24",
            cwd=dst, timeout=60)
        run("ddev", "start", "-y", cwd=dst, timeout=300)
        run("ddev", "composer", "install", "--no-interaction",
            "--prefer-dist", "--no-progress", cwd=dst, timeout=300)
        php = run("ddev", "exec", "php", "-r", "echo PHP_VERSION;", cwd=dst)
        node = run("ddev", "exec", "node", "--version", cwd=dst)
        composer = run("ddev", "exec", "composer", "--version", cwd=dst).splitlines()[0]
        db = run("ddev", "mysql", "-N", "-e", "SELECT VERSION();", cwd=dst)
        assert php.startswith("8.4."), "PHP 8.4 not active in one arm"
        assert node.startswith("v24."), "Node 24 not active in one arm"
        assert sha256_file(dst / "composer.lock") == LOCK_SHA256
        # The only tracked mutation may be the DDEV project-name override.
        modified = run("git", "-C", str(dst), "diff", "--name-only")
        assert modified in ("", ".ddev/config.yaml"), "unexpected tracked source change"
        details.append({
            "arm": arm, "workspace_id": "g0d02-" + arm,
            "source_sha": SOURCE_SHA, "lock_sha256": LOCK_SHA256,
            "php_version": php, "node_version": node,
            "mariadb_version": db, "composer_version": composer,
        })
        print("G0D-02 " + arm + ": DDEV/Composer/Node/PHP reachable in isolated Git clone")

    direct_dir = temp / "g0d02-direct"
    pcp_dir = temp / "g0d02-pcp"
    # Prove databases do not share data. Only fresh disposable DBs are used.
    run("ddev", "mysql", "-e",
        "CREATE TABLE g0d02_only_direct (marker INT NOT NULL);",
        cwd=direct_dir)
    pc_count = run("ddev", "mysql", "-N", "-e",
                   "SELECT COUNT(*) FROM information_schema.tables "
                   "WHERE table_schema=DATABASE() AND table_name='g0d02_only_direct';",
                   cwd=pcp_dir)
    assert pc_count.strip() == "0", "PCP arm sees direct DB table"
    run("ddev", "mysql", "-e",
        "CREATE TABLE g0d02_only_pcp (marker INT NOT NULL);",
        cwd=pcp_dir)
    dir_count = run("ddev", "mysql", "-N", "-e",
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema=DATABASE() AND table_name='g0d02_only_pcp';",
                    cwd=direct_dir)
    assert dir_count.strip() == "0", "Direct arm sees PCP DB table"

    report = manifest(codex=codex, ddev=ddev, arm_details=details)
    folder = temp / "g0d02-evidence"
    assert not folder.exists()
    folder.mkdir(mode=0o700)
    (folder / "preflight.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G0D-02 isolated toolchain/source/DB preflight PASS")
    print("G0D-02 REAL PCP job readiness: FALSE; model/effort/auth/Runtime not verified")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, OSError, ValueError, RuntimeError,
            subprocess.TimeoutExpired) as exc:
        print(f"G0D-02 FAIL CLOSED: {type(exc).__name__}: {str(exc)[:650]}", file=sys.stderr)
        sys.exit(2)
