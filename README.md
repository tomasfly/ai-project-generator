# AI Project Generator

A small, extensible generator for creating self-contained projects from the AI Engineering Standard and a project profile.

The included concrete template generates a Python/FastAPI microservice. The generated project records the standard and profile versions locally and does not depend on the standard repository at runtime.

## Repository layout

- `templates/`: technology and profile templates; each template is self-contained.
- `scripts/`: generator entry points.
- `config/profiles/`: generator-facing profile metadata that maps technologies to templates.
- `tests/`: generator tests using the standard library.

## Usage

```sh
./scripts/create-project orders-service \
  --profile microservice \
  --language python \
  --framework fastapi
```

Add `--dry-run` to validate the project name and selected profile without writing files.

## Use Cases

Run commands from the generator repository:

```sh
cd ai-project-generator
```

### Inspect Available Commands

```sh
python3 scripts/create-project --help
python3 scripts/ai-project --help
```

### Create a Project

The current supported combination is `microservice` + `python` + `fastapi`:

```sh
python3 scripts/create-project orders-service \
  --profile microservice \
  --language python \
  --framework fastapi \
  --output-dir ..
```

The project is created at `../orders-service`. The `name` argument must be lowercase kebab-case, such as `orders-service`.

| Argument | Required | Description |
| --- | --- | --- |
| `name` | Yes | Project name in lowercase kebab-case. |
| `--profile` | Yes | Profile name from `config/profiles/`. |
| `--language` | Yes | Language declared by the selected profile. |
| `--framework` | Yes | Framework declared by the selected profile. |
| `--output-dir` | No | Parent directory for the new project; defaults to the current directory. |
| `--standard-version` | No | Explicit `MAJOR.MINOR.PATCH` Standard version override. |
| `--dry-run` | No | Validates the request and shows the resolved template without creating files. |

Use a dry run before creating a project:

```sh
python3 scripts/create-project orders-service \
  --profile microservice \
  --language python \
  --framework fastapi \
  --dry-run
```

When the Standard checkout is not at the local path configured in `config/generator.json`, provide its version explicitly:

```sh
python3 scripts/create-project payments-service \
  --profile microservice \
  --language python \
  --framework fastapi \
  --standard-version 1.0.0 \
  --output-dir ..
```

### Validate a Generated Project

Install the generator dependencies, then validate from the generator repository:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/ai-project validate --project-dir ../orders-service
```

The generated project also includes the validator, so it can be run in place:

```sh
cd ../orders-service
./scripts/ai-project validate
```

### Add a Technology Template

To support a new technology for an existing profile, create a self-contained template and map it in that profile. For example, to add a Node.js/Express microservice:

1. Create `templates/microservice/node-express/` by using `templates/microservice/python-fastapi/` as the structural reference.
2. Add `templates/microservice/node-express/template.yml`:

   ```yaml
   template:
     name: node-express
     version: "1.0.0"
   ```

3. Include every file and directory required by `config/profiles/microservice.json`, adapting the implementation to the technology. Keep token placeholders such as `__PROJECT_NAME__`, `__STANDARD_VERSION__`, `__PROFILE_NAME__`, `__PROFILE_VERSION__`, `__TEMPLATE_VERSION__`, `__LANGUAGE__`, and `__FRAMEWORK__` where generated metadata or documentation needs them.
4. Add the mapping to the `technologies` array in `config/profiles/microservice.json`:

   ```json
   {
     "language": "node",
     "framework": "express",
     "template": "node-express"
   }
   ```

5. Check template resolution before creating a project:

   ```sh
   python3 scripts/create-project catalog-service \
     --profile microservice \
     --language node \
     --framework express \
     --dry-run
   ```

### Add a Profile

Create a profile when its required project contract differs from an existing profile, such as a frontend application. Add `config/profiles/frontend.json` with the supported technology mappings and the files/directories that validation must require:

```json
{
  "name": "frontend",
  "version": "1.0.0",
  "description": "Web application.",
  "technologies": [
    {
      "language": "typescript",
      "framework": "react-vite",
      "template": "typescript-react-vite"
    }
  ],
  "requirements": {
    "files": ["AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md", "README.md", "project.yml", "package.json"],
    "directories": [".github", "src", "tests", "docs", "docs/architecture"],
    "docker": {},
    "architecture_document": "docs/architecture/overview.md"
  }
}
```

Create the matching self-contained template at `templates/frontend/typescript-react-vite/`, including `template.yml` and all required files. Then verify the new mapping:

```sh
python3 scripts/create-project customer-portal \
  --profile frontend \
  --language typescript \
  --framework react-vite \
  --dry-run
```

Profile files are JSON to keep the generator core simple and dependency-light. Each one has a name, version, technology-to-template mapping, and profile requirements. Add a profile or technology mapping to extend the generator without changing its CLI contract.

Generated projects record the selected standard and profile versions locally in `project.yml`; they do not require the standard repository at runtime.

The generator reads the Standard version from the local path configured in `config/generator.json`, normally the sibling repository's `ai-engineering-standard/VERSION`. It never performs network access to resolve a version and never invents a default. Use `--standard-version` for an explicit override when the canonical checkout is elsewhere.

## Resolution Model

- **Profile**: what kind of project is required, such as a microservice or backend.
- **Template**: how that project is implemented with a technology, such as Python/FastAPI.
- **Generator**: resolves profile + language + framework + template and copies the selected self-contained files.

The current mapping is deliberately small: `microservice` + `python` + `fastapi` resolves to the `python-fastapi` template. Future combinations can be added as profile metadata and a real project requires them; no extra technology templates are included yet.

## Validate a Project

Install the validator's YAML dependency, then run it from a generated project:

```sh
pip install -r requirements.txt
./scripts/ai-project validate
```

The validator reads `project.yml`, resolves the declared profile and template metadata, checks the profile's required structure, and exits non-zero on contract failure. It validates the generated project contract rather than a project name. Output distinguishes each declared version from the currently available metadata. If they differ, structural validation continues with a warning; exact historical validation is not claimed.

A generated project is self-contained in source, tests, documentation, AI instructions, Docker configuration, metadata, and runtime dependencies. It does not contain the complete generator repository. The externally installed `ai-project` CLI may validate it, while runtime operation remains independent of both repositories.

The future `ai-project update` command may compare standard versions, show changes, apply an explicit migration, and validate. Automatic upgrades and remote template loading are not implemented.

For historical reproducibility, future releases should use immutable Git tags or releases for the Standard, Generator, and templates. Version fields identify the contracts; immutable releases provide the artifacts needed for exact historical validation.

## Tests

```sh
python3 -m unittest discover -s tests
```
