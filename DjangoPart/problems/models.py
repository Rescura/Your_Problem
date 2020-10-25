from django.db import models

# 고민 정보를 담고 있는 모델(ID(생략됨), 제목, 생성시각, 게시자이름, 고민내용)
class ProblemsModel(models.Model):
    problemTitle = models.CharField('problemTitle', max_length=100, blank=False, null=False)
    problemTime = models.DateTimeField('problemTime', auto_now_add=True)
    problemAuthor = models.CharField('problemAuthor', max_length=50, blank=False, null=False)
    problemContent = models.TextField('problemContent', blank=False, null=False)

    # 고민 목록을 요청했을때 간단한 정보(제목, 게시자이름, 텍스트50자)를 돌려주는 함수
    #def info(self):
    #    return {
    #        'problemTitle' : self.problemTitle,
    #        'problemTime' : self.problemTime,
    #    }

    def __str__(self):
        return self.problemTitle

# 답변 정보를 담고 있는 모델(답변ID(생략됨), 고민ID, 답변시각, 게시자이름, 답변내용)
class ReplyModel(models.Model):
    problemId = models.ForeignKey(ProblemsModel, on_delete=models.CASCADE)
    replyTitle = models.CharField('replyTitle', max_length=50, blank=False, null=False)
    replyTime = models.DateTimeField('replyTime', auto_now_add=True)
    replyAuthor = models.CharField('replyAuthor', max_length=50, blank=False, null=False)
    replyContent = models.TextField('replyText', blank=False, null=False)


