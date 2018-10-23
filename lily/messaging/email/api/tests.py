import json

from lily.tests.utils import GenericAPITestCase
from lily.messaging.email.factories import EmailDraftFactory, EmailAccountFactory, EmailMessageFactory
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

    def _create_object_stub(self, size=1, action=None, with_send_from=True, with_message=False, **kwargs):
        object_list = super(DraftEmailTests, self)._create_object_stub(size, force_to_list=True, **kwargs)

        for obj in object_list:
            obj['action'] = 'compose'  # 'compose' is the default
            if action is not None:
                obj['action'] = action

            account = EmailAccountFactory(
                owner=self.user_obj, tenant=self.user_obj.tenant
            )

            obj['send_from'] = None
            if with_send_from:
                obj['send_from'] = account.id

            if with_message:
                obj['message'] = EmailMessageFactory.create(account=account).id

        if size == 1:
            return object_list[0]

        return object_list

    def _extra_create_object_kwargs(self):
        """
        Adds owner of emails as a default keyword argument of create_batch
        called in create object to make sure that we have access to the
        created emails.
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

    def _test_create_action_object(self, action, with_send_from=True, with_message=False, should_succeed=True):
        """
        This helper function tests the basic create functionality with the
        passed action.
        """
        set_current_user(self.user_obj)
        stub_dict = self._create_object_stub(
            action=action,
            with_send_from=with_send_from,
            with_message=with_message
        )

        request = self.user.post(self.get_url(self.list_url), stub_dict)

        status_code = status.HTTP_400_BAD_REQUEST
        if should_succeed:
            status_code = status.HTTP_201_CREATED

        self.assertStatus(request, status_code, stub_dict)

        if should_succeed:
            created_id = json.loads(request.content).get('id')
            self.assertIsNotNone(created_id)

            db_obj = self.model_cls.objects.get(pk=created_id)
            self._compare_objects(db_obj, json.loads(request.content))

    def test_create_compose_object(self):
        """
        Test that creating an email with action 'compose' is possible.
        """
        self._test_create_action_object('compose')

    def test_create_compose_object_with_message(self):
        """
        Test that creating an email with a message and action 'compose' is
        not possible.
        """
        self._test_create_action_object('compose', with_message=True, should_succeed=False)

    def test_create_compose_object_without_send_from(self):
        """
        Test that creating an email without send_from and with action 'compose'
        is not possible.
        """
        self._test_create_action_object('compose', with_send_from=False, should_succeed=False)

    def test_get_list_tenant_filter(self):
        """
        Test that users from different tenants can't access each other's data.
        """
        set_current_user(self.other_tenant_user_obj)

        other_tenant_obj_list = self._create_object(
            size=3,
            send_from__owner=self.other_tenant_user_obj,
            tenant=self.other_tenant_user_obj.tenant
        )

        set_current_user(self.user_obj)
        self._create_object(size=3)

        set_current_user(None)

        request = self.other_tenant_user.get(self.get_url(self.list_url))
        self.assertStatus(request, status.HTTP_200_OK)
        self.assertEqual(len(other_tenant_obj_list), len(request.data.get('results')))

        for i, db_obj in enumerate(reversed(other_tenant_obj_list)):
            self._compare_objects(db_obj, request.data.get('results')[i])
