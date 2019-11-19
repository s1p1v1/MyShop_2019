from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from authapp.models import ShopUser
from mainapp.models import Country, Product


class UsersListView(ListView):
    model = ShopUser
    template_name = 'myadmin/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UsersListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'myadmin/user_update.html'
    success_url = reverse_lazy('myadmin:users')
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'myadmin/user_update.html'
    success_url = reverse_lazy('myadmin:users')
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'myadmin/user_delete.html'
    success_url = reverse_lazy('myadmin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context


################################################################

class CountrysListView(ListView):
    model = Country
    template_name = 'myadmin/countrys.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CountrysListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CountrysListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/страны'
        return context


'''
@user_passes_test(lambda u: u.is_superuser)
def countrys(request):
    title = 'админка/страны'
    countrys_list = Country.objects.all()
    content = {
        'title': title,
        'objects': countrys_list
    }
    return render(request, 'myadmin/countrys.html', content)
'''


class CountryCreateView(CreateView):
    model = Country
    template_name = 'myadmin/country_update.html'
    success_url = reverse_lazy('myadmin:countrys')
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CountryCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'страны/создание/редактирование'
        return context


'''
class CountryUpdateView(UpdateView):
    model = Country
    template_name = 'myadmin/country_update.html'
    success_url = reverse_lazy('myadmin:countrys')
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CountryUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'страны/редактирование'
        return context

'''


class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'myadmin/country_delete.html'
    success_url = reverse_lazy('myadmin:countrys')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CountryDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CountryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'страны/удаление'
        return context


########################################################

'''
@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    country = get_object_or_404(Country, pk=pk)
    products_list = Product.objects.filter(country__pk=pk).order_by('caption')
    print(products_list)
    content = {
        'title': title,
        'country': country,
        'objects': products_list,
    }
    return render(request, 'myadmin/products.html', content)

'''


class CountryProductsView(ListView):
    template_name = 'myadmin/products.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        print(self.request, self.kwargs)
        self.country = get_object_or_404(Country, pk=pk)
        print('1pk', pk)
        products_list = Product.objects.filter(country__pk=pk)
        print('1pl', products_list)
        return products_list

    def get_context_data(self, **kwargs):
        context = super(CountryProductsView, self).get_context_data(**kwargs)
        print('1c1', context)
        context['title'] = 'продукт/создание'
        pk = self.kwargs['pk']
        context['country'] = self.country
        print('1c2', context)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'myadmin/product_read.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'myadmin/product_create.html'
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        # print('c1',context)
        context['title'] = 'продукт/создание'
        pk = self.kwargs['pk']
        self.country = get_object_or_404(Country, pk=pk)
        print(self.country)
        print('c2', context)
        print(pk)
        context['pk'] = pk
        return context

    def get_success_url(self):
        # return reverse('myadmin:products', args=[self.object.country.pk])
        return reverse('myadmin:products', args=[self.kwargs['pk']])
        # return reverse('myadmin:products', args=[2])


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'myadmin/product_update.html'
    fields = ('__all__')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        pk = self.kwargs['pk']
        print(pk)
        self.country = get_object_or_404(Country, pk=pk)
        context['pk'] = pk
        return context

    def get_success_url(self):
        return reverse('myadmin:products', args=[self.kwargs['pk']])
        # return reverse('myadmin:products', args=[self.object.country.pk])
        # return reverse('myadmin:products', args=[self.country.pk])
        # return reverse('myadmin:products', args=[1])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'myadmin/product_delete.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        pk = self.kwargs['pk']
        print(pk)
        context['pk'] = pk
        return context

    def get_success_url(self):
        return reverse('myadmin:products', args=[self.kwargs['pk']])
        # return reverse('myadmin:products', args=[self.object.country.pk])


'''
@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    country = get_object_or_404(Country, pk=pk)
    products_list = Product.objects.filter(country__pk=pk).order_by('caption')
    content = {
        'title': title,
        'country': country,
        'objects': products_list,
    }
    return render(request, 'myadmin/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        # задаем начальное значение категории в форме
        product_form = ProductEditForm(initial={'country': country})
    content = {'title': title, 'update_form': product_form, 'country': country}
    return render(request, 'myadmin/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title, 'object': product, }
    return render(request, 'myadmin/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('myadmin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    content = {'title': title, 'update_form': edit_form, 'country': edit_product.country}
    return render(request, 'myadmin/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('myadmin:products', args=[product.country.pk]))
    content = {
        'title': title,
        'product_to_delete': product
    }
    return render(request, 'myadmin/product_delete.html', content)

'''
