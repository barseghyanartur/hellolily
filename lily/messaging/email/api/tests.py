from lily.tests.utils import GenericAPITestCase
from lily.messaging.email.factories import EmailDraftMessageFactory
from lily.messaging.email.models.models import EmailDraftMessage
from lily.messaging.email.api.serializers import EmailDraftMessageReadSerializer


class DraftEmailTests(GenericAPITestCase):
    """
    Class containing tests for the drafts email API.
    """

    list_url = 'emaildraft-list'
    detail_url = 'emaildraft-detail'
    factory_cls = EmailDraftMessageFactory
    model_cls = EmailDraftMessage
    serializer_cls = EmailDraftMessageReadSerializer

    def _create_object_stub(self, **kwargs):
        object_list = self.factory_cls.stub_batch(1, **kwargs)

        for obj in object_list:
            print(obj)

        self.assertEqual(True, False)

    def test_something(self):
        self.assertEqual(True, False)
