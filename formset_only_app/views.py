from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Item
from .forms import ItemModelFormSet


class ItemCreateOKView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'formset_only_app/ok.html'
    success_url = reverse_lazy('formset_only:ok')

    def get_context_data(self, **kwargs):
        context = super(ItemCreateOKView, self).get_context_data()

        # templateでも扱えるよう、contextにformsetを詰め込んでおく
        if self.request.POST:
            context['items'] = ItemModelFormSet(self.request.POST)
        else:
            context['items'] = ItemModelFormSet(queryset=Item.objects.none())
        return context

    # 継承元のProcessFormViewでform.is_valid()を呼んでおり、これが呼ばれると必ずFalseになってしまう
    # そこで、post〜redirectまでの処理をpost()をオーバーライドして記述する
    # 各メソッドで何をやっているかは、以下を参照しながら読むと分かりやすい
    # https://ccbv.co.uk/projects/Django/1.10/django.views.generic.edit/CreateView/
    def post(self, request, *args, **kwargs):
        # 継承元のBaseCreateViewのpost()でやっている通り、self.objectにNoneをセット
        # https://github.com/django/django/blob/cecc079168e8669138728d31611ff3a1e7eb3a9f/django/views/generic/edit.py#L216
        self.object = None

        # contextよりformsetの値を取得
        # self.objectを設定する前にcontextを取得しようとすると、以下のエラーになるので注意
        # 'ItemCreateOKView' object has no attribute 'object'
        context = self.get_context_data()
        formset = context['items']
        
        # formsetの検証
        if formset.is_valid():
            formset.save()

            # ModelFormMixinのform_valid()でやっている通り、formオブジェクトをself.objectにセット
            # https://github.com/django/django/blob/cecc079168e8669138728d31611ff3a1e7eb3a9f/django/views/generic/edit.py#L158
            self.object = context['form']
            # FormMixinのform_valid()でやっている通り、HttpResponseRedirectを使ってリダイレクト
            # https://github.com/django/django/blob/cecc079168e8669138728d31611ff3a1e7eb3a9f/django/views/generic/edit.py#L75
            return HttpResponseRedirect(self.get_success_url())
        else:
            # formsetの検証でエラーの場合は、form_invalid()に処理を任せる
            # その際に必要なformオブジェクトはcontextより取得する
            return self.form_invalid(context['form'])


class ItemCreateNGView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'formset_only_app/ng.html'
    success_url = reverse_lazy('formset_only:ng')
    
    def get_context_data(self, **kwargs):
        context = super(ItemCreateNGView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = ItemModelFormSet(self.request.POST)
        else:
            context['items'] = ItemModelFormSet(queryset=Item.objects.none())
        return context

    def form_invalid(self, form):
        print('----------form.errors----------\n{}'.format(form.errors))
        print('----------form.data----------\n{}'.format(form.data))
        return super(ItemCreateNGView, self).form_invalid(form)
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['items']

        if formset.is_valid():
            formset.save()
            return super(ItemCreateNGView, self).form_valid(form)
        else:
            return super(ItemCreateNGView, self).form_invalid(form)