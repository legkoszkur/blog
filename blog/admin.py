from django.contrib import admin
from .models import Post, Category,ArticleStatistic,ArticleStatisticAdmin,Comment,CommentReports


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(ArticleStatistic, ArticleStatisticAdmin)
admin.site.register(Comment)
admin.site.register(CommentReports)



