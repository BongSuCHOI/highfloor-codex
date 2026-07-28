# PEP 723 and uv Scripts

Use a PEP 723 script for a standalone tool that benefits from explicit Python and dependency metadata without creating project dependency state.

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx==0.28.1"]
# ///
```

Run with:

```bash
uv run --isolated --script tool.py
```

Pin dependencies when reproducibility matters. Keep project code in its declared project environment instead of converting it to a one-off script. Use `scripts/python/new-script.py` to create a no-overwrite skeleton with an explicit Python requirement and repeatable dependencies.
