from rest_framework import viewsets
from orders.models import LoanProposal
from orders.serializers import LoanProposalSerializer

class LoanProposalViewSet(viewsets.ModelViewSet):
    queryset = LoanProposal.objects.select_related("customer").all()
    serializer_class = LoanProposalSerializer