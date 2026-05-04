# Created By  : PabloCM83


from eltoque_mcp.ext.pydantic_extra_types import EXTRA_CURRENCIES, ISO4217Plus


class TestExtraCurrencies:
    """Test suite for EXTRA_CURRENCIES constant."""

    def test_extra_currencies_is_list(self):
        """Test that EXTRA_CURRENCIES is a list."""
        assert isinstance(EXTRA_CURRENCIES, list)

    def test_extra_currencies_not_empty(self):
        """Test that EXTRA_CURRENCIES is not empty."""
        assert len(EXTRA_CURRENCIES) > 0

    def test_extra_currencies_count(self):
        """Test the number of extra currencies."""
        # According to the source, there should be 3 Cuban currencies
        assert len(EXTRA_CURRENCIES) == 3

    def test_extra_currencies_structure(self):
        """Test that each extra currency has required fields."""
        for currency in EXTRA_CURRENCIES:
            assert isinstance(currency, dict)
            assert "alpha_3" in currency
            assert "name" in currency
            assert "numeric" in currency

    def test_extra_currencies_cuban_codes(self):
        """Test that Cuban currency codes are present."""
        codes = {curr["alpha_3"] for curr in EXTRA_CURRENCIES}
        expected_codes = {"CUC", "CLA", "MLC"}
        assert codes == expected_codes

    def test_extra_currencies_cuc(self):
        """Test Cuban Convertible Peso entry."""
        cuc = next(c for c in EXTRA_CURRENCIES if c["alpha_3"] == "CUC")
        assert cuc["name"] == "Cuban Convertible Peso"
        assert cuc["numeric"] == "931"

    def test_extra_currencies_cla(self):
        """Test Cuban Classic Card entry."""
        cla = next(c for c in EXTRA_CURRENCIES if c["alpha_3"] == "CLA")
        assert cla["name"] == "Cuban Clasic Card (USD)"
        assert cla["numeric"] == "998"

    def test_extra_currencies_mlc(self):
        """Test Freely Convertible Money entry."""
        mlc = next(c for c in EXTRA_CURRENCIES if c["alpha_3"] == "MLC")
        assert mlc["name"] == "Freely Convertible Money"
        assert mlc["numeric"] == "931"

    def test_extra_currencies_all_have_alpha_3(self):
        """Test that all currencies have alpha_3 code."""
        for currency in EXTRA_CURRENCIES:
            assert len(currency["alpha_3"]) == 3
            assert currency["alpha_3"].isupper()

    def test_extra_currencies_all_have_names(self):
        """Test that all currencies have names."""
        for currency in EXTRA_CURRENCIES:
            assert isinstance(currency["name"], str)
            assert len(currency["name"]) > 0

    def test_extra_currencies_all_have_numeric(self):
        """Test that all currencies have numeric codes."""
        for currency in EXTRA_CURRENCIES:
            assert isinstance(currency["numeric"], str)
            assert currency["numeric"].isdigit()
            assert len(currency["numeric"]) == 3


class TestISO4217PlusImport:
    """Test suite for ISO4217Plus import."""

    def test_iso4217plus_is_importable(self):
        """Test that ISO4217Plus is importable."""
        assert ISO4217Plus is not None

    def test_iso4217plus_is_class(self):
        """Test that ISO4217Plus is a class."""
        assert isinstance(ISO4217Plus, type)

    def test_iso4217plus_subclass_of_str(self):
        """Test that ISO4217Plus is a subclass of str."""
        assert issubclass(ISO4217Plus, str)

    def test_iso4217plus_allowed_currencies_populated(self):
        """Test that allowed_currencies set is populated."""
        assert len(ISO4217Plus.allowed_currencies) > 0

    def test_iso4217plus_has_extra_currences(self):
        """Test that ISO4217Plus includes extra currencies."""
        extra_codes = {curr["alpha_3"] for curr in EXTRA_CURRENCIES}
        assert extra_codes.issubset(ISO4217Plus.allowed_currencies)


class TestPydanticExtraTypesModule:
    """Test suite for the pydantic_extra_types module."""

    def test_module_all_exports(self):
        """Test that __all__ is defined."""
        import eltoque_mcp.ext.pydantic_extra_types as module

        assert hasattr(module, "__all__")
        assert "EXTRA_CURRENCIES" in module.__all__
        assert "ISO4217Plus" in module.__all__

    def test_module_exports_accessible(self):
        """Test that all exports are accessible."""
        from eltoque_mcp.ext import pydantic_extra_types

        assert hasattr(pydantic_extra_types, "EXTRA_CURRENCIES")
        assert hasattr(pydantic_extra_types, "ISO4217Plus")

    def test_iso4217plus_validation_with_extra_currencies(self):
        """Test that ISO4217Plus validates using extra currencies."""
        from pydantic import BaseModel

        class Model(BaseModel):
            currency: ISO4217Plus

        # Should accept custom Cuban currencies
        for code in ["CUC", "CLA", "MLC"]:
            model = Model(currency=code)
            assert model.currency == code
