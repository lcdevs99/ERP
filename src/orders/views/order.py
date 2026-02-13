import logging
import uuid

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects
        .select_related("customer")
        .prefetch_related("items__product", "status_history")
        .all()
    )
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    filterset_fields = ["status", "customer"]
    ordering_fields = ["created_at", "total_value"]

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

        logger.info(
            "Starting order status update",
            extra={
                "correlation_id": correlation_id,
                "order_id": pk,
                "user": request.user.id if request.user.is_authenticated else None,
                "payload": request.data,
            },
        )

        try:
            order = self.get_object()

            serializer = self.get_serializer(
                order,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info(
                "Order status updated successfully",
                extra={
                    "correlation_id": correlation_id,
                    "order_id": order.id,
                    "new_status": serializer.data.get("status"),
                },
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exc:
            logger.error(
                "Error updating order status",
                extra={
                    "correlation_id": correlation_id,
                    "order_id": pk,
                    "error": str(exc),
                },
                exc_info=True,
            )
            raise
