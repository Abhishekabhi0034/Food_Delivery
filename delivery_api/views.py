from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pricing
from .serializers import PricingSerializer

class PriceCalculatorAPI(APIView):
    def post(self, request):
        zone = request.data.get('zone')
        organization_id = request.data.get('organization_id')
        total_distance = request.data.get('total_distance')
        item_type = request.data.get('item_type')

        try:
            pricing = Pricing.objects.get(
                organization_id=organization_id,
                zone=zone,
                item__type=item_type
            )
            base_distance = pricing.base_distance_in_km
            base_price = pricing.fix_price
            km_price = pricing.km_price

            if total_distance <= base_distance:
                total_price = base_price
            else:
                extra_distance = total_distance - base_distance
                total_price = base_price + extra_distance * km_price

            return Response({'total_price': total_price}, status=status.HTTP_200_OK)
        except Pricing.DoesNotExist:
            return Response({'error': 'Pricing not found for the given criteria'}, status=status.HTTP_400_BAD_REQUEST)
