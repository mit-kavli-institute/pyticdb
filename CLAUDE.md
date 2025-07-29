# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
```bash
# Run tests using nox
nox -s tests

# Run tests directly with pytest
pytest

# Run specific test file
pytest tests/test_import.py
```

### Code Quality
```bash
# Format code with black (line length 79)
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking with mypy
mypy src/pyticdb
```

### Documentation
```bash
# Build documentation
nox -s docs
```

### Installation
```bash
# Install for development (includes dev dependencies)
pip install -e ".[dev]"

# Install from source
pip install .
```

## Architecture Overview

PyTICDB is a SQLAlchemy-based wrapper for accessing PostgreSQL databases with spatial indexing capabilities, originally designed for the TESS Input Catalog.

### Core Components

1. **conn.py** - Database connection management
   - `Databases`: Global cache for reflected database schemas
   - `reflected_session()`: Creates reflected metadata and session makers
   - Implements multiprocess-safe connection handling with PID guards
   - Disables connection pooling (uses NullPool) for cleaner multiprocess usage

2. **query.py** - Query interface layer
   - `query_by_id()`: Query by primary key(s) with automatic chunking for large ID lists
   - `query_by_loc()`: Spatial cone search using Q3C indexing
   - `query_raw()`: Direct SQL execution
   - Django-style filtering with `column__operator` syntax
   - `@resolve_database` decorator handles database/table resolution

3. **Configuration** - Database credentials via `~/.config/tic/db.conf`
   ```ini
   [database-alias]
   username=USERNAME
   password=PASSWORD
   database=DATABASE-NAME
   host=HOSTDOMAIN
   port=DATABASE-PORT
   ```

### Key Design Patterns

- **Schema Reflection**: Tables are reflected on-demand and cached in `TableReflectionCache`
- **Multiprocess Safety**: Connection guards ensure database connections aren't shared across processes
- **Default Database**: Falls back to "tic_82" database and "ticentries" table if not specified
- **Batch Processing**: Automatically chunks large ID queries to avoid PostgreSQL parameter limits (65535)