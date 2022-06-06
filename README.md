# csv2http

[![ci](https://github.com/Kilo59/csv2http/workflows/ci/badge.svg)](https://github.com/Kilo59/csv2http/actions)

## Quick start

Install

```
pip install csv2http
```

Check CLI usage

```
csv2http --help
```

```
csv2http my_file.csv mockbin.org/bin/a88f6cf9-e88b-487f-ae98-598807232178
```

## Roadmap

- [x] As Library - Alpha
  - [x] parse csv as dictionary/json - Alpha
  - [x] accept mutator function - Alpha
  - [x] HTTP POST request with json from csv - Alpha
  - [x] limit concurrency - Alpha
  - [ ] non-blocking file IO - ???
  - [ ] hooks for recording response results - Beta
  - [ ] mkdoc docs - Beta
- [x] As CLI - Beta
  - [x] argparse - Alpha
  - [ ] progress bar - ???
  - [ ] use dedicated CLI library (typer, rich etc.) - Beta
- [x] GH Actions CI (lint, test, etc.)
- [ ] GH Actions CD (publish to pypi)

## Example

```
python csv2http/core.py /Users/gabriel/dev/csv2http/tests/data/simple.csv http://mockbin.org/bin/a88f6cf9-e88b-487f-ae98-598807232178
```
