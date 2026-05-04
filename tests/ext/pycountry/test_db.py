# Created By  : PabloCM83


class TestDB:
    def test_currency(self):
        from eltoque_mcp.ext.pycountry.db import Currency

        assert Currency.__name__ == "Currency"
        assert Currency.__module__ == "eltoque_mcp.ext.pycountry.db"
        assert Currency.__qualname__ == "Currency"
