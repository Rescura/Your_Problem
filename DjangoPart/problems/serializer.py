from rest_framework import serializers
from .models import ProblemsModel, ReplyModel

class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemsModel # 모델 설정
        fields = ('id', 'problemTitle', 'problemAuthor', 'problemTime', 'problemContent') # 필드 설정


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyModel # 모델 설정
        fields = ('id', 'problemId', 'replyTitle', 'replyTime', 'replyAuthor', 'replyContent') # 필드 설정

