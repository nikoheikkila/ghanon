"""Tests for Container model."""

from assertpy import assert_that

from ghanon.models.workflow import Container


class TestContainer:
    """Tests for Container model."""

    def test_image_only(self):
        c = Container.model_validate({"image": "node:18"})
        assert_that(c.image).is_equal_to("node:18")

    def test_with_credentials(self):
        c = Container.model_validate(
            {
                "image": "ghcr.io/owner/image",
                "credentials": {"username": "user", "password": "${{ secrets.TOKEN }}"},
            },
        )
        assert_that(c.credentials.username).is_equal_to("user")

    def test_with_env(self):
        c = Container.model_validate({"image": "node:18", "env": {"NODE_ENV": "test"}})
        assert_that(c.env).contains_entry({"NODE_ENV": "test"})

    def test_with_ports(self):
        c = Container.model_validate({"image": "nginx", "ports": [80, 443, "8080:80"]})
        assert_that(c.ports).is_length(3)

    def test_with_volumes(self):
        c = Container.model_validate(
            {
                "image": "node:18",
                "volumes": ["/tmp:/tmp", "my-vol:/data"],
            },
        )
        assert_that(c.volumes).is_length(2)

    def test_with_options(self):
        c = Container.model_validate({"image": "node:18", "options": "--cpus 2 --memory 4g"})
        assert_that(c.options).contains("--cpus")
