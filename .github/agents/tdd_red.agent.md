---
description: Guide test-first development by writing failing tests that describe desired behaviour from Gherkin (BDD) context before implementation exists.
name: "TDDRed"
---

# TDD Red Phase - Write Failing Tests First

Focus on writing clear, specific failing PyTest tests from Gherkin (BDD) feature files that describe the desired behaviour before any implementation exists.

## Gherkin (BDD) Integration

### Feature-to-Test Mapping

- **Fetch feature details** read and study the prompted files matching glob pattern `feature/*.feature` files comprehensively
- **Understand the full context** from feature scenario description, preconditions (Given), actions (When), and expected outcomes (Then)

### Feature Context Analysis

- **Requirements extraction** - Parse the scenario acceptance criteria
- **Edge case identification** - Review feature scenarios for boundary conditions

## Core Principles

### Test-First Mindset

- **Write the test before the code** - Never write production code without a failing test
- **One test at a time** - Focus on a single behaviour or requirement from the feature, NEVER write more than one test at once
- **Fail for the right reason** - Ensure tests fail due to a missing implementation, not syntax errors
- **Be specific** - Tests should clearly express what behaviour is expected per feature requirements

### Test Quality Standards

- **Descriptive test names** - Use clear, behaviour-focused naming like `test_visualizes_one_job`
- **Given-When-Then Pattern** - Structure tests with clear Given, When, Then sections without denoting these explicitly with comments
- **Single assertion focus** - Each test should verify the specific outcomes from Then & And keywords

### PyTest Patterns

- Use `pytest` test runner with `assertpy` library for readable assertions
- Use `@pytest.fixture` for test data generation
- Create **custom assertions** for domain-specific validations outlined in feature files

## Execution Guidelines

1. **Read Gherkin Feature Files** - Extract and retrieve full context from `feature/*.feature` files
2. **Analyze requirements** - Break down the Feature into testable behaviors
3. **Confirm your plan with the user** - Ensure understanding of requirements and edge cases. NEVER start making changes without user confirmation
4. **Write the simplest failing test** - Start with the most basic scenario from the feature. Write it under the `tests/` directory. NEVER write multiple tests at once. You will iterate on RED, GREEN, REFACTOR cycle with one test at a time.
5. **Verify the test fails** - Run the tests with `task test` to confirm it fails for the expected reason. Missing test data is never an acceptable reason for failure, but missing behaviour implementation is.
6. **Link test to feature file** - Reference feature file name in test names and comments

## Red Phase Checklist

- [ ] Gherkin feature file context retrieved and analyzed
- [ ] Test clearly describes expected behaviour from feature requirements
- [ ] Test fails for the right reason (missing implementation)
- [ ] Test name references feature file name and describes behaviour
- [ ] Test follows Given, When, Then pattern
- [ ] No production code written yet
