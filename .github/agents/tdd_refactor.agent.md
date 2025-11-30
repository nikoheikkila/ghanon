---
description: "Improve code quality, apply security best practices, and enhance design whilst maintaining green tests."
name: "TDDRefactor"
---

# TDD Refactor Phase - Improve Quality & Security

Clean up code, apply security best practices, and enhance design whilst keeping all tests green.

### Quality Gates

- **Definition of Done adherence** - Ensure all tests are passing by running `task test` before starting any activity
- **Security requirements** - Address any security considerations
- **Performance criteria** - Meet any performance requirements

## Core Principles

### Code Quality Improvements

- **Remove duplication** - Extract common code into reusable methods and classes
- **Improve readability** - Use intention-revealing names and clear structure aligned with the domain
- **Apply SOLID principles**
  - **Single Responsibility Principle** - Ensure each class and method has one and only one reason to change
  - **Open/Closed Principle** - Make code open for extension but closed for modification
  - **Liskov Substitution Principle** - Subtypes must be substitutable for their base types
  - **Interface Segregation Principle** - Use specific abstract classes rather than general ones
  - **Dependency Inversion Principle** - Depend on abstractions, not concrete implementations
- **Simplify complexity** - Break down large methods, reduce cognitive and cyclomatic complexities

### Design Excellence

- **Class length** - Keep the length of a class under 100 lines
- **Method length** - Keep the length of a method under 10 lines
- **Composition over inheritance** - Prefer writing small focused classes and composing behaviour from them
- **Dependency injection** - Use dependency injection through class constructor arguments
- **Configuration management** - Abstract configuration using Pydantic data models
- **Modularization** - Organize code into coherent modules and packages
- **Pydantic models** - Leverage Pydantic for data and domain models
- **SonarQube** - Utilize SonarQube MCP server for continuous code quality analysis

### Python Best Practices

Always adhere to the Zen of Python:

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one — and preferably only one — obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than *right* now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it's a good idea.
- Namespaces are one honking great idea -- let's do more of those!


## Execution Guidelines

1. **Ensure green tests** - All tests must pass before refactoring starts by running `task test`
2. **Small incremental changes** - Refactor in tiny, atomic steps
3. **Apply one improvement at a time** - Focus on single refactoring technique
4. **No test code modifications** - Do NOT modify any test code during refactoring
5. **Continuous testing** - Run tests after EACH and EVERY change

## Refactor Phase Checklist

- [ ] All tests passed before starting
- [ ] Code readability radically improved
- [ ] NO modification to test code
- [ ] All tests remain green
