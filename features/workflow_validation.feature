Feature: GitHub Actions Workflow Validation

    Scenario: Complex workflow validation
        Given a complex workflow `complex_workflow.yml`
        When I parse the workflow
        Then the validation should pass

    Scenario: Fail for using branch trigger
        Given a workflow with a `push.branches` trigger `workflow_with_push_branches.yml`
        When I parse the workflow
        Then the validation should fail with message: "Use the `pull_request` trigger instead of the `push.branches` trigger."

    Scenario: Invalid YAML syntax should still return errors
        Given an invalid YAML string "name: Test\non:\n  push: [\n    invalid"
        When I parse the workflow
        Then the validation should fail
        And errors should not be empty
