# csv2http

[![ci](https://github.com/Kilo59/csv2http/workflows/ci/badge.svg)](https://github.com/Kilo59/csv2http/actions)

## Quick start

Install

```
pip install csv2http
```

Check CLI usage

```
❯ csv2http --help
usage: csv2http [-h] [-c CONCURRENCY] [--method {POST,PATCH,PUT}] file url

HTTP request for every row of a CSV file

positional arguments:
  file                  payload csv file
  url                   URL destination - called with `http` if scheme is absent

options:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Maximum number of concurrent requests (default: 25)
  --method {POST,PATCH,PUT}
                        HTTP method/verb (default: POST)
```

Make POST calls to http://mockbin.org from a local csv file.

```
❯ csv2http my_file.csv mockbin.org/bin/a88f6cf9-e88b-487f-ae98-598807232178 --concurrency 3
 POST http://mockbin.org/bin/mockbin.org/bin/a88f6cf9-e88b-487f-ae98-598807232178
  status codes - {200: 3}
  status codes - {200: 3}
  status codes - {200: 3}
  status codes - {200: 1}
```

Check the bin log
https://mockbin.org/bin/a88f6cf9-e88b-487f-ae98-598807232178/log

## Roadmap

- [x] As Library - Alpha
  - [x] parse csv as dictionary/json - Alpha
  - [x] accept mutator function - Alpha
  - [x] HTTP POST request with json from csv - Alpha
  - [x] limit concurrency - Alpha
  - [ ] non-blocking file IO - ???
  - [ ] hooks for response results - Beta
  - [ ] mkdoc docs - Beta
- [x] As CLI - Beta
  - [x] argparse - Alpha
  - [ ] progress bar - ???
  - [ ] use dedicated CLI library (typer, rich etc.) - Beta
- [x] GH Actions CI (lint, test, etc.)
- [ ] GH Actions CD (publish to pypi)
