# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basket.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    print(request.user)
    basket_items = Basket.objects.filter(user=request.user).order_by('product__country')
    content = {'basket_items': basket_items}
    return render(request, 'basket/basket.html', content)


'''
@login_required
class BasketListView(ListView):
    model = Basket
    template_name = 'basket/basket.html'

    def dispatch(self, *args, **kwargs):
        return super(BasketListView, self).dispatch(*args, **kwargs)
'''


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('catalogue:good', args=[pk]))
    # получить продукт
    product = get_object_or_404(Product, pk=pk)
    # получить пользователя request.user
    # получить такие же продукты у этого пользователя
    old_basket_item = Basket.objects.filter(user=request.user, product=product)

    if old_basket_item:
        old_basket_item[0].quantity += 1
        old_basket_item[0].save()
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''

@login_required
class BasketAddView(UpdateView):
    model = Basket
    template_name = 'mainapp/good.html'
    fields = ('__all__')

    #@method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BasketAddView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BasketAddView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        print('pk',pk)
        product = get_object_or_404(Product, pk=pk)
        old_basket_item = Basket.objects.filter(user=request.user, product=product)
        if old_basket_item:
            old_basket_item[0].quantity += 1
            old_basket_item[0].save()
        else:
            new_basket_item = Basket(user=request.user, product=product)
            new_basket_item.quantity += 1
            new_basket_item.save()
        return context
'''


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
@login_required
class BasketRemoveView(DeleteView):
    model = Basket
    template_name = 'basket/includes/inc_basket_list.html'
    success_url = reverse_lazy('basket/basket')

    #@method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BasketRemoveView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
'''


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__country')
        content = {'basket_items': basket_items, }
        result = render_to_string('basket/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})


'''
@login_required
class BasketUpdateView(UpdateView):
    model = Basket
    template_name = 'basket/basket.html'
    fields = ('__all__')

    #@method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BasketUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BasketUpdateView, self).get_context_data(**kwargs)
        #print(context)
        pk = self.kwargs['pk']
        quantity = self.kwargs['quantity']
        print(pk, quantity)
        new_basket_item = Basket.objects.get(pk=pk)
        if int(quantity) > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        return context
'''


@login_required
def basket_delete(request, pk):
    if request.is_ajax():
        new_basket_item = Basket.objects.get(pk=int(pk))
        new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__cost')
        content = {'basket_items': basket_items, }
        result = render_to_string('basket/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})


'''
class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'basket/includes/inc_basket_list.html'
    success_url = reverse_lazy('basket/basket')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BasketDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
'''
