import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CREATE_SCRIPT = ROOT / "scripts" / "create-project"
VALIDATE_SCRIPT = ROOT / "scripts" / "ai-project"


class ValidateProjectTests(unittest.TestCase):
    def create_project(self, output_directory: Path) -> Path:
        result = subprocess.run(
            [
                sys.executable,
                str(CREATE_SCRIPT),
                "orders-service",
                "--profile",
                "microservice",
                "--language",
                "python",
                "--framework",
                "fastapi",
                "--output-dir",
                str(output_directory),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return output_directory / "orders-service"

    def validate(self, project_directory: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT), "validate", "--project-dir", str(project_directory)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_generated_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.validate(self.create_project(Path(directory)))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_project_yml_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            (project / "project.yml").unlink()
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project.yml", result.stdout)

    def test_missing_agents_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            (project / "AGENTS.md").unlink()
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AGENTS.md", result.stdout)

    def test_missing_integration_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            shutil.rmtree(project / "tests" / "integration")
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tests/integration/", result.stdout)

    def test_missing_dockerfile_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            (project / "Dockerfile").unlink()
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Dockerfile", result.stdout)

    def test_missing_template_metadata_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            project_yml = project / "project.yml"
            project_yml.write_text(
                project_yml.read_text(encoding="utf-8").replace(
                    'template:\n  name: python-fastapi\n  version: "1.0.0"\n\n', ""
                ),
                encoding="utf-8",
            )
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("template metadata missing", result.stdout)

    def test_invalid_version_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.create_project(Path(directory))
            project_yml = project / "project.yml"
            project_yml.write_text(
                project_yml.read_text(encoding="utf-8").replace('version: "1.0.0"', 'version: "v1"', 1),
                encoding="utf-8",
            )
            result = self.validate(project)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAJOR.MINOR.PATCH", result.stdout)


if __name__ == "__main__":
    unittest.main()