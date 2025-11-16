# Test Plan - Arkatar World Studio

## Overview

This document outlines the testing strategy for Arkatar World Studio, a fantasy world-building and campaign management tool.

## Testing Philosophy

The project follows Test-Driven Development (TDD) principles:
- Tests are written before or alongside implementation
- Each component has corresponding tests
- Tests verify both individual units and integration points

## Backend Testing

### Test Coverage

#### 1. Model Tests (`tests/test_models.py`)

**Purpose**: Verify SQLAlchemy models and database relationships

**Coverage**:
- ✅ Location creation and hierarchy (parent-child relationships)
- ✅ Faction creation and base location association
- ✅ Character creation with faction membership
- ✅ Religion/Deity creation
- ✅ Item/Artifact creation
- ✅ Relation creation between entities
- ✅ Timeline Event creation
- ✅ Story Arc creation with outline

**Test Count**: 10 tests

#### 2. API Tests

**Locations API** (`tests/test_api_locations.py`):
- ✅ Create location
- ✅ Get all locations
- ✅ Get location by ID
- ✅ Update location
- ✅ Delete location
- ✅ Filter by type
- ✅ Search functionality
- ✅ Handle non-existent resources (404)

**Test Count**: 8 tests

**Basic CRUD API** (`tests/test_api_basic.py`):
- ✅ Factions CRUD operations
- ✅ Characters CRUD operations
- ✅ Religions CRUD operations
- ✅ Health endpoint

**Test Count**: 4 tests

**Relations & Items API** (`tests/test_api_relations.py`):
- ✅ Items CRUD operations
- ✅ Relations CRUD operations
- ✅ Entity relations endpoint (get all relations for specific entity)
- ✅ Filter relations by type and source/target

**Test Count**: 4 tests

### Test Execution

```bash
cd backend
pytest tests/ -v
```

**Current Status**: 26 tests passing ✅

### Areas for Future Testing

1. **Simulation Logic** (`app/simulation.py`):
   - Test relation intensity changes
   - Test event generation logic
   - Test edge cases (empty world, single faction)

2. **Export Functionality** (`app/export_markdown.py`):
   - Verify Markdown format correctness
   - Test with various data configurations
   - Test empty world export

3. **World Snapshot API**:
   - Integration test for complete world export
   - Performance test with large datasets

4. **Timeline API**:
   - Test date ordering
   - Test filtering by tags and search
   - Test era handling

5. **Story Arcs API**:
   - Test outline structure
   - Test status filtering
   - Test relationships with events and characters

## Frontend Testing

### Current State

Basic test infrastructure is set up:
- Vitest configuration in `vite.config.ts`
- Testing Library installed
- Test setup file at `src/tests/setup.ts`

### Planned Tests

1. **Component Tests**:
   - Dashboard renders correctly
   - Locations list displays data
   - API calls are made correctly
   - Loading states work
   - Error handling

2. **Integration Tests**:
   - Navigation between views
   - CRUD operations through UI
   - Form submissions
   - Data refresh after operations

### Test Execution

```bash
cd frontend
npm test
```

## CLI Testing

### Manual Testing

The CLI can be manually tested with:

```bash
# List characters
python arkatar_cli.py list-characters

# List factions
python arkatar_cli.py list-factions

# Export to Markdown
python arkatar_cli.py export-markdown --output ./export

# Run simulation
python arkatar_cli.py simulate --ticks 10 --verbose
```

### Planned Automated Tests

1. **Command Parsing**:
   - Test argument parsing
   - Test help messages
   - Test invalid arguments

2. **Database Operations**:
   - Test list commands with sample data
   - Test export generates correct files
   - Test simulation creates events

## Integration Testing

### End-to-End Scenarios

1. **Complete World Creation**:
   - Create locations, factions, characters
   - Establish relations
   - Create timeline events
   - Export to Markdown

2. **Simulation Flow**:
   - Set up initial world state
   - Run simulation
   - Verify events created
   - Verify relations changed

3. **Frontend-Backend Integration**:
   - Start backend server
   - Start frontend dev server
   - Perform CRUD operations through UI
   - Verify database changes

## Performance Testing

### Future Considerations

1. **API Response Times**:
   - Measure response time for large datasets
   - Test pagination effectiveness
   - Test search query performance

2. **Database Performance**:
   - Test with 1000+ entities
   - Measure relation query performance
   - Test simulation with complex relation graphs

3. **Frontend Rendering**:
   - Test list rendering with many items
   - Test dashboard load time
   - Measure memory usage

## Test Metrics

### Current Coverage

| Module | Tests | Status |
|--------|-------|--------|
| Models | 10 | ✅ Passing |
| Locations API | 8 | ✅ Passing |
| Basic CRUD APIs | 4 | ✅ Passing |
| Relations API | 4 | ✅ Passing |
| **Total Backend** | **26** | **✅ All Passing** |
| Frontend | 0 | 📝 TBD |
| CLI | 0 | 📝 Manual Testing |

### Coverage Goals

- **Backend**: 80%+ code coverage (models, CRUD, routes)
- **Business Logic**: 100% coverage (simulation, export)
- **Frontend**: 60%+ component coverage
- **Integration**: Key user workflows covered

## Testing Best Practices

1. **Isolation**: Each test uses a fresh database (via fixtures)
2. **Independence**: Tests don't depend on execution order
3. **Clarity**: Test names describe what is being tested
4. **Fixtures**: Use pytest fixtures for common setup
5. **Assertions**: Clear, specific assertions

## Running All Tests

### Backend
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend
```bash
cd frontend
npm test
```

### Manual Integration Test
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - CLI
python arkatar_cli.py list-factions
```

## Continuous Improvement

This test plan is a living document. As the application grows, tests should be:
- Added for new features
- Updated when functionality changes
- Reviewed for relevance and effectiveness
- Expanded to cover edge cases and bug fixes

## Known Issues / Tech Debt

1. Simulation logic needs dedicated unit tests
2. Export functionality needs format validation tests
3. Frontend has no automated tests yet (setup is ready)
4. CLI needs automated test suite
5. No load/performance tests implemented

## Conclusion

The backend has solid test coverage for core CRUD operations and models. The test infrastructure is in place and follows best practices. Future work should focus on:

1. Testing simulation and export logic
2. Adding frontend component tests
3. Creating automated CLI tests
4. Adding integration tests for complete workflows
5. Performance testing with realistic data volumes
