# Created By  : PabloCM83

from typer import Typer

from eltoque_mcp.cli import app


class TestCliModule:
    """Test suite for the CLI module."""

    def test_app_instance_exists(self):
        """Test that app instance is created."""
        assert app is not None

    def test_app_is_typer_instance(self):
        """Test that app is an instance of Typer."""
        assert isinstance(app, Typer)

    def test_cli_module_importable(self):
        """Test that cli module is importable."""
        from eltoque_mcp import cli

        assert cli is not None

    def test_cli_module_has_app(self):
        """Test that cli module exports app."""
        from eltoque_mcp import cli

        assert hasattr(cli, "app")

    def test_app_is_callable(self):
        """Test that app can be called as a CLI."""
        # Typer apps are callable
        assert callable(app)
