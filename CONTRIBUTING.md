# Contributing

## Code Style

- **Use `defaultdict` instead of `dict.setdefault`** — Prefer `from collections import defaultdict` and `d[key].append(value)` over `d.setdefault(key, []).append(value)`.
- **Avoid `dict.get`** — Use direct access `d[key]` with `in` checks instead of `d.get(key)`. Only use `.get()` when the default value is meaningful and non-trivial.
- **Keep code simple** — Prioritize readability and minimalism. Avoid over-engineering.
- **Use absolute imports** — Always import from the top-level package. Never use relative imports.
- **No magic numbers** — Use named constants. Internal constants prefixed with `_`.
- **Never test private methods** — Private functions (prefixed with `_`) are implementation details. Test only public functions through their public interface.
- **Prefer composition over inheritance** — Build behavior by composing smaller functions and objects. Avoid class hierarchies and `super()` calls unless necessary.

## Validation

Before committing:

```bash
uvx ruff check --fix
uv run pyright
uv run pytest tests/ -v
```

All checks must pass with zero errors and warnings.
