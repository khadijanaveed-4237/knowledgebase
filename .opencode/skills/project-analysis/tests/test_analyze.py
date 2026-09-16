#!/usr/bin/env python3
"""Tests for the project-analysis analyzer.

Run with:
    python3 -m unittest discover -s tests -v
or:
    python3 tests/test_analyze.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(TEST_DIR, "fixtures")
SCRIPTS = os.path.dirname(TEST_DIR)

sys.path.insert(0, os.path.join(SCRIPTS, "scripts"))

import analyze  # noqa: E402


def fixture(name):
    return os.path.join(FIXTURES, name)


def snapshot_dict(root):
    """Capture file contents and sizes to verify the target stays untouched."""
    snap = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            with open(full, "rb") as fh:
                snap[rel] = (os.path.getsize(full), fh.read())
    return snap


class TestStructureDetection(unittest.TestCase):
    def test_simple_python_structure(self):
        st = analyze.collect_structure(fixture("simple-python"))
        self.assertEqual(st["plausibility"], "fact")
        self.assertEqual(st["confidence"], "high")
        self.assertTrue(st["file_count"] >= 2)
        self.assertIn("app.py", st["files"])
        self.assertIn("pyproject.toml", st["files"])

    def test_no_manifest_structure(self):
        st = analyze.collect_structure(fixture("no-manifest"))
        self.assertEqual(st["file_count"], 1)
        self.assertIn("helper.py", st["files"])

    def test_mixed_language_structure(self):
        st = analyze.collect_structure(fixture("mixed-language"))
        self.assertIn("main.py", st["files"])
        self.assertIn("script.js", st["files"])
        self.assertIn("package.json", st["files"])
        self.assertIn("pyproject.toml", st["files"])


class TestProjectTypeDetection(unittest.TestCase):
    def test_simple_python_detected(self):
        pt = analyze.detect_project_type(fixture("simple-python"))
        self.assertEqual(pt["verdict"], "detected")
        self.assertIn("Python", pt["types"])
        self.assertIn("pyproject.toml", pt["evidence"])
        self.assertEqual(pt["primary"], "Python")
        self.assertEqual(pt["primary_confidence"], "high")
        self.assertFalse(pt["multiple_ecosystems"])

    def test_simple_nodejs_detected(self):
        pt = analyze.detect_project_type(fixture("simple-nodejs"))
        self.assertEqual(pt["verdict"], "detected")
        self.assertIn("Node.js / JavaScript / TypeScript", pt["types"])
        self.assertIn("package.json", pt["evidence"])

    def test_no_manifest_insufficient(self):
        pt = analyze.detect_project_type(fixture("no-manifest"))
        self.assertEqual(pt["verdict"], "INSUFFICIENT EVIDENCE")
        self.assertEqual(pt["plausibility"], "insufficient")
        self.assertEqual(pt["evidence"], [])
        self.assertIsNone(pt["primary"])

    def test_multiple_ecosystems_detected(self):
        pt = analyze.detect_project_type(fixture("mixed-language"))
        self.assertEqual(pt["verdict"], "detected")
        self.assertTrue(pt["multiple_ecosystems"])
        self.assertIn("primary_confidence", pt)
        self.assertIn("ecosystems", pt)
        self.assertGreaterEqual(len(pt["ecosystems"]), 2)


class TestArchitectureDetection(unittest.TestCase):
    def test_simple_python_architecture(self):
        arch = analyze.understand_architecture(fixture("simple-python"))
        self.assertIn("Python", arch["language_breakdown"])
        self.assertGreaterEqual(arch["source_file_count"], 1)
        self.assertIn("app.py", arch["entry_point_candidates"])
        self.assertEqual(arch["plausibility"], "fact")

    def test_large_file_architecture_has_functions(self):
        arch = analyze.understand_architecture(fixture("large-file-project"))
        self.assertIn("Python", arch["language_breakdown"])
        # big_module.py lives at root, so source grouping "." should be >= 1
        self.assertGreaterEqual(arch["source_grouping"].get(".", 0), 1)

    def test_likely_directories(self):
        arch = analyze.understand_architecture(fixture("mixed-language"))
        self.assertIn("likely_directories", arch)

    def test_config_and_manifest_files(self):
        arch = analyze.understand_architecture(fixture("simple-python"))
        self.assertIn("pyproject.toml", arch["manifest_files"])
        self.assertIn("config_files", arch)


class TestProblemDetection(unittest.TestCase):
    def test_readme_present_no_problem(self):
        problems = analyze.find_problems(fixture("with-readme"))
        titles = [p["title"].lower() for p in problems]
        self.assertFalse(any("readme" in t for t in titles))

    def test_readme_missing_problem(self):
        problems = analyze.find_problems(fixture("without-readme"))
        titles = [p["title"].lower() for p in problems]
        self.assertTrue(any("readme" in t for t in titles))

    def test_with_tests_no_test_problem(self):
        problems = analyze.find_problems(fixture("with-tests"))
        titles = [p["title"].lower() for p in problems]
        self.assertFalse(any("test" in t for t in titles))

    def test_without_tests_test_problem(self):
        problems = analyze.find_problems(fixture("without-tests"))
        titles = [p["title"].lower() for p in problems]
        self.assertTrue(any("test files" in t for t in titles))

    def test_todo_fixme_hack_detected(self):
        problems = analyze.find_problems(fixture("with-todo"))
        titles = [p["title"].lower() for p in problems]
        self.assertTrue(any("todo" in t for t in titles))
        self.assertTrue(any("fixme" in t for t in titles))
        self.assertTrue(any("hack" in t for t in titles))

    def test_silent_exception_detected(self):
        problems = analyze.find_problems(fixture("with-todo"))
        titles = [p["title"].lower() for p in problems]
        self.assertTrue(any("silent exception" in t for t in titles))

    def test_missing_files_have_evidence(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        self.assertIsNotNone(readme_problem)
        self.assertTrue(all("type" in e and "description" in e
                            for e in readme_problem["evidence"]))

    def test_missing_files_have_category(self):
        problems = analyze.find_problems(fixture("without-readme"))
        for p in problems:
            self.assertIn("category", p)


class TestLargeFileDetection(unittest.TestCase):
    def test_large_file_reported_with_size_and_threshold(self):
        problems = analyze.find_problems(fixture("large-file-project"))
        large = [p for p in problems if p["category"] == "large_file"]
        self.assertTrue(large, "Expected large-file finding")
        p = large[0]
        ctx = p["context"]
        self.assertGreater(ctx["size_bytes"], analyze.LARGE_FILE_THRESHOLD)
        self.assertEqual(ctx["threshold"], analyze.LARGE_FILE_THRESHOLD)
        # Additional evidence should be gathered for source files.
        self.assertIn("function_count", ctx)
        self.assertIn("class_count", ctx)
        self.assertGreater(ctx["function_count"], 0)
        self.assertIn("likely_responsibilities", ctx)

    def test_large_file_with_multiple_responsibilities_medium_confidence(self):
        problems = analyze.find_problems(fixture("large-file-project"))
        large = [p for p in problems if p["category"] == "large_file"]
        p = large[0]
        self.assertGreater(len(p["context"]["likely_responsibilities"]), 1)
        self.assertEqual(p["confidence"], "medium")

    def test_large_file_has_typed_evidence(self):
        problems = analyze.find_problems(fixture("large-file-project"))
        large = [p for p in problems if p["category"] == "large_file"]
        p = large[0]
        types = {e["type"] for e in p["evidence"]}
        self.assertIn("file_size", types)


class TestSecretDetection(unittest.TestCase):
    def test_placeholder_values_not_flagged(self):
        problems = analyze.find_problems(fixture("placeholder-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        self.assertEqual(secrets, [], "Placeholders should not be flagged as secrets")

    def test_real_secrets_detected(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        self.assertTrue(secrets, "Real secrets should be detected")

    def test_secret_values_not_exposed(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        report_text = json.dumps(problems)
        # Secret values must not appear in the report output.
        self.assertNotIn("sk-abc123def456ghi789jkl012mno345pqr678stu901", report_text)
        self.assertNotIn("xK9mB2vP7qL4nR8wT3yF6jH1dS5gZ0cA", report_text)

    def test_secret_metadata_present(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        ctx = secrets[0]["context"]
        self.assertIn("matched_key", ctx)
        self.assertIn("value_length", ctx)
        self.assertIn("strength", ctx)
        self.assertIn("category", ctx)
        self.assertIn("line", ctx)

    def test_secret_strength_classified(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        strengths = {s["context"]["strength"] for s in secrets}
        self.assertIn(2, strengths, "Strong signature (sk-) should be strength 2")


class TestCauseAnalysis(unittest.TestCase):
    def test_readme_cause_distinguishes_verified_possible(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        causes = analyze.find_causes(readme_problem)
        self.assertTrue(causes)
        c = causes[0]
        self.assertIn("verified_cause", c)
        self.assertIn("possible_causes", c)
        self.assertTrue(c["possible_causes"])

    def test_cause_never_invents_verified_claim(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        causes = analyze.find_causes(readme_problem)
        c = causes[0]
        # Verified cause must be nothing more than the observable fact.
        self.assertIn("not found", c["verified_cause"].lower())

    def test_large_file_cause(self):
        problems = analyze.find_problems(fixture("large-file-project"))
        large = [p for p in problems if p["category"] == "large_file"]
        causes = analyze.find_causes(large[0])
        self.assertTrue(causes)
        self.assertTrue(causes[0]["possible_causes"])
        self.assertNotIn("grew organically", causes[0]["possible_causes"][0].lower())


class TestVerification(unittest.TestCase):
    def test_fact_high_confidence_verified(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        causes = analyze.find_causes(readme_problem)
        status = analyze.verify_finding(readme_problem, causes)
        self.assertIn(status, ("verified", "partially_verified", "unverified"))

    def test_all_findings_have_verification_in_report(self):
        report = analyze.build_report(fixture("without-readme"))
        findings = report["stages"]["4_findings"]
        self.assertTrue(findings)
        for f in findings:
            self.assertIn("verification", f)
            self.assertIn("verification", f["problem"])
            self.assertIn(f["verification"],
                          ("verified", "partially_verified", "unverified"))


class TestSeverity(unittest.TestCase):
    def test_missing_readme_is_low(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        impact = analyze.evaluate_impact(readme_problem)
        self.assertEqual(impact["severity"], "low")

    def test_strong_secret_is_high(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        strong = next(s for s in secrets if s["context"]["strength"] == 2)
        impact = analyze.evaluate_impact(strong)
        self.assertEqual(impact["severity"], "high")

    def test_lone_marker_is_not_high(self):
        problems = analyze.find_problems(fixture("with-todo"))
        markers = [p for p in problems if p["category"] == "code_marker"]
        for m in markers:
            impact = analyze.evaluate_impact(m)
            self.assertNotEqual(impact["severity"], "high",
                                "Lone markers must not be high severity")

    def test_severity_has_confidence_and_reasoning(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        impact = analyze.evaluate_impact(readme_problem)
        self.assertIn("severity_confidence", impact)
        self.assertIn("reasoning", impact)


class TestRecommendations(unittest.TestCase):
    def test_recommendation_based_on_evidence(self):
        problems = analyze.find_problems(fixture("without-readme"))
        readme_problem = next(
            (p for p in problems if "readme" in p["title"].lower()), None)
        causes = analyze.find_causes(readme_problem)
        impact = analyze.evaluate_impact(readme_problem)
        recs = analyze.recommend(readme_problem, impact, causes)
        self.assertTrue(recs)
        self.assertIn("based_on", recs[0])

    def test_recommendation_has_confidence(self):
        problems = analyze.find_problems(fixture("large-file-project"))
        large = [p for p in problems if p["category"] == "large_file"]
        causes = analyze.find_causes(large[0])
        impact = analyze.evaluate_impact(large[0])
        recs = analyze.recommend(large[0], impact, causes)
        self.assertTrue(recs)
        for r in recs:
            self.assertIn("confidence", r)

    def test_secret_recommendation_mentions_verification(self):
        problems = analyze.find_problems(fixture("real-secrets"))
        secrets = [p for p in problems if p["category"] == "possible_secret"]
        causes = analyze.find_causes(secrets[0])
        impact = analyze.evaluate_impact(secrets[0])
        recs = analyze.recommend(secrets[0], impact, causes)
        joined = " ".join(r["recommendation"] for r in recs).lower()
        self.assertIn("verif", joined)


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_report_has_all_sections(self):
        report = analyze.build_report(fixture("simple-python"))
        self.assertIn("target", report)
        self.assertIn("stages", report)
        self.assertIn("1_structure", report["stages"])
        self.assertIn("2_project_type", report["stages"])
        self.assertIn("3_architecture", report["stages"])
        self.assertIn("4_findings", report["stages"])
        self.assertIn("summary", report)
        self.assertTrue(report["read_only_target"])

    def test_json_is_valid(self):
        report = analyze.build_report(fixture("simple-python"))
        dumped = json.dumps(report)
        loaded = json.loads(dumped)
        self.assertEqual(loaded["target"], report["target"])

    def test_summary_counts(self):
        report = analyze.build_report(fixture("without-readme"))
        summary = report["summary"]
        self.assertIn("total_findings", summary)
        self.assertIn("severity_counts", summary)
        self.assertIn("verification_counts", summary)

    def test_findings_sorted_by_severity(self):
        report = analyze.build_report(fixture("real-secrets"))
        findings = report["stages"]["4_findings"]
        sev_order = {"high": 0, "medium": 1, "low": 2, "unknown": 3}
        severities = [sev_order[f["impact"]["severity"]] for f in findings]
        self.assertEqual(severities, sorted(severities))

    def test_markdown_generated(self):
        report = analyze.build_report(fixture("simple-python"))
        md = analyze.render_markdown(report)
        self.assertIn("# Project Analysis Report", md)
        self.assertIn("## 1. Inspect files and structure", md)
        self.assertIn("## 2. Identify project type", md)
        self.assertIn("## 3. Understand architecture", md)
        self.assertIn("## 4. Findings", md)

    def test_markdown_contains_confidence_and_verification(self):
        report = analyze.build_report(fixture("without-readme"))
        md = analyze.render_markdown(report)
        self.assertIn("Confidence", md)
        self.assertIn("Verification", md)
        self.assertIn("Legend", md)

    def test_report_has_verification_counts_in_markdown(self):
        report = analyze.build_report(fixture("without-readme"))
        md = analyze.render_markdown(report)
        self.assertIn("Verification distribution", md)


class TestReadOnlyBehavior(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_target_not_modified_by_build_report(self):
        target = fixture("simple-python")
        snapshot = snapshot_dict(target)
        analyze.build_report(target)
        self.assertEqual(snapshot, snapshot_dict(target))

    def test_target_not_modified_by_full_report(self):
        target = fixture("simple-python")
        snapshot = snapshot_dict(target)
        report = analyze.build_report(target)
        analyze.render_markdown(report)
        analyze.collect_structure(target)
        analyze.detect_project_type(target)
        analyze.understand_architecture(target)
        analyze.find_problems(target)
        self.assertEqual(snapshot, snapshot_dict(target))

    def test_output_written_outside_target(self):
        target = fixture("simple-python")
        snapshot = snapshot_dict(target)
        out_dir = os.path.join(self.tmp, "out")
        report = analyze.build_report(target)
        os.makedirs(out_dir, exist_ok=True)
        md_path = os.path.join(out_dir, "ANALYSIS.md")
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(analyze.render_markdown(report))
        self.assertTrue(os.path.exists(md_path))
        # Target must remain untouched; only the report path is written to.
        self.assertEqual(snapshot, snapshot_dict(target))


class TestCodeSummary(unittest.TestCase):
    def test_summary_has_expected_sections(self):
        summary = analyze.summarize_code(fixture("simple-python"))
        self.assertIn("overview", summary)
        self.assertIn("project_type", summary)
        self.assertIn("languages", summary)
        self.assertIn("symbols", summary)
        self.assertIn("testing", summary)
        self.assertIn("key_observations", summary)
        self.assertIn("limitations", summary)

    def test_summary_json_serializable(self):
        summary = analyze.summarize_code(fixture("simple-nodejs"))
        dumped = json.dumps(summary)
        loaded = json.loads(dumped)
        self.assertEqual(loaded["overview"], summary["overview"])

    def test_summary_detects_python_technologies(self):
        summary = analyze.summarize_code(fixture("large-file-project"))
        names = [t["name"] for t in summary["technologies"]]
        self.assertIn("fastapi", names)

    def test_summary_symbol_counts(self):
        summary = analyze.summarize_code(fixture("large-file-project"))
        counts = summary["symbols"]["counts"]
        self.assertGreater(counts["function"], 0)
        self.assertGreater(counts["class"], 0)

    def test_summary_markdown_rendered(self):
        summary = analyze.summarize_code(fixture("simple-python"))
        md = analyze.render_summary_markdown(summary)
        self.assertIn("# Code Summary", md)
        self.assertIn("## Project Type", md)
        self.assertIn("## Languages", md)
        self.assertIn("## Functions and Classes", md)

    def test_summary_read_only(self):
        target = fixture("simple-python")
        snapshot = snapshot_dict(target)
        analyze.summarize_code(target)
        self.assertEqual(snapshot, snapshot_dict(target))

    def test_summary_no_manifest_type_insufficient(self):
        summary = analyze.summarize_code(fixture("no-manifest"))
        self.assertIsNone(summary["project_type"]["primary"])


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.script = os.path.join(SCRIPTS, "scripts", "analyze.py")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, args, cwd=None):
        return subprocess.run(
            [sys.executable, self.script] + args,
            capture_output=True, text=True, cwd=cwd or self.tmp)

    def test_cli_output_dir(self):
        target = fixture("simple-python")
        out_dir = os.path.join(self.tmp, "out")
        result = self._run([target, "--output", out_dir])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(os.path.join(out_dir, "ANALYSIS.md")))

    def test_cli_output_includes_code_summary(self):
        target = fixture("simple-python")
        out_dir = os.path.join(self.tmp, "out")
        result = self._run([target, "--output", out_dir])
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(os.path.join(out_dir, "ANALYSIS.md"), encoding="utf-8") as fh:
            md = fh.read()
        self.assertIn("Code Summary", md)
        self.assertIn("Project Type", md)

    def test_cli_json(self):
        target = fixture("simple-python")
        out_dir = os.path.join(self.tmp, "out")
        result = self._run([target, "--output", out_dir, "--json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("stages", data)
        self.assertIn("target", data)

    def test_cli_json_valid_after_load(self):
        target = fixture("simple-python")
        out_dir = os.path.join(self.tmp, "out")
        result = self._run([target, "--output", out_dir, "--json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        # Secret values must never leak through CLI JSON.
        self.assertNotIn("sk-", result.stdout)

    def test_cli_target_must_be_dir(self):
        result = self._run(["/nonexistent/path"])
        self.assertNotEqual(result.returncode, 0)

    def test_cli_without_target_usage(self):
        result = self._run([])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage", result.stdout + result.stderr)

    def test_target_not_modified_by_cli(self):
        target = fixture("simple-python")
        snapshot = snapshot_dict(target)
        out_dir = os.path.join(self.tmp, "out")
        self._run([target, "--output", out_dir, "--json"])
        self.assertEqual(snapshot, snapshot_dict(target))


if __name__ == "__main__":
    unittest.main()