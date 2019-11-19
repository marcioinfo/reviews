# THIRD PARTY IMPORTS
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

# PROJECT IMPORTS
from reviews.models import Review
from reviews.serializers import ReviewSerializer, DetailedReviewSerializer

from commons.views import CustomAPIView


class ReviewView(CustomAPIView):

    def get(self, request):
        """
        Retrieve all reviews from the authenticated user.
        ---

        **Response Json:** (Many)

            [{
              "rating": 4,
              "title": "Review Title",
              "summary": "The Review Summary/Description",
              "company_name": "Company Name that was being reviewed",
              "submission_date": "Date that the submission was made"
            }]
        """

        user_id = self.authenticate(request)

        reviews = Review.objects.filter(reviewer=user_id
                                        ).order_by('-submission_date')

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):

        """
        Register a new review from an authenticated user.
        ---

        **Request Json:** (Single)

            {
              "rating": 4,
              "title": "Review Title",
              "summary": "The Review Summary/Description",
              "company_name": "Company Name that is being reviewed"
            }
        """

        user_id = self.authenticate(request)

        data = request.data
        data['reviewer'] = user_id
        data['ip_address'] = self.request_ip(request)

        serializer = DetailedReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Your Review was stored!"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
