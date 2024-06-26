from django.conf import settings 
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from fairy_tairy.permissions import *
from diaries.models import Diary
from .models import *
from .serializers import *

import requests
import time

def request_emotion(content):
    """
    일기 내용으로 emootion label 검출
    """
    flask_url = f'http://{settings.FLASK_URL}:5000/get_sentiment'
    try:
        
        response = requests.post(flask_url, json={'content': content},verify=False, timeout=50)

        if response.status_code == 200:
            response_data = response.json()
            emotion_label = response_data['emotion_label']
            print("Received emotion_label:", emotion_label)
            time.sleep(2)
            
            return emotion_label
        
        else:
            print("Failed to get emotion from Flask:", response.status_code)
            
            return None
    
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        
        return None

def request_comment(content):
    """
    일기 내용으로 응원 문구 생성
    """
    flask_url = f'http://{settings.FLASK_URL}:5000/get_comment'
    try:
        
        response = requests.post(flask_url, json={'content': content},verify=False, timeout=50)

        if response.status_code == 200:
            response_data = response.json()
            comment = response_data['comment']
            print("Received comment:", comment)
            time.sleep(2)
            
            return comment
        
        else:
            print("Failed to get comment from Flask:", response.status_code)
            
            return None
    
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        
        return None
    
class EmotionViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionSerializer
    queryset = Emotion.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(diary__user=self.request.user)
        
        return super().filter_queryset(queryset)
    
    
    def list(self, request, *args, **kwargs):
        """
        emmtion_list 내가 작성한 일기의 감정라벨, 응원문구 목록 조회 API
        
        ---
        
        """
        return super().list(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        """
        emotion_delete 감정라벨, 응원문구 삭제하는 API
        
        ---
        
        """
        return super().destroy(request, *args, **kwargs)
    
    

    def create(self, request, *args, **kwargs):
        """
        emotion_create 일기 내용으로 감정라벨, 응원문구 생성 하는 API
        
        ---
        ## 예시 request:
        
            {
                'diary' : 2
            }
            
        ## 예시 response:
        
            200
            {
                "id": 2,
                "emotion_label": "불안",
                "emotion_prompt": "",
                "chat": " 이별은 사실일지도 모르겠어요 ",
                "diary": 2
            }
            
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diary = serializer.validated_data.get('diary')

        if diary.user != request.user:
            return Response({'error': "Diary does not belong to the current user."}, status=status.HTTP_400_BAD_REQUEST)

        chat = request_comment(diary.content)
        label = request_emotion(diary.content)
        
        existing_emotion = Emotion.objects.filter(diary=diary).first()
        if existing_emotion:
            serializer = self.get_serializer(existing_emotion, data={'chat': chat, 'emotion_label': label}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(diary=diary, chat=chat, emotion_label = label)
            
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(diary=diary, chat=chat, emotion_label = label)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

    # def update(self, request, *args, **kwargs):
    #     """
    #     emotion_update 일기 내용으로 감정라벨, 응원문구 업데이트 하는 API
        
    #     ---
        
    #     ### id : emotoio의  ID
        
        
    #     ## 예시 request:
        
    #         {
    #             'diary' : 2
    #         }
            
    #     ## 예시 response:
        
    #         200
    #         {
    #             "id": 2,
    #             "emotion_label": "불안",
    #             "emotion_prompt": "",
    #             "chat": " 이별은 사실일지도 모르겠어요 ",
    #             "diary": 2
    #         }
            
    #     """
    #     instance = self.get_object()  # 기존 Emotion 객체 가져오기
    #     diary = get_object_or_404(Diary, id=instance.diary.id, user=request.user)
        
    #     chat = request_comment(diary.content)
    #     label = request_emotion(diary.content)
        
    #     serializer = self.get_serializer(instance, data=request.data,chat=chat, emotion_label = label)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
       
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     emotion_partial_update 일기 내용으로 감정라벨, 응원문구 업데이트 하는 API
        
    #     ---
        
    #     """
    #     return super().partial_update(request, *args, **kwargs)
    