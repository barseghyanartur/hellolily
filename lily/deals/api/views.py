from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lily.api.filters import ElasticSearchFilter
from lily.api.mixins import ModelChangesMixin, TimeLogMixin, DataExistsMixin

from .serializers import (DealSerializer, DealNextStepSerializer, DealWhyCustomerSerializer, DealWhyLostSerializer,
                          DealFoundThroughSerializer, DealContactedBySerializer, DealStatusSerializer)
from ..models import Deal, DealNextStep, DealWhyCustomer, DealWhyLost, DealFoundThrough, DealContactedBy, DealStatus


class DealContactedByList(APIView):
    swagger_schema = None

    def get(self, request, format=None):
        return Response(Deal.CONTACTED_BY_CHOICES)


class DealNextStepList(APIView):
    model = DealNextStep
    serializer_class = DealNextStepSerializer
    swagger_schema = None

    def get(self, request, format=None):
        queryset = self.model.objects.filter(tenant_id=self.request.user.tenant_id)
        serializer = DealNextStepSerializer(queryset, many=True)
        return Response(serializer.data)


class DealWhyCustomerViewSet(ModelViewSet):
    # Set the queryset, this takes care of setting the `base_name`.
    queryset = DealWhyCustomer.objects
    # Set the serializer class for this viewset.
    serializer_class = DealWhyCustomerSerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealWhyCustomerViewSet, self).get_queryset().all()


class DealWhyLostViewSet(ModelViewSet):
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = DealWhyLost.objects
    serializer_class = DealWhyLostSerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealWhyLostViewSet, self).get_queryset().all()


class DealNextStepViewSet(ModelViewSet):
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = DealNextStep.objects
    # Set the serializer class for this viewset.
    serializer_class = DealNextStepSerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealNextStepViewSet, self).get_queryset().all()


class DealFoundThroughViewSet(ModelViewSet):
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = DealFoundThrough.objects
    # Set the serializer class for this viewset.
    serializer_class = DealFoundThroughSerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealFoundThroughViewSet, self).get_queryset().all()


class DealContactedByViewSet(ModelViewSet):
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = DealContactedBy.objects
    # Set the serializer class for this viewset.
    serializer_class = DealContactedBySerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealContactedByViewSet, self).get_queryset().all()


class DealStatusViewSet(ModelViewSet):
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = DealStatus.objects
    # Set the serializer class for this viewset.
    serializer_class = DealStatusSerializer
    swagger_schema = None

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealStatusViewSet, self).get_queryset().all()


class DealFilter(filters.FilterSet):
    class Meta:
        model = Deal
        fields = {
            'account': ['exact', ],
            'amount_once': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'amount_recurring': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'assigned_to': ['exact', ],
            'card_sent': ['exact', ],
            'closed_date': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'contacted_by': ['exact', ],
            'created': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'currency': ['exact', ],
            'found_through': ['exact', ],
            'is_checked': ['exact', ],
            'modified': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'name': ['exact', ],
            'new_business': ['exact', ],
            'next_step': ['exact', ],
            'next_step_date': ['exact', 'lt', 'lte', 'gt', 'gte', ],
            'quote_id': ['exact', ],
            'status': ['exact', ],
            'twitter_checked': ['exact', ],
            'why_customer': ['exact', ],
            'why_lost': ['exact', ],
        }


class DealViewSet(ModelChangesMixin, TimeLogMixin, DataExistsMixin, ModelViewSet):
    """
    retrieve:
    Returns the given deal.

    list:
    Returns a list of all deals.

    create:
    Creates a new deal.

    update:
    Overwrites the whole deal with the given data.

    > Note: Next step date is automatically incremented based on the next step unless the next step is 'None'.

    partial_update:
    Updates just the fields in the request data of the given deal.

    > Note: Next step date is automatically incremented based on the next step unless the next step is 'None'.

    delete:
    Deletes the given deal.

    changes:
    Returns all the changes performed on the given deal.

    timelogs:
    Returns all timelogs for the given deal.
    """
    # Set the queryset, without .all() this filters on the tenant and takes care of setting the `base_name`.
    queryset = Deal.objects
    # Set the serializer class for this viewset.
    serializer_class = DealSerializer
    # Set all filter backends that this viewset uses.
    filter_backends = (ElasticSearchFilter, OrderingFilter, filters.DjangoFilterBackend, )

    # ElasticSearchFilter: set the model type.
    model_type = 'deals_deal'
    # OrderingFilter: set all possible fields to order by.
    ordering_fields = ('id', )
    # OrderingFilter: set the default ordering fields.
    ordering = ('id', )
    # DjangoFilter: set the filter class.
    filter_class = DealFilter

    def get_queryset(self):
        """
        Set the queryset here so it filters on tenant and works with pagination.
        """
        return super(DealViewSet, self).get_queryset().filter(is_deleted=False)
