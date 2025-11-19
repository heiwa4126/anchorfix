# anchorfix Project Rules

## Project Overview

- This is a Python package that converts HTML anchor IDs to sequential numbered format (e.g., `#a0001`, `#a0002`)
- Main purpose: Fix CMS-generated HTML where text-based anchor IDs cause internal link issues
- Package name: anchorfix
- Target Python version: >=3.9
- Build system: uv_build
- License: MIT
- Package manager: uv (with .venv)

## Environment Setup

- **Package manager**: uv with local `.venv` virtual environment
- **Important**: When opening a new terminal, activate the virtual environment with:
  ```bash
  source .venv/bin/activate
  ```
  Or use `uv run` prefix for commands to automatically use the correct environment

## Code Style

- Use dataclasses for structured data
- Keep functions minimal and focused
- Follow Python naming conventions
- Use type hints where appropriate (Python 3.9+ union syntax: `str | None`)
- Type checking: Use `isinstance()` checks for BeautifulSoup's union types (`str | AttributeValueList`)

## Testing

- Test files should be named `*_test.py`
- Use pytest for testing
- Test both functionality and data structure validation
- Integration tests use `examples/` directory files directly
- Run tests with: `poe test` or `uv run pytest`

## Task Execution

Use `poethepoet` (poe) for all development tasks:

```bash
poe test          # Run tests
poe check         # Lint check (ruff)
poe format        # Format code
poe mypy          # Type checking
poe build         # Full build (lint, test, build, smoketest)
poe lint          # All linting (pep440, ruff, mypy, pyproject validation)
```

See `poe_tasks.toml` for all available tasks.

## Dependencies

**Runtime dependencies:**

- beautifulsoup4 (HTML parsing)

**Development dependencies:**

- mypy (type checking)
- pytest (testing)
- ruff (linting & formatting)
- poethepoet (task runner)
- hypothesis (property-based testing)
- bumpuv (version bumping)
- validate-pyproject (project validation)

Add dependencies with:

```bash
uv add <package>           # Runtime dependency
uv add --dev <package>     # Development dependency
```

## File Structure

```
.
├── src/anchorfix/
│   ├── __init__.py         # Public API exports
│   ├── __main__.py         # CLI entry point
│   ├── _core.py            # Core processing logic
│   └── _core_test.py       # Tests
├── examples/               # Test data & documentation examples
│   ├── basic_input.html
│   ├── basic_expected.html
│   ├── incomplete_input.html
│   ├── incomplete_expected.html
│   ├── mixed_links_input.html
│   ├── mixed_links_expected.html
│   └── duplicate_id_input.html
├── pyproject.toml          # Project configuration
├── poe_tasks.toml          # Task definitions
└── README.md               # Full documentation
```

- Test files alongside source files with `_test.py` suffix
- Test files excluded from wheel distribution via `tool.uv.build-backend.wheel-exclude`

## Core Functionality

### Main Functions (`_core.py`)

- `process_html(html_content: str, prefix: str = "a") -> str`
  - Process HTML string, convert anchor IDs to sequential format
  - Returns modified HTML string

- `process_html_file(file_path: str | Path, prefix: str = "a") -> str`
  - Read HTML file and process it
  - Auto-detect encoding (tries UTF-8, then Shift-JIS, then CP932)
  - Returns modified HTML string

- `DuplicateIdError`
  - Exception raised when duplicate IDs are detected
  - Contains `id_value` and `line_numbers` attributes

### CLI (`__main__.py`)

- Entry point: `anchorfix <htmlfile> [--prefix PREFIX]`
- Options:
  - `--prefix PREFIX`: ID prefix (default: "a")
  - `-V, --version`: Show version
  - `-h, --help`: Show help
- Output to stdout (redirect to save: `anchorfix input.html > output.html`)

## Processing Rules

1. **Target elements**: `<h1>`-`<h6>` tags with `id` attribute, `<a>` tags with `name` attribute
2. **ID format**: `{prefix}0001`, `{prefix}0002`, ... (4-digit sequential, starts from 0001)
3. **Overwrite**: All existing `id`/`name` values are replaced
4. **Internal links**: `<a href="#...">` within the same file are automatically updated
5. **External links**: `<a href="other.html#...">` are preserved unchanged
6. **Duplicate detection**: Throws `DuplicateIdError` if same ID appears multiple times
7. **Incomplete HTML**: Accepts HTML fragments (e.g., body content only)

## Quality Checks

All code must pass:

- `poe check` (ruff linting)
- `poe mypy` (type checking with no errors)
- `poe test` (all 19 tests passing)

Run `poe build` before committing to ensure all checks pass.

## Output Format for Large Text Blocks

When providing complete file contents or large code blocks that contain nested code blocks (with triple backticks), wrap the entire output in quadruple backticks (````) to prevent markdown parsing issues and allow easy copy-paste.

Example:

```markdown
[complete file content here with nested `code blocks`]
```
