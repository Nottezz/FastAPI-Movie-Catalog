from unittest import TestCase

from movie_catalog.api.api_v1.auth.services import redis_tokens


class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        self.assertTrue(redis_tokens.token_exists(new_token))
