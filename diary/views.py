from zoneinfo import ZoneInfo
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View #汎用的なView用の基底クラス
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Page
from .forms import PageForm
class IndexView(LoginRequiredMixin,View):
        # get 日記アプリのトップページにアクセスしたときに動く
        # request(requestObject):ユーザから送られてきたデータを含む
    def get(self, request):
        #render:画面のレスポンスを返す
        datetime_now = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d日 %H:%M:%S")
        return render(
            request, "diary/index.html",{"datetime_now":datetime_now})
    
class PageCreateView(LoginRequiredMixin,View):
    #入力する画面を表示するためのmethod    
    def get(self, request):
        form = PageForm()   
                                                        #diary/page_form.htmlの(from.as_p)に該当
        return render(request, "diary/page_form.html", {"form":form})
    
    #ユーザが保存をおしたら動くmethod
    def post(self, request):
        form = PageForm(request.POST,request.FILES) #POSTにはユーザが入力したデータが含まれている
        if form.is_valid(): #入力項目のバリデーション☑
             form.save()
                #データベースを操作する際、sqlを使わず
                #プログラム内のオブジェクトを操作することで
                #データベースの操作をする技術をORM(オーアールマッパー)という
             return redirect("diary:index")
        return render(request,"diary/page_form.html",{"form":form})        

class PageListView(LoginRequiredMixin,View):
    def get(self, request):
        page_list = Page.objects.order_by("page_date")
        return render(request, "diary/page_list.html",{"page_list":page_list})

class PageDetailView(LoginRequiredMixin,View):
    def get(self,request,id):
        #データベースからIDが一致するPageのデータを取得
        #一致するデータがなければ404を表示
        page = get_object_or_404(Page, id=id)
        return render(request, "diary/page_detail.html",{"page":page})

class PageUpdateView(LoginRequiredMixin,View):
    def get(self,request,id):
        page = get_object_or_404(Page,id=id)
        form = PageForm(instance = page)
        return render(request, "diary/page_update.html",{"form" : form})
    
    def post(self, request, id):
        page = get_object_or_404(Page, id)
        form = PageForm(request.POST,request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("diary:page_detail", id=id)
        return render(request,"diary/page_form.html",{"form":form})

class PageDeleteView(LoginRequiredMixin,View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        return render(request,"diary/page_confirm_delete.html",{"page":page})
    
    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        page.delete()
        return redirect('diary:page_list')
        
            
index = IndexView.as_view()
page_create = PageCreateView.as_view()
page_list = PageListView.as_view()
page_detail = PageDetailView.as_view()
page_update = PageUpdateView.as_view()
page_delete = PageDeleteView.as_view()


