from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from orders.models import Order, OrderStatusHistory
from orders.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer").prefetch_related("items__product", "status_history").all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        notes = request.data.get("notes", "")

        if new_status:
            previous_status = order.status
            order.status = new_status
            order.save()

            OrderStatusHistory.objects.create(
                order=order,
                previous_status=previous_status,
                new_status=new_status,
                changed_by=request.user if request.user.is_authenticated else None,
                notes=notes
            )

            return Response({"status": order.status}, status=status.HTTP_200_OK)

        return Response({"error": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST)