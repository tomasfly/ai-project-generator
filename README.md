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

Profile files are JSON to keep the generator core simple and dependency-light. Each one has a name, version, technology-to-template mapping, and profile requirements. Add a profile or technology mapping to extend the generator without changing its CLI contract.

Generated projects record the selected standard and profile versions locally in `project.yml`; they do not require the standard repository at runtime.

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

The validator reads `project.yml`, resolves the declared profile and template metadata, checks the profile's required structure, and exits non-zero on failure. It validates the generated project contract rather than a project name.

The future `ai-project update` command may compare standard versions, show changes, apply an explicit migration, and validate. Automatic upgrades and remote template loading are not implemented.

## Tests

```sh
python3 -m unittest discover -s tests
```
