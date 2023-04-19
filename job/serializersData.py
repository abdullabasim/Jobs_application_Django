from rest_framework import serializers
from .models import Job ,CandidatesApplied

class SerializerJob(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'

    def update(self,instance,validated_data):


        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.jobType = validated_data.get('jobType', instance.jobType)
        instance.education = validated_data.get('education', instance.education)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.positions = validated_data.get('positions', instance.positions)
        instance.company = validated_data.get('company', instance.company)
        instance.save()

        return instance


class SerializerCandidatesApplied(serializers.ModelSerializer):
    job = SerializerJob()
    class Meta:
        model = CandidatesApplied
        fields = ['user','job','resume','appliedAt']

