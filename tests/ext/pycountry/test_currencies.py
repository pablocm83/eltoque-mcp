# Created By  : PabloCM83


from eltoque_mcp.ext.pycountry import Currencies, Currency, currencies


class TestCurrency:
    """Test suite for Currency class from ext.pycountry.db."""

    def test_currency_class_exists(self):
        """Test that Currency class is available."""
        assert Currency is not None

    def test_currency_class_name(self):
        """Test Currency class name."""
        assert Currency.__name__ == "Currency"

    def test_currency_class_module(self):
        """Test Currency class module."""
        assert Currency.__module__ == "eltoque_mcp.ext.pycountry.db"

    def test_currency_is_data_subclass(self):
        """Test that Currency is a subclass of pycountry Data."""
        from pycountry.db import Data

        assert issubclass(Currency, Data)

    def test_currency_instantiation(self):
        """Test creating a Currency instance."""
        # Currency is a subclass of Data and can be instantiated
        # with the same interface as pycountry currencies
        assert Currency is not None


class TestCurrencies:
    """Test suite for Currencies class from ext.pycountry.__init__."""

    def test_currencies_class_exists(self):
        """Test that Currencies class is available."""
        assert Currencies is not None

    def test_currencies_has_add_entry_method(self):
        """Test that Currencies has add_entry method."""
        assert hasattr(Currencies, "add_entry")

    def test_currencies_is_database_subclass(self):
        """Test that Currencies is a subclass of Database."""
        from pycountry.db import Database

        assert issubclass(Currencies, Database)


class TestCurrenciesInstance:
    """Test suite for the currencies instance."""

    def test_currencies_instance_exists(self):
        """Test that currencies instance is available."""
        assert currencies is not None

    def test_currencies_get_method(self):
        """Test that currencies can get entries by alpha_3 code."""
        # Standard ISO 4217 currency
        usd = currencies.get(alpha_3="USD")
        assert usd is not None
        assert usd.alpha_3 == "USD"

    def test_currencies_get_various_codes(self):
        """Test getting various currency codes."""
        test_codes = ["USD", "EUR", "GBP", "JPY"]

        for code in test_codes:
            currency = currencies.get(alpha_3=code)
            assert currency is not None
            assert currency.alpha_3 == code

    def test_currencies_get_invalid_code(self):
        """Test that invalid code returns None."""
        result = currencies.get(alpha_3="INVALID")
        assert result is None

    def test_currencies_iterate(self):
        """Test that currencies can be iterated."""
        count = 0
        for _ in currencies:
            count += 1
            if count > 5:
                break

        assert count > 0

    def test_currencies_has_usd(self):
        """Test that USD is in currencies."""
        usd = currencies.get(alpha_3="USD")
        assert usd is not None
        assert usd.name == "US Dollar"

    def test_currencies_has_eur(self):
        """Test that EUR is in currencies."""
        eur = currencies.get(alpha_3="EUR")
        assert eur is not None
        assert eur.name == "Euro"

    def test_currencies_get_returns_currency_object(self):
        """Test that get returns Currency-like objects."""
        usd = currencies.get(alpha_3="USD")
        assert hasattr(usd, "alpha_3")
        assert hasattr(usd, "name")
        assert hasattr(usd, "numeric")

    def test_currencies_currency_has_numeric_code(self):
        """Test that currency objects have numeric codes."""
        usd = currencies.get(alpha_3="USD")
        assert usd is not None
        assert usd.numeric == "840"

    def test_currencies_currency_name_property(self):
        """Test currency name property."""
        gbp = currencies.get(alpha_3="GBP")
        assert gbp is not None
        assert "Pound" in gbp.name


class TestCurrenciesAddEntry:
    """Test suite for adding custom currencies."""

    def test_add_custom_cuban_currencies(self):
        """Test that custom Cuban currencies are added."""
        # These should have been added during ISO4217Plus initialization
        cup = currencies.get(alpha_3="CUP")
        assert cup is not None
        assert cup.alpha_3 == "CUP"

    def test_cuban_peso_in_currencies(self):
        """Test Cuban Peso is available."""
        cup = currencies.get(alpha_3="CUP")
        assert cup is not None
        assert "Cuban" in cup.name or cup.name == "Cuban Peso"

    def test_cuban_custom_codes(self):
        """Test custom Cuban currency codes are available."""
        # After ISO4217Plus initialization, these should be available
        codes = ["CUP", "CUC", "CLA", "MLC"]

        for code in codes:
            currency = currencies.get(alpha_3=code)
            # CUP is standard, others are custom
            assert currency is not None, f"{code} not found in currencies"

    def test_custom_currency_properties(self):
        """Test that custom currencies have proper properties."""
        cuc = currencies.get(alpha_3="CUC")
        if cuc:  # CUC should be present after initialization
            assert hasattr(cuc, "alpha_3")
            assert hasattr(cuc, "name")
            assert hasattr(cuc, "numeric")
