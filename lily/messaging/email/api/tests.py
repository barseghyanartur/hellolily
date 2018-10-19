import json

from django.forms.models import model_to_dict

from lily.tests.utils import GenericAPITestCase
from lily.messaging.email.factories import EmailDraftFactory, EmailAccountFactory
from lily.messaging.email.models.models import EmailDraft
from lily.messaging.email.api.serializers import EmailDraftReadSerializer
from lily.tenant.middleware import set_current_user
from rest_framework import status


class DraftEmailTests(GenericAPITestCase):
    """
    Class containing tests for the drafts email API.
    """

    list_url = 'emaildraft-list'
    detail_url = 'emaildraft-detail'
    factory_cls = EmailDraftFactory
    model_cls = EmailDraft
    serializer_cls = EmailDraftReadSerializer

    def _create_object_stub(self, size=1, action=None, **kwargs):
        object_list = super(DraftEmailTests, self)._create_object_stub(size, force_to_list=True, **kwargs)

        for obj in object_list:
            if action is not None:
                obj['action'] = action

            obj['send_from'] = model_to_dict(
                EmailAccountFactory(owner=self.user_obj, tenant=self.user_obj.tenant)
            )

            if action == 'compose':
                obj['send_from'] = obj['send_from']['id']

            print(obj)

        if size == 1:
            return object_list[0]

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
        This test is replaced by 5 other tests, each testing different create
        actions.
        """
        pass

    def test_create_compose_object(self):
        """
        This test is to test if creating an email with action 'compose' works
        as expected.
        """

        set_current_user(self.user_obj)
        stub_dict = self._create_object_stub(action='compose')

        print(self.get_url(self.list_url))

        request = self.user.post(self.get_url(self.list_url), stub_dict)
        self.assertStatus(request, status.HTTP_201_CREATED, stub_dict)

        print(request.content)

        created_id = json.loads(request.content).get('id')
        self.assertIsNotNone(created_id)

        db_obj = self.model_cls.objects.get(pk=created_id)
        self._compare_objects(db_obj, json.loads(request.content))


