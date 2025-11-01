# Tests

This directory contains test files for MediaCopyer.

## Test Files

- `test_i18n_logs.py` - Tests for internationalization (i18n) log messages

## Running Tests

To run tests from the project root directory:

```bash
# Run a specific test
python tests/test_i18n_logs.py

# Or run from the tests directory
cd tests
python test_i18n_logs.py
```

## Adding New Tests

When adding new test files:

1. Name them with the `test_` prefix
2. Add the path setup at the beginning:
   ```python
   import sys
   from pathlib import Path
   
   # Add the project root to the path (parent of tests directory)
   sys.path.insert(0, str(Path(__file__).parent.parent))
   ```
3. Import the modules you need to test
4. Document the test in this README