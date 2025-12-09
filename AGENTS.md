# AGENTS.md

## Build/Test Commands

- `task install` - Install dependencies (uses uv)
- `task test` - Run format, lint, and tests
- `task test:unit` - Run tests only
- `task test:watch` - Watch mode for TDD
- `task lint` - Lint with pyrefly and ruff
- `task format` - Auto-fix and format code

## Code Style

- **Python 3.14+**, Ruff with `select = ["ALL"]`, 120 char line length
- **Imports**: Standard library → third-party → local (ruff handles sorting)
- **Types**: Required in production code; tests exempt from type annotations
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Models**: Use `StrictModel` (extra="forbid") by default; `FlexibleModel` for user-defined mappings
- **Aliases**: Use `Field(alias="hyphen-name")` for hyphenated YAML keys
- **Validators**: Use `ErrorMessage` enum for validation messages
- **Tests**: Use `assertpy` for assertions, `@pytest.mark.parametrize` for test cases, 100% coverage required

## Key Conventions

- See `.github/copilot-instructions.md` for full architecture and development workflow
- ATDD workflow: Write Gherkin scenarios in `features/`, then failing tests, then implementation
