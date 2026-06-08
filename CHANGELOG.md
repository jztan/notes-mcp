# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Bumped the FastMCP pin to a verified compatible set:
  - `fastmcp>=3.4.2,<3.5`
  - `aiosqlite==0.22.1`
  - `pytest==9.0.3`
  - `pytest-asyncio==1.3.0`

### Verified

- Confirmed the project passes its test suite with `fastmcp 3.4.2`, `pytest 9.0.3`, `aiosqlite 0.22.1`, and `pytest-asyncio 1.3.0`.
- The `fastmcp 3.3.x` import regression (top-level imports in `server.py` and `test_server.py` failing during import and test collection) is resolved in `fastmcp 3.4.2`. The pin skips the affected `3.3.x` line.
