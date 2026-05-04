# Created By  : PabloCM83

import pytest
from pydantic import BaseModel, ValidationError

from eltoque_mcp.ext.pydantic_extra_types.currency_code import ISO4217Plus


class TestISO4217Plus:
    """Test suite for ISO4217Plus currency validation."""

    def test_valid_standard_currency_code(self):
        """Test validation of standard ISO 4217 currency codes."""

        class Model(BaseModel):
            currency: ISO4217Plus

        model = Model(currency=ISO4217Plus("USD"))
        assert model.currency == "USD"

    def test_valid_lowercase_currency_code(self):
        """Test that lowercase currency codes are converted to uppercase."""

        class Model(BaseModel):
            currency: ISO4217Plus

        model = Model(currency=ISO4217Plus("usd"))
        assert model.currency == "USD"

    def test_valid_cuban_custom_currencies(self):
        """Test validation of custom Cuban currency codes."""

        class Model(BaseModel):
            currency: ISO4217Plus

        for code in ["CUC", "CLA", "MLC"]:
            model = Model(currency=ISO4217Plus(code))
            assert model.currency == code

    def test_valid_various_iso4217_currencies(self):
        """Test various valid ISO 4217 currency codes."""
        valid_codes = ["EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CUP", "MXN"]

        class Model(BaseModel):
            currency: ISO4217Plus

        for code in valid_codes:
            model = Model(currency=ISO4217Plus(code))
            assert model.currency == code

    def test_invalid_currency_code(self):
        """Test that invalid currency codes raise ValidationError."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError) as exc_info:
            Model(currency=ISO4217Plus("XYZ"))

        assert "InvalidCurrency" in str(exc_info.value)

    def test_invalid_too_short_code(self):
        """Test that currency codes shorter than 3 characters are invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus("US"))

    def test_invalid_too_long_code(self):
        """Test that currency codes longer than 3 characters are invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus("USDA"))

    def test_invalid_with_numbers(self):
        """Test that currency codes with numbers are invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus("US1"))

    def test_invalid_with_special_characters(self):
        """Test that currency codes with special characters are invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus("US-D"))

    def test_string_validation_through_pydantic(self):
        """Test string validation occurs through Pydantic automatically."""

        class Model(BaseModel):
            currency: ISO4217Plus

        model = Model(currency=ISO4217Plus("usd"))
        assert model.currency == "USD"

    def test_allowed_currencies_set_not_empty(self):
        """Test that allowed_currencies set is populated."""
        assert len(ISO4217Plus.allowed_currencies) > 0

    def test_allowed_currencies_includes_standard_codes(self):
        """Test that standard currency codes are in allowed list."""
        assert "USD" in ISO4217Plus.allowed_currencies
        assert "EUR" in ISO4217Plus.allowed_currencies
        assert "GBP" in ISO4217Plus.allowed_currencies

    def test_allowed_currencies_includes_custom_cuban_codes(self):
        """Test that custom Cuban codes are in allowed list."""
        assert "CUC" in ISO4217Plus.allowed_currencies
        assert "CLA" in ISO4217Plus.allowed_currencies
        assert "MLC" in ISO4217Plus.allowed_currencies

    def test_iso4217plus_is_string_subclass(self):
        """Test that ISO4217Plus is a subclass of str."""
        assert issubclass(ISO4217Plus, str)

    def test_pydantic_json_schema_generation(self):
        """Test JSON schema generation for ISO4217Plus."""

        class Model(BaseModel):
            currency: ISO4217Plus

        schema = Model.model_json_schema()
        assert "properties" in schema
        assert "currency" in schema["properties"]
        assert "enum" in schema["properties"]["currency"]

    def test_pydantic_json_schema_includes_cuban_currencies(self):
        """Test that JSON schema includes custom Cuban currencies."""

        class Model(BaseModel):
            currency: ISO4217Plus

        schema = Model.model_json_schema()
        enum_values = schema["properties"]["currency"]["enum"]
        assert "CUC" in enum_values
        assert "CLA" in enum_values
        assert "MLC" in enum_values

    def test_model_serialization(self):
        """Test model serialization with ISO4217Plus."""

        class Model(BaseModel):
            currency: ISO4217Plus

        model = Model(currency=ISO4217Plus("usd"))
        json_str = model.model_dump_json()
        assert "USD" in json_str

    def test_model_deserialization(self):
        """Test model deserialization with ISO4217Plus."""

        class Model(BaseModel):
            currency: ISO4217Plus

        data = '{"currency": "EUR"}'
        model = Model.model_validate_json(data)
        assert model.currency == "EUR"

    def test_model_deserialization_with_lowercase(self):
        """Test model deserialization with lowercase currency code."""

        class Model(BaseModel):
            currency: ISO4217Plus

        data = '{"currency": "gbp"}'
        model = Model.model_validate_json(data)
        assert model.currency == "GBP"

    def test_empty_string_invalid(self):
        """Test that empty string is invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus(""))

    def test_whitespace_invalid(self):
        """Test that whitespace is invalid."""

        class Model(BaseModel):
            currency: ISO4217Plus

        with pytest.raises(ValidationError):
            Model(currency=ISO4217Plus("   "))
