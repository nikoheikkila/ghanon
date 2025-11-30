"""Tests for YAML parsing functionality."""

from assertpy import assert_that

from ghanon.models.workflow import EventType
from ghanon.parser import parse_workflow_yaml


class TestYamlParsing:
    """Tests for YAML parsing functionality."""

    def test_basic_yaml(self):
        yaml = """
name: CI
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello"
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.name).is_equal_to("CI")
        assert_that(w.jobs).contains_key("build")

    def test_on_boolean_fix(self):
        """Test that 'on' is not parsed as boolean True."""
        yaml = """
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo test
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.on).is_equal_to(EventType.PUSH)

    def test_complex_workflow(self):
        yaml = """
name: CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
  workflow_dispatch:
    inputs:
      deploy:
        description: Deploy after build
        type: boolean
        default: false

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '18'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: ['18', '20']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test

  deploy:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - run: echo "Deploying..."
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.name).is_equal_to("CI/CD")
        assert_that(w.jobs).is_length(3)
        assert_that(w.jobs["test"].needs).is_equal_to("lint")
        assert_that(w.jobs["deploy"].needs).is_equal_to(["lint", "test"])
        assert_that(w.jobs["test"].strategy.fail_fast).is_false()
