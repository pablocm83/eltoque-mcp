# Created By  : PabloCM83


from typing import Any, cast

from pycountry import currencies as pcurrencies
from pycountry.db import Database

from eltoque_mcp.ext.pycountry.db import Currency

__all__ = ["Currencies", "Currency", "currencies"]


class Currencies(Database[Currency]):
    def add_entry(self, *, alpha_3: str, numeric: str, name: str, **kw: Any) -> None: ...


currencies = cast(Currencies, pcurrencies)
