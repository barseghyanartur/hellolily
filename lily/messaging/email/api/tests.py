from lily.tests.utils import GenericAPITestCase
from lily.messaging.email.factories import EmailDraftMessageFactory, EmailAccountFactory
from lily.messaging.email.models.models import EmailDraftMessage
from lily.messaging.email.api.serializers import EmailDraftMessageReadSerializer
from lily.tenant.middleware import set_current_user
from rest_framework import status


class DraftEmailTests(GenericAPITestCase):
    """
    Class containing tests for the drafts email API.
    """

    list_url = 'emaildraftmessage-list'
    detail_url = 'emaildraftmessage-detail'
    factory_cls = EmailDraftMessageFactory
    model_cls = EmailDraftMessage
    serializer_cls = EmailDraftMessageReadSerializer

    def _create_object_stub(self, size=1, **kwargs):
        object_list = super(DraftEmailTests, self)._create_object_stub(size, force_to_list=True, **kwargs)

        for obj in object_list:
            obj['send_from'] = EmailAccountFactory(owner=self.user_obj, tenant=self.user_obj.tenant).__dict__
            del obj['send_from']['_state']
            del obj['send_from']['_tenant_']

        return object_list

    def _extra_create_object_kwargs(self):
        """
        Adds owner of emails as a keyword argument of create_batch called
        in create object to make sure that we have access to the created emails.
        """
        return dict(
            send_from__owner=self.user_obj
        )

    def test_create_object_authenticated(self):
        """
        Test that the object is created normally when the user is properly authenticated.
        """
        set_current_user(self.user_obj)
        stub_dict = self._create_object_stub()

        print(stub_dict)
        print(self.get_url(self.list_url))

        request = self.user.post(self.get_url(self.list_url), stub_dict)
        self.assertStatus(request, status.HTTP_201_CREATED, stub_dict)

        created_id = json.loads(request.content).get('id')
        self.assertIsNotNone(created_id)

        db_obj = self.model_cls.objects.get(pk=created_id)
        self._compare_objects(db_obj, json.loads(request.content))


