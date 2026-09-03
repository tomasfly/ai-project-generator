import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "create-project"


class CreateProjectTests(unittest.TestCase):
    def run_generator(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_dry_run_accepts_supported_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as output_directory:
            result = self.run_generator(
                "orders-service",
                "--profile",
                "microservice",
                "--language",
                "python",
                "--framework",
                "fastapi",
                "--output-dir",
                output_directory,
                "--dry-run",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("microservice/python-fastapi", result.stdout)

    def test_rejects_invalid_project_name(self) -> None:
        result = self.run_generator(
            "Orders_Service",
            "--profile",
            "microservice",
            "--language",
            "python",
            "--framework",
            "fastapi",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("lowercase kebab-case", result.stderr)

    def test_rejects_unsupported_technology(self) -> None:
        result = self.run_generator(
            "orders-service",
            "--profile",
            "microservice",
            "--language",
            "node",
            "--framework",
            "express",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("does not support", result.stderr)

    def test_explicit_standard_version_override_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as output_directory:
            result = self.run_generator(
                "orders-service",
                "--profile",
                "microservice",
                "--language",
                "python",
                "--framework",
                "fastapi",
                "--standard-version",
                "2.3.4",
                "--output-dir",
                output_directory,
            )
            project_yml = Path(output_directory) / "orders-service" / "project.yml"
            project_content = project_yml.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('version: "2.3.4"', project_content)

    def test_default_version_is_read_from_configured_source(self) -> None:
        with tempfile.TemporaryDirectory() as output_directory:
            result = self.run_generator(
                "orders-service",
                "--profile",
                "microservice",
                "--language",
                "python",
                "--framework",
                "fastapi",
                "--output-dir",
                output_directory,
            )
            project_yml = Path(output_directory) / "orders-service" / "project.yml"
            project_content = project_yml.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('version: "1.0.0"', project_content)


if __name__ == "__main__":
    unittest.main()