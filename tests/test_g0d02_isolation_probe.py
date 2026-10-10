"""Pure-source contract checks for G0D-02 (never starts DDEV or Codex)."""
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/g0d02_isolation_probe.py"
spec = importlib.util.spec_from_file_location("g0d02_probe", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def sample(arm, **overrides):
    record = {
        "arm": arm,
        "workspace_id": "g0d02-" + arm,
        "source_sha": probe.SOURCE_SHA,
        "lock_sha256": probe.LOCK_SHA256,
        "php_version": "8.4.24",
        "node_version": "v24.10.0",
        "mariadb_version": "11.8.0-MariaDB",
        "composer_version": "Composer version 2.8.12",
    }
    record.update(overrides)
    return record


class ProbeContractTests(unittest.TestCase):
    def test_pins_permanent_frozen_baseline(self):
        self.assertEqual(
            probe.SOURCE_SHA, "39ef13c25b24c4a1b43a720ae53419f479996ed2"
        )
        self.assertEqual(probe.CODEX_VERSION, "0.160.0")
        self.assertEqual(probe.DDEV_VERSION, "1.25.4")
        self.assertEqual(len(probe.LOCK_SHA256), 64)

    def test_cli_version_match_is_exact(self):
        self.assertTrue(probe.version_matches("codex-cli 0.160.0", "0.160.0"))
        self.assertFalse(probe.version_matches("codex-cli 0.162.0", "0.160.0"))
        self.assertFalse(probe.version_matches("codex-cli 0.160.01", "0.160.0"))

    def test_candidate_report_never_claims_real_execution_or_g0_go(self):
        report = probe.manifest(
            codex="codex-cli 0.160.0", ddev="ddev version v1.25.4",
            arm_details=[sample("direct"), sample("pcp")],
        )
        self.assertFalse(report["eligible_for_controlled_benchmark"])
        self.assertFalse(report["project_baseline_activated"])
        self.assertFalse(report["pcp_runtime_connected"])
        self.assertFalse(report["provider_authenticated"])
        self.assertEqual(report["real_pcpxdirect_trials"], 0)
        self.assertIsNone(report["model_id"])
        self.assertIsNone(report["reasoning_effort"])
        self.assertEqual(report["independent_database_probe"], "PASS")
        self.assertEqual(len(report["workspace_identities"]), 2)
        self.assertEqual(len(set(report["workspace_identities"])), 2)
        self.assertEqual(len(report["toolchain_id"]), 30)

    def test_mismatched_toolchains_are_rejected(self):
        with self.assertRaises(AssertionError):
            probe.manifest(
                codex="codex-cli 0.160.0", ddev="ddev version v1.25.4",
                arm_details=[sample("direct"), sample("pcp", php_version="8.4.99")],
            )
        with self.assertRaises(AssertionError):
            probe.manifest(
                codex="codex-cli 0.160.0", ddev="ddev version v1.25.4",
                arm_details=[sample("direct"), sample("pcp", lock_sha256="b" * 64)],
            )

    def test_source_preflight_has_hard_stops_and_no_codex_inference(self):
        code = SCRIPT.read_text(encoding="utf-8")
        for marker in (
            "RUNNER_ENVIRONMENT", "GITHUB_REPOSITORY",
            'assert sha256_file(source / "composer.lock") == LOCK_SHA256',
            '"diff", "--name-only", "HEAD"',
            "git", "clone", "--no-local", "--no-hardlinks",
            "ddev", "list", "-j",
            "g0d02_only_direct", "g0d02_only_pcp",
            '"eligible_for_controlled_benchmark": False',
            '"model_id": None', '"reasoning_effort": None',
        ):
            self.assertIn(marker, code)
        for forbidden in ("codex exec", "codex login", "gh repo create",
                          "ddev restart", "docker system prune", "rm -rf"):
            self.assertNotIn(forbidden, code)


if __name__ == "__main__":
    unittest.main()
