# Tests

Test files for MediaCopyer functionality.

## Running Tests

```bash
# From project root
python tests/test_i18n_logs.py

# From tests directory
cd tests && python test_i18n_logs.py
```

## Adding Tests

1. Name files with `test_` prefix
2. Add path setup:
   ```python
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent))
   ```