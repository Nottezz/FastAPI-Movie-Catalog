from movie_catalog.api.api_v1.movie_catalog.dependencies import UNSAFE_METHOD


class TestUnsafeMethods:
    def test_doesnt_contain_safe_methods(self) -> None:
        safe_methods = {
            "GET",
            "HEAD",
            "OPTIONS",
        }
        assert not UNSAFE_METHOD & safe_methods

    def test_all_methods_are_upper(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHOD)
