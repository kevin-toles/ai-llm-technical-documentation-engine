# Workflow Decision Framework
## Selective Adoption of "79 Code Rabbit" TDD + Document Hierarchy

**Status**: ACTIVE  
**Adopted**: November 13, 2025  
**Approach**: Option A - Selective Adoption

---

## I. Workflow Decision Tree

```
START: New Task/WBS Item
    │
    ├─ Is this an ARCHITECTURAL decision?
    │  ├─ YES → Use FULL WORKFLOW (Steps 1-7)
    │  └─ NO → Continue
    │
    ├─ Does this introduce NEW PATTERNS?
    │  ├─ YES → Use FULL WORKFLOW (Steps 1-7)
    │  └─ NO → Continue
    │
    ├─ Does WBS conflict with ARCH/PY guidelines?
    │  ├─ YES → Use FULL WORKFLOW (Steps 1-7)
    │  └─ NO → Continue
    │
    ├─ Is this SECURITY/PERFORMANCE critical?
    │  ├─ YES → Use FULL WORKFLOW (Steps 1-7)
    │  └─ NO → Use LIGHTWEIGHT TDD
    │
    └─ For all other tasks → Use LIGHTWEIGHT TDD
```

---

## II. Full Workflow (Steps 1-7)

### When to Use:
✅ **Architectural Decisions**
- Designing new module structure
- Choosing design patterns
- Defining component interfaces
- System-wide refactoring

✅ **New Pattern Implementation**
- First use of Builder, Factory, Strategy, etc.
- Implementing patterns from ARCHITECTURE_GUIDELINES
- Creating reusable abstractions

✅ **Conflict Resolution**
- WBS item conflicts with guidelines
- Multiple valid approaches exist
- Trade-offs between patterns

✅ **Critical Code**
- Security-sensitive operations
- Performance-critical paths
- Data validation/integrity
- Error handling strategies

### Process:

#### **Steps 1-3: Document Analysis (BEFORE coding)**

**Step 1 - BOOK_TAXONOMY_MATRIX Review** (30-45 min)
```bash
# 1. Open docs/BOOK_TAXONOMY_MATRIX.md
# 2. Identify applicable textbooks for current task
# 3. Map task concepts to taxonomy (discipline/concept/topic)
# 4. List relevant high-level concepts

Example Output:
- Task: "Implement caching layer"
- Textbooks: Architecture Patterns with Python, Python Distilled
- Concepts: caching, memoization, cache invalidation, performance
```

**Step 2 - Guideline Cross-Referencing** (45-60 min)
```bash
# 1. Open guidelines/ARCHITECTURE_GUIDELINES_...md
# 2. Open guidelines/PYTHON_GUIDELINES_...md
# 3. Search for concepts identified in Step 1
# 4. Review annotations and cross-reference tables
# 5. Note referenced textbook chapters/sections
# 6. Review chapter summaries for relevance
# 7. Identify specific JSON sections to read

Example Output:
- ARCH Guidelines § 4.2: References "Architecture Patterns Ch. 7"
- PY Guidelines § 3.5: References "Python Distilled Ch. 5.3"
- JSON sections to read: arch_patterns.json lines 450-520
```

**Step 3 - Conflict Identification** (15-30 min)
```bash
# 1. Compare findings from BOOK_TAXONOMY, ARCH, PY guidelines
# 2. Document discrepancies/contradictions
# 3. Resolve by document priority:
#    1. REFACTORING_PLAN.md
#    2. BOOK_TAXONOMY_MATRIX.md
#    3. ARCHITECTURE_GUIDELINES
#    4. PYTHON_GUIDELINES
# 4. Generate Conflict Assessment if WBS conflicts with guidelines

Example Output:
- Conflict: WBS suggests Strategy pattern, ARCH suggests Factory
- Resolution: Follow ARCH (higher priority for patterns)
- OR: Create formal Conflict Assessment for user approval
```

**Document Analysis Output** → Save as `docs/analysis/[task-name]-analysis.md`

#### **Step 4: TDD Implementation** (RED → GREEN → REFACTOR)

**RED Phase:**
```python
# Create failing test FIRST
# tests/test_[feature].py

def test_caching_layer_stores_values():
    """Cache should store and retrieve values."""
    cache = CacheLayer()
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # FAILS - CacheLayer doesn't exist yet
```

