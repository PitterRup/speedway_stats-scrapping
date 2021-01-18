from unittest import mock

import pytest
from marshmallow import Schema, fields

from api.util.marshmallow_tools import validate_ma


class FakeSchema(Schema):
    attr = fields.String(required=True)


class FakeFlaskG():
    req_para = {}


class FakeFlaskRequest():
    def __init__(self, post_para):
        self.values = post_para


@pytest.mark.parametrize('post_para, errors', [
    (dict(attr=u'ok'), False),
    (dict(attr=123), True),
    (dict(attr2=u'val'), True),
])
def test_validate_ma(post_para, errors):
    # given
    fake_g = FakeFlaskG()
    fake_request = FakeFlaskRequest(post_para)

    @validate_ma(FakeSchema)
    def fake_resource():
        para = fake_g.req_para
        return para

    # when
    with mock.patch('api.util.marshmallow_tools.g', fake_g), mock.patch('api.util.marshmallow_tools.request', fake_request):  # noqa: E501
        response = fake_resource()
        if errors:
            'errors' in 'response'
        else:
            assert response == post_para
