# THIRD PARTY LIBRARIES
from rest_framework import serializers

# PROJECT LIBRARIES
#from reviews.models import Review
from models.models import Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('rating', 'title',
                  'summary', 'company_name',
                  'submission_date')


class DetailedReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('rating', 'title',
                  'summary', 'company_name',
                  'submission_date', 'reviewer',
                  'ip_address')
