Feature: GitHub Actions Workflow Validation with Ghanon

    Scenario Outline: Valid Cases
        Given a workflow "<workflow>"
        When I parse it
        Then the validation should pass
        And I should see message "<workflow>" is a valid workflow

        Examples:
            | workflow             |
            | simple_workflow.yml  |
            | complex_workflow.yml |

    Scenario Outline: Error Cases
        Given a workflow "<workflow>"
        When I parse it
        Then the validation should fail
        And I should see message "<error>"

        Examples:
            | workflow                        | error                                                                 |
            | invalid_key.yml                 | Error parsing workflow file                                           |
            | workflow_with_push_branches.yml | Use the `pull_request` trigger instead of the `push.branches` trigger |
