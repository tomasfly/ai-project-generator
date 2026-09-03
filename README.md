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

Profile files are JSON to keep the generator dependency-free. Each one has a name, version, and technology-to-template mapping. Add a profile or technology mapping to extend the generator without changing its CLI contract.

Generated projects record the selected standard and profile versions locally in `project.yml`; they do not require the standard repository at runtime.

## Tests

```sh
python3 -m unittest discover -s tests
```