**GREEN Phase:**
```python
# Minimal implementation to pass test
# src/cache_layer.py

class CacheLayer:
    def __init__(self):
        self._store = {}
    
    def set(self, key, value):
        self._store[key] = value
    
    def get(self, key):
        return self._store.get(key)
```

**REFACTOR Phase:**
```python
# Clean code + align with guidelines
# src/cache_layer.py

from typing import Any, Optional, Dict
from dataclasses import dataclass, field

@dataclass
class CacheLayer:
    """
    Cache layer implementation following Repository pattern.
    
    References:
    - ARCHITECTURE_GUIDELINES § 4.2 (Caching Strategies)
    - Architecture Patterns with Python Ch. 7
    """
    _store: Dict[str, Any] = field(default_factory=dict, init=False)
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache."""
        self._store[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
        return self._store.get(key)
```

#### **Steps 5-7: Continuous Quality + Verification**

**Step 5: Continuous Compliance**
- Maintain traceability comments (references to guidelines/JSON sections)
- Apply patterns from document analysis
- Use type hints, docstrings per PYTHON_GUIDELINES

**Step 6: Quality Gates (after EVERY change)**
```bash
# Run ALL these checks before commit:

# 1. Ruff
ruff check src/[modified-file].py

# 2. Type checking
mypy src/[modified-file].py

# 3. Tests
pytest tests/test_[feature].py -v

# 4. Full test suite (no regressions)
pytest tests/ -q

# 5. SonarQube (if running)
sonar-scanner

# All must PASS before proceeding
```

**Step 7: Final Alignment**
- [ ] All quality gates pass
- [ ] All tests pass (unit + integration)
- [ ] No regressions in existing tests
- [ ] Code complies with all 4 guiding documents
- [ ] Document references recorded in commit message

**Commit Message Format:**
```
[PATTERN] Brief description

FULL WORKFLOW APPLIED:
- Analysis: docs/analysis/[task]-analysis.md
- Pattern: [Pattern Name] from ARCH § X.Y
- Guidelines: ARCH § X.Y, PY § Z.W
- JSON Refs: [Book] Ch. N pp. XXX-YYY
- Tests: X/X passing
- Quality: Ruff clean, mypy clean

TDD Cycle: RED → GREEN → REFACTOR complete
```

---

## III. Lightweight TDD Workflow

### When to Use:
✅ **Routine Implementation**
- Simple extractions (like Sprint 3.1-3.4)
- Following established patterns
- File copying/adaptation
- Configuration changes
- Test writing for known patterns

✅ **Non-Architectural Changes**
- Bug fixes
- Documentation updates
- Refactoring within established structure
- Performance optimizations (non-critical)

### Process:

#### **Quick Check** (5 min)
```bash
# 1. Review REFACTORING_PLAN.md for this task (30 sec)
# 2. Confirm no architectural decision needed (30 sec)
# 3. Identify existing pattern to follow (1 min)
# 4. Proceed with TDD
```

#### **TDD Cycle** (RED → GREEN → REFACTOR)

**RED:**
```python
# Write failing test
def test_feature():
    assert expected_behavior()  # FAILS
```

**GREEN:**
```python
# Minimal implementation
def feature():
    return expected_result
```

**REFACTOR:**
```python
# Clean + type hints + docstring
def feature() -> ResultType:
    """Brief description."""
    return expected_result
```

#### **Quality Gates** (before commit)
```bash
# Minimum checks:
ruff check src/[file].py
pytest tests/test_[feature].py -v
pytest tests/ -q  # No regressions

# Optional (if time):
mypy src/[file].py
```

#### **Commit Message Format:**
```
[TYPE] Brief description

LIGHTWEIGHT TDD:
- Pattern: [Following existing pattern from Sprint X.Y]
- Tests: X/X passing
- Quality: Ruff clean

TDD: RED → GREEN → REFACTOR
```

---

## IV. Conflict Assessment Template

**Use when**: WBS/REFACTORING_PLAN conflicts with ARCH/PY guidelines

