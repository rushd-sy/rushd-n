from pydantic import ValidationError
import pytest
from task_03_1 import User

class TestUserModel:

    def test__invalid_name_too_short(self):
        with pytest.raises(ValidationError) as err:
            user = User(  # noqa: F841
                name='b',
                email='m@',
                age=14
            )
            assert 'at least 2' in str(err)

    def test__invalid_name_int(self):
        with pytest.raises(ValidationError) as err:
            user = User(  # noqa: F841
                name=123, # type: ignore
                email='m@',
                age=14
            )
            assert 'must be str' in str(err)

    def test_invalid_age_too_young(self):
        with pytest.raises(ValidationError) as err:
            user = User(  # noqa: F841
                name='Bitar',
                email='m@',
                age=12
            )
            assert 'age at least 13' in str(err)

    def test_invalid_age_too_old(self):
        with pytest.raises(ValidationError) as err:
            user = User(  # noqa: F841
                name='Bitar',
                email='m@',
                age=200
            )
            assert 'age at most 120' in str(err)
    

    def test_invalid_email_no_at_symbol(self):
        with pytest.raises(ValidationError) as err:
            user = User(  # noqa: F841
                name='Bitar',
                email='m',
                age=21
            )
            assert 'name must have @' in str(err)
    