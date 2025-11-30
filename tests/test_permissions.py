"""Tests for Permissions model."""

from assertpy import assert_that

from ghanon.models.workflow import PermissionLevel, PermissionsEvent


class TestPermissions:
    """Tests for Permissions model."""

    def test_all_permissions(self):
        p = PermissionsEvent.model_validate(
            {
                "actions": "read",
                "attestations": "write",
                "checks": "write",
                "contents": "read",
                "deployments": "write",
                "discussions": "read",
                "id-token": "write",
                "issues": "write",
                "models": "read",
                "packages": "write",
                "pages": "write",
                "pull-requests": "write",
                "repository-projects": "read",
                "security-events": "write",
                "statuses": "write",
            },
        )
        assert_that(p.actions).is_equal_to(PermissionLevel.READ)
        assert_that(p.id_token).is_equal_to(PermissionLevel.WRITE)
        assert_that(p.models).is_equal_to("read")  # models has restricted enum
