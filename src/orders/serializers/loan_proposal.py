from rest_framework import serializers
from orders.models import LoanProposal
from .customer import CustomerSerializer

class LoanProposalSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = LoanProposal
        fields = ["id", "customer", "amount", "status", "created_at"]