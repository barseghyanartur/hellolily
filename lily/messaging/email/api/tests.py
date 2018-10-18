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

    #def _create_object_stub(self, **kwargs):
    #    object_list = self.factory_cls.stub_batch(1, **kwargs)

    #    for obj in object_list:
    #        print(obj)

    def _create_object(self, with_relations=False, size=1, **kwargs):
        """
        Default implentation for the creation of objects, this doesn't do anything with relations other than
        what the factory does by default..
        """
        # Set a default tenant of the user.
        kwargs['tenant'] = self.user_obj.tenant if not kwargs.get('tenant') else kwargs['tenant']

        object_list = self.factory_cls.create_batch(size=size, **kwargs)

        if size > 1:
            return object_list
        else:
            # If required size is 1, just give the object instead of a list.
            return object_list[0]


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
