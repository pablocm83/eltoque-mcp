# Created By  : PabloCM83


from collections.abc import Iterable
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

from eltoque_mcp.ext.pycountry import currencies

EXTRA_CURRENCIES = [
    {"alpha_3": "CUC", "name": "Cuban Convertible Peso", "numeric": "931"},
    {"alpha_3": "CLA", "name": "Cuban Clasic Card (USD)", "numeric": "998"},
    {"alpha_3": "MLC", "name": "Freely Convertible Money", "numeric": "931"},
]


def _get_currencies(extras: Iterable[dict[str, str]] = EXTRA_CURRENCIES) -> None:
    for extra in extras:
        currencies.add_entry(**extra)


class ISO4217Plus(str):
    """Currency parses currency subset of the [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) format.
    It include custom cuban currencies like CUC, MLC, etc.
        ```py
        from pydantic import BaseModel

        from eltoque_mcp.ext.pydantic_extra_types.currency_code import ISO4217Plus


        class Currency(BaseModel):
            alpha_3: ISO4217Plus


        cur = Currency(alpha_3='AED')
        print(cur)
        # > alpha_3='AED'
        ```
    """
    _get_currencies()
    allowed_countries_list = [country.alpha_3 for country in currencies]
    allowed_currencies = set(allowed_countries_list)

    @classmethod
    def _validate(cls, currency_code: str, _: core_schema.ValidationInfo) -> str:
        """Validate a subset of the [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        It include custom's cuban currencies like CUC, MLC, etc.

        Args:
            currency_code: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 4217 currency code.

        Raises:
            PydanticCustomError: If the ISO 4217 currency code is not valid or is bond, precious metal or testing code.
        """
        currency_code = currency_code.upper()
        if currency_code not in cls.allowed_currencies:
            raise PydanticCustomError(
                "InvalidCurrency",
                "Invalid currency code."
                " See https://en.wikipedia.org/wiki/ISO_4217 . "
                "Cuban's custom codes are included.",
            )
        return currency_code

    @classmethod
    def __get_pydantic_core_schema__(cls, _: type[Any], __: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the currency subset of the
        [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        It include custom cuban's currencies like CUC, MLC, etc.

        Args:
             _: The source type.
             __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the subset of the currency subset of the
            [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
            It include custom cuban's currencies like CUC, MLC, etc.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with subset of the [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        It include custom cuban's currencies like CUC, MLC, etc.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the subset of the ISO4217 currency code validation. with cuban's currencies.

        """
        json_schema = handler(schema)
        json_schema.update({"enum": cls.allowed_countries_list})
        return json_schema

