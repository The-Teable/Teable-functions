from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from .models import FilteringResultProductMap, FilteringResults, Questionnaires, Teas, Users, SurveyResults, SurveyResults2
from .lib import filtering_algorithm
import json

class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teas
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'age', 'gender', 'tel', 'address', 'email']
    def create(self, validated_data):
        validated_data['create_date'] = datetime.now()
        return super().create(validated_data)
        
class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResults
        fields = ['survey_responses']
    def create(self, validated_data):
        query_params = self.context['request'].query_params
        user_id = query_params.get('userId')
        version = query_params.get('version')
        print(user_id, version, not(version), not(user_id))
        if (not user_id) or (not version):
            raise serializers.ValidationError('Params not provided enough')
        validated_data['user_id'] = user_id
        validated_data['questionnaire_id'] = version
        validated_data['create_date'] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        survey_id = self.context['request'].query_params.get('surveyId')
        if not survey_id:
            raise serializers.ValidationError('Params not provided enough')
        validated_data['survey_id'] = survey_id
        validated_data['update_date'] = datetime.now()
        return super().update(instance, validated_data)
        
class SurveyResult2Serializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResults2
        fields = ['survey_responses']
    def create(self, validated_data):
        query_params = self.context['request'].query_params
        user_id = query_params.get('userId')
        version = query_params.get('version')
        print(user_id, version, not(version), not(user_id))
        if (not user_id) or (not version):
            raise serializers.ValidationError('Params not provided enough')
        validated_data['user_id'] = user_id
        validated_data['questionnaire_id'] = version
        validated_data['create_date'] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        survey_id = self.context['request'].query_params.get('surveyId')
        if not survey_id:
            raise serializers.ValidationError('Params not provided enough')
        validated_data['survey_id'] = survey_id
        validated_data['update_date'] = datetime.now()
        return super().update(instance, validated_data)

class QuestionnairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaires
        fields = '__all__'

class FilteringResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilteringResults
        fields = []
        
    def create(self, validated_data):
        query_params = self.context['request'].query_params
        survey_id = query_params.get('surveyId')
        if not survey_id:
            raise serializers.ValidationError('Params not provided enough')
        survey_result = SurveyResults.objects.filter(id=survey_id)
        if len(survey_result) < 1:
            raise serializers.ValidationError('There is no corresponding survey result')
        survey_response = json.loads(survey_result[0].survey_responses.replace("'", "\""))
        if 'type' not in survey_response or 'flavor' not in survey_response or 'expect' not in survey_response or 'caffeine' not in survey_response:
            raise serializers.ValidationError('Survey response not answered enough')
        tea_type = survey_response['type']
        tea_flavor = survey_response['flavor']
        tea_expect = survey_response['expect']
        tea_caffeine = survey_response['caffeine']
        algorithm_result_str = filtering_algorithm.tea_filtering(''.join(tea_type), ''.join(tea_flavor), ''.join(tea_expect), tea_caffeine).to_json(orient = 'records', force_ascii = False)
        algorithm_result_json = json.loads(algorithm_result_str)
        validated_data['survey_result_id'] = survey_result[0].id
        validated_data['create_date'] = datetime.now()
        created_instance = super().create(validated_data)
        filtering_result_id = created_instance.id
        teas = []
        for tea in algorithm_result_json:
            tea_db = Teas.objects.filter(brand=tea['브랜드'], name=tea['제품 이름'])
            if len(tea_db) < 1:
                raise serializers.ValidationError('There is no corresponding tea info')
            teas.append(tea_db[0])
            FilteringResultProductMap.objects.create(filtering_result_id=filtering_result_id, tea_id=tea_db[0].id, create_date=datetime.now())
        return created_instance