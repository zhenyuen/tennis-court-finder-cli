# Contributing

## Code Style

- **Use `defaultdict` instead of `dict.setdefault`** — Prefer `from collections import defaultdict` and `d[key].append(value)` over `d.setdefault(key, []).append(value)`.
- **Avoid `dict.get`** — Use direct access `d[key]` with `in` checks instead of `d.get(key)`. Only use `.get()` when the default value is meaningful and non-trivial.
- **Keep code simple** — Prioritize readability and minimalism. Avoid over-engineering.
- **Only use absolute imports** — Always import from the top-level package (e.g., `from tennis_court_scraper.models import Slot`). Never use relative imports (`from .models import Slot`) or inline `sys.path` manipulation.
- **No magic numbers** — Use named constants. Internal constants prefixed with `_`.
- **Never test private methods** — Private functions (prefixed with `_`) are implementation details. Test only public functions through their public interface.
- **Prefer composition over inheritance** — Build behavior by composing smaller functions and objects. Avoid class hierarchies and `super()` calls unless necessary.
- **Type-hint all functions** — Every function and method must have annotated parameters and return types. Use `pyright` to verify.

## Validation

Before committing:

```bash
uvx ruff check --fix
uv run pyright
uv run pytest tests/ -v
```

All checks must pass with zero errors and warnings.
