Feature: GitHub Actions Workflow Validation

    Scenario: Fail for using branch trigger
        Given a workflow with a `push.branches` trigger
        When I validate the workflow
        Then the validation should fail with message: "Use the `pull_request` trigger instead of the `push.branches` trigger."
