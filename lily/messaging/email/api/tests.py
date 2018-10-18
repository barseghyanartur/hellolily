from lily.tests.utils import GenericAPITestCase
from lily.messaging.email.factories import EmailDraftMessageFactory
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

    def _extra_create_object_kwargs(self):
        """
        Adds owner of emails as a keyword argument of create_batch called
        in create object to make sure that we have access to the created emails.
        """
        return dict(
            send_from__owner=self.user_obj
        )

    def test_update_object_unauthenticated(self):
        """
        Test that an unauthenticated user doesn't have the access to update an object.
        """
        set_current_user(self.user_obj)
        db_obj = self._create_object()
        stub_dict = self._create_object_stub()

        print(db_obj)
        print(self.get_url(self.detail_url, kwargs={'pk': db_obj.pk}))

        request = self.anonymous_user.put(self.get_url(self.detail_url, kwargs={'pk': db_obj.pk}), stub_dict)

        self.assertStatus(request, status.HTTP_403_FORBIDDEN, stub_dict)
        self.assertEqual(request.data, {u'detail': u'Authentication credentials were not provided.'})

    def test_get_list_authenticated(self):
        """
        Test that the list returns normally when the user is properly authenticated.
        """
        set_current_user(self.user_obj)
        obj_list = self._create_object(size=3)

        request = self.user.get(self.get_url(self.list_url))

        self.assertStatus(request, status.HTTP_200_OK)
        self.assertEqual(len(obj_list), len(request.data.get('results')))

        for i, db_obj in enumerate(reversed(obj_list)):
            api_obj = request.data.get('results')[i]
            self._compare_objects(db_obj, api_obj)

