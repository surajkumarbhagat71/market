from django.shortcuts import render,redirect ,get_object_or_404
from django.views.generic import ListView , DetailView , View , TemplateView
from django.views.generic.edit import UpdateView ,DeleteView
from .models import *
from . forms import *
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import Group

from django.contrib.auth import  login , logout , authenticate


#---------------------------------------- Registation & login & logout -----------------------

class UserRegistations(View):
    def get(self,request,*args,**kwargs):
        form = User_RegistationForm()
        return render(request, 'main/signup.html', {"form":form})


    def post(self,request,*args,**kwargs):
        form = User_RegistationForm(request.POST or None)

        if form.is_valid():
            s = form.save()
            group = Group.objects.get(name='users')
            s.groups.add(group)
            s.save()
            return redirect('shop:home')


class Login(View):
    def get(self,request):
        return render(request, 'main/login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email = username)
        except ObjectDoesNotExist:
            return redirect('shop:login')

        try:
            user = authenticate(username = username.username,password = password)

            if user is not None:
                login(request,user)
            else:
                return redirect('shop:home')

            if user.groups.filter(name='users').exists():
                return redirect('shop:order_sumary')
            elif user.groups.filter(name='admin'):
                return redirect('shop:dashaboard')
            else:
                return redirect('shop:home')

        except ObjectDoesNotExist:
            return redirect('shop:home')



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:home')


# _________________________________________________ Shop Work ______________________________________________#

class Home(ListView):
    model = Item
    template_name = 'main/home.html'
    context_object_name = 'items'



class PorductDetail(DetailView):
    model = Item
    template_name = 'main/item_detail.html'
    context_object_name = 'product'



class SearchProduct(View):
    def get(self,request):
        search = request.GET.get('search')
        cond = Q(title__icontains = search ) | Q(brand__brand_name__icontains = search)
        data = {"items":Item.objects.filter(cond)}
        return render(request,'main/home.html',data)



class AddToCart(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):

        item = get_object_or_404(Item ,item_id = pk)

        order_item , create = CartItem.objects.get_or_create(user = request.user , itme = item , ordered=False)

        order = Order.objects.filter(user = request.user ,ordered=False)

        if order.exists():
            order_as = order[0]
            if order_as.items.filter(itme__item_id = pk ).exists():
                order_item.qty += 1
                order_item.save()
                return redirect('shop:order_sumary')
            else:
                order_as.items.add(order_item)
                return redirect('shop:order_sumary')
        else:
            order = Order.objects.create(user=request.user,ordered=False)
            order.items.add(order_item)
            return redirect('shop:order_sumary')




class RemoveItemQty(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        item = get_object_or_404(Item,item_id = pk)
        order = Order.objects.filter(user = request.user , ordered=False)
        if order.exists():
            order_as = order[0]
            if order_as.items.filter(itme__item_id = pk ).exists():
                order_item = CartItem.objects.filter(user= request.user, itme = item , ordered = False )[0]
                if order_item.qty > 1:
                    order_item.qty -= 1
                    order_item.save()
                    return redirect('shop:order_sumary')
                else:
                    order_as.items.remove(order_item)
                    return redirect('shop:order_sumary')
            else:
                return redirect('shop:home')
        else:
            return redirect('shop:home')



class RemoveItem(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):

        item = get_object_or_404(Item,item_id =pk)

        order = Order.objects.filter(user = request.user , ordered=False)

        if order.exists():
            order_as = order[0]
            if order_as.items.filter(itme__item_id = pk).exists():
                cart_item = CartItem.objects.filter(user=request.user , itme=item , ordered=False)[0]
                order_as.items.remove(cart_item)
                cart_item.delete()
                return redirect('shop:order_sumary')
            else:
                return redirect('shop:order_sumary')
        else:
            return redirect('shop:home')



class Checkout(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
            form = AddressForm(request.POST or None)
            data = {
                "forms":form,
                "address":UserAddress.objects.filter(user = request.user)
            }
            return render(request,'users/checkout.html',data)

    def post(self,request,*args,**kwargs):
        order = Order.objects.get(user=request.user ,ordered=False)
        form = AddressForm(request.POST or None)
        if self.request.method == "POST":
            save_address = request.POST.get('save_address',None)
            if save_address != None:
                my_address = UserAddress.objects.get(address_id=save_address ,user=request.user)

                order.address = my_address
                order.save()
                return redirect('shop:payment')
            else:
                if form.is_valid():
                    a = form.save(commit=False)
                    a.user = self.request.user
                    a.save()

                    order.address = a
                    order.save()
                    return redirect('shop:payment')


class UpdateAddress(UpdateView):
    model = UserAddress
    form_class = AddressForm
    template_name = 'users/update_address.html'

    def form_valid(self, form):
        form.save()
        return redirect('shop:home')


class DeleteAddress(LoginRequiredMixin,View):
    def get(self,request,pk):
        data = UserAddress.objects.get(address_id=pk)
        data.delete()
        return render(request,'users/checkout.html')




class OrderSumary(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            data = {"order":Order.objects.get( user = self.request.user ,ordered = False)}
            return render(self.request,'users/order_summary.html',data)
        except ObjectDoesNotExist:
            return render(request,'main/home.html')



class MyOrder(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        data = {"order":Order.objects.filter( user = self.request.user ,ordered = True)}
        return render(request,'users/my_order.html',data)



class PaymentView(LoginRequiredMixin,View):
    def get(self,request):

        return render(request,'users/payment.html')

    def post(self,request,*args,**kwargs):
        order = Order.objects.get(user=request.user,ordered=False)

        if not order.address:
            return redirect('shop:checkout')

        if request.method == "POST":
            if request.POST.get('payment') == 'cod':
                pay = Payment()
                pay.user = request.user
                pay.order_id = order
                pay.amount = order.get_total()
                pay.save()

                order_as = order.items.all()
                order_as.update(ordered=True)
                for x in order_as:
                    x.save()

                order.ordered = True
                order.order_date = timezone.now()
                order.save()
                return redirect('shop:myorder')


#------------------------------------------- Owner --------------------------------------------#

class Dashaboard(LoginRequiredMixin,View):
    def get(self,request):
        data = {
            "all_request_order":Order.objects.filter(status=False).count(),
            "all_order":Order.objects.filter(status=True).count(),
            "all_add_item":Order.objects.filter(ordered=False).count(),
            'allbrand':Brand.objects.all().count(),
            'allcategory':Category.objects.all().count(),
        }

        return render(request,'owner/dashaboard.html',data)


class RequestForOrder(LoginRequiredMixin,View):
    def get(self,request):
        data = {"request_order":Order.objects.filter(status=False)}

        return render(request,'owner/order_request.html',data)


class AproveOrder(LoginRequiredMixin,View):
    def get(self,request,pk):
        order = Order.objects.get(order_id = pk)
        order.status = True
        order.save()
        return render(request,'owner/dashaboard.html')


class AddItem(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form = ItemForm()
        data = {"form":form}
        return render(request,'owner/additem.html',data)


    def post(self,request,*args,**kwargs):
        form = ItemForm(request.POST or None , request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('shop:dashaboard')

        return render(request,'owner/dashaboard.html')


class AllItem(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'owner/all_item.html'
    context_object_name = 'item'




class AllOrder(LoginRequiredMixin,View):
    def get(self,request):
        data = {"allorder":Order.objects.filter(status=True)}
        return render(request,'owner/all_order.html',data)


class DeleteItem(LoginRequiredMixin,View):
    def get(self,request,pk):
        data = Item.objects.get(item_id = pk)
        data.delete()
        return render(request,'owner/all_item.html')


class AddBrand(LoginRequiredMixin,View):
    def get(self,request):
        form = ItemBrandForm()
        data = {"forms":form}
        return render(request,'owner/addbrand.html',data)


    def post(self,request):
        form = ItemBrandForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request,'owner/addbrand.html')


class AddCategory(LoginRequiredMixin,View):
    def get(self,request):
        form = ItemCategoryForm()
        data = {"form":form}
        return render(request,'owner/addcategory.html',data)


    def post(self,request):
        form = ItemCategoryForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('shop:dashaboard')




class AllBrand(LoginRequiredMixin,ListView):
    model =  Brand
    template_name = 'owner/all_brand.html'
    context_object_name = 'allbrand'



class AllCategory(LoginRequiredMixin,ListView):
    model =  Category
    template_name = 'owner/all_category.html'
    context_object_name = 'allcategory'



class DeleteBrand(LoginRequiredMixin,View):
    def get(self,request,pk):
        data = Brand.objects.get(brand_id=pk)
        data.delete()
        return render(request,'owner/all_brand.html')


class DeleteCategory(LoginRequiredMixin,View):
    def get(self,request,pk):
        data = Category.objects.get(category_id = pk)
        data.delete()
        return render(request,'owner/all_category.html')






