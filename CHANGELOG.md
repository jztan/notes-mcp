# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Updated dependency guidance to a verified compatible set:
  - `fastmcp>=3.2.4,<3.3`
  - `aiosqlite==0.22.1`
  - `pytest==9.0.3`
  - `pytest-asyncio==1.3.0`

### Verified

- Confirmed the project passes its test suite with `fastmcp 3.2.4`, `pytest 9.0.3`, `aiosqlite 0.22.1`, and `pytest-asyncio 1.3.0`.
- Confirmed the current `fastmcp 3.3.1` release is not compatible with this codebase as written because top-level imports used by `server.py` and `test_server.py` fail during import and test collection.