```markdown
## Conflict Assessment: [Task Name]

**WBS Item**: Sprint X.Y - [Description]

**Conflicting Guideline(s)**: 
- ARCHITECTURE_GUIDELINES § X.Y: [Quote/Summary]
- PYTHON_GUIDELINES § Z.W: [Quote/Summary]

**Nature of Conflict**: 
[ ] Design approach
[ ] Implementation pattern
[ ] Dependency management
[ ] Performance strategy
[ ] Security concern
[ ] Code consistency

**Option A - Follow Guidelines**
- **Pros**: Compliance, maintainability, security, best practices
- **Cons**: May require re-scoping WBS, timeline impact
- **Effort**: [X hours]

**Option B - Adapt WBS to Meet Guidelines**
- **Pros**: Preserves intent, gains compliance, sustainable
- **Cons**: Re-planning required, WBS changes
- **Effort**: [Y hours]

**Option C - Time-Boxed Deviation (with remediation plan)**
- **Pros**: Short-term delivery, meets deadline
- **Cons**: Technical debt, future refactor needed, risk
- **Effort**: [Z hours + remediation]
- **Remediation**: [Plan to align with guidelines in Sprint X+N]

**Recommendation**: [A / B / C]

**Rationale**: 
[Explanation of why this option is best given current constraints]

**Approval Needed From**: [User / Technical Lead / Team]

**Decision**: [To be filled after user approval]
**Date**: [Date]
```

---

## V. Task Classification Examples

### Use FULL WORKFLOW:

| Task | Why Full Workflow |
|------|-------------------|
| Design caching layer | Architectural decision |
| Implement Factory pattern | New pattern introduction |
| Create authentication system | Security critical |
| Optimize database queries | Performance critical |
| Design microservice communication | Architectural + new patterns |

### Use LIGHTWEIGHT TDD:

| Task | Why Lightweight |
|------|-----------------|
| Extract data models (Sprint 3.1) | Following established extraction pattern |
| Copy pipeline files (Sprint 4) | File adaptation, non-architectural |
| Add new test case | Test writing |
| Fix bug in existing code | Bug fix, pattern already exists |
| Update configuration | Configuration change |

---

## VI. Sprint 4 Application Plan

**Sprint 4: Pipeline Integration**

### Planning Phase (Use FULL WORKFLOW):
- **Step 1**: Review BOOK_TAXONOMY_MATRIX for microservices patterns
- **Step 2**: Review ARCHITECTURE_GUIDELINES for pipeline architecture
- **Step 3**: Identify conflicts between tpm-job-finder-poc and guidelines
- **Output**: `docs/analysis/sprint4-pipeline-analysis.md`
- **Time**: 2-3 hours

### Execution Phase (Use LIGHTWEIGHT TDD):
- File copying from tpm-job-finder-poc
- Path updates
- Dependency adaptation
- Integration testing
- **Time**: 8-12 hours

### Decision Points (Switch to FULL WORKFLOW if):
- New architectural pattern needed
- Conflict discovered between codebases
- Security/performance concern arises

---

## VII. Success Metrics

### Full Workflow Success:
- [ ] Analysis document created before coding
- [ ] All 4 guiding documents consulted
- [ ] Conflicts documented and resolved
- [ ] Pattern traceable to specific guideline section
- [ ] All quality gates pass

### Lightweight TDD Success:
- [ ] Existing pattern identified and followed
- [ ] Tests written before implementation
- [ ] Quality gates pass (Ruff + tests)
- [ ] No regressions

### Overall Sprint Success:
- [ ] Zero regressions
- [ ] All tests passing
- [ ] Code aligned with guidelines (where applicable)
- [ ] Technical debt minimized

---

## VIII. Appendix: Document Locations

```
Project Root: /Users/kevintoles/POC/llm-document-enhancer/

Priority Documents (in order):
1. REFACTORING_PLAN.md
2. docs/BOOK_TAXONOMY_MATRIX.md
3. guidelines/ARCHITECTURE_GUIDELINES_Architecture_Patterns_with_Python_LLM_ENHANCED.md
4. guidelines/PYTHON_GUIDELINES_Learning_Python_Ed6_LLM_ENHANCED.md

Analysis Output:
- docs/analysis/[task-name]-analysis.md

Quality Tools:
- Ruff: ruff check src/
- Mypy: mypy src/
- Pytest: pytest tests/
- SonarQube: http://localhost:9000
```

---

**Last Updated**: November 13, 2025  
**Status**: Active - Sprint 3 Complete, Ready for Sprint 4
