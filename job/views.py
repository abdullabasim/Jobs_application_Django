from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.db.models import Avg , Min,Max,Count
from .models import Job ,CandidatesApplied
from .serializersData import SerializerJob, SerializerCandidatesApplied
from django.shortcuts import get_object_or_404
from rest_framework import  status
from .filters import JobsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.views import APIView
# Create your views here.


class jobList(APIView):

    def get(self,request):
        filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
        count = filterset.qs.count()

        resPerPage = 30
        paginator = PageNumberPagination()
        paginator.page_size = resPerPage

        queryset = paginator.paginate_queryset(filterset.qs, request)

        serializer = SerializerJob(queryset, many=True)
        return Response({
            'count': count,
            'resPerPage': resPerPage,
            'jobs': serializer.data
        })

    @permission_classes([IsAuthenticated])
    def post(self,request):
        request.data['user'] = request.user
        serializer = SerializerJob(data=request.data, many=False)
        return Response(serializer.data)

class jobDetail(APIView) :
    def get_job_object(self, pk):
            job = get_object_or_404(Job, id=pk)

            return job

    def get(self,request,pk):
        serializer = SerializerJob(self.get_job_object(pk), many=False)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        job = self.get_job_object(pk)

        if job.user != request.user:
            return Response({
                "message": "You can not update this job"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = SerializerJob(job, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    @permission_classes([IsAuthenticated])
    def delete(self,request,pk):
        job = self.get_job_object(pk)
        if job.user != request.user:
            return Response({
                "message": "You can not delete this job"
            }, status=status.HTTP_403_FORBIDDEN)
        job.delete()

        return Response({'message': 'Job is deleted!'}, status=status.HTTP_200_OK)




@api_view(['GET'])
def getTopicStats(request,topic):

   args = {"title__icontains" : topic}

   jobs = Job.objects.filter(**args)

   if len(jobs) == 0 :
       return Response({'message': f'There no stat found for {topic}'.format(topic=topic)})


   stats = jobs.aggregate(
       total_jobs = Count('title'),
       avg_positions = Avg ('positions'),
       avg_salary=Avg('salary'),
       min_salary=Min('salary'),
       max_salary=Max('salary'),
   )

   return Response(stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyToJob(request,pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    if user.userprofile.resume == '' :
        return Response({
            "error": "You should upload resume first"
        }, status=status.HTTP_400_BAD_REQUEST)

    if job.lastDate < timezone.now() :
        return Response({
            "error": "Job is expired"
        }, status=status.HTTP_400_BAD_REQUEST)

    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()

    if alreadyApplied :
        return Response({
            "error": "You have already applied for this Job"
        }, status=status.HTTP_400_BAD_REQUEST)

    jobApplied = CandidatesApplied.objects.create(
        job=job,
        user=user,
        resume = user.userprofile.resume
    )

    return Response({
        'message' : 'Applied done'
    },status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserAppliedJobs(request):

    args = {'user_id' : request.user.id}

    jobs = CandidatesApplied.objects.filter(**args)

    serializer = SerializerCandidatesApplied(jobs,many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isApplied(request,pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    applied = job.candidatesapplied_set.filter(user=user).exists()

    return Response(applied)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserJobs(request):

    args = {'user' : request.user.id}
    jobs = Job.objects.filter(**args)
    serializer = SerializerJob(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidateApplied(request,pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    if job.user != user :
        return Response({
            'message': 'You can not access this job'
        }, status=status.HTTP_403_FORBIDDEN)

    candidates = job.candidatesapplied_set.all()

    serializer = SerializerCandidatesApplied(candidates, many=True)

    return Response(serializer.data)