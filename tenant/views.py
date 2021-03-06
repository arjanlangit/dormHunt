from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView
    )
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.contrib import messages
import folium
import requests
import json

# SECTION Import Models
from landlord.models import Property, AddTenant, Reminder, Expenses, History
from tenant.models import Application, MessageRoom, Message
from user.models import User

# SECTION Import Forms
from tenant.forms import ApplicationForm
from user.models import User

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class no_dorm(TemplateView):
    template_name = 'tenant/tenant_home_no_dorm.html'

class has_dorm(TemplateView):
    template_name = 'tenant/tenant_home.html'

    def get_context_data(self, **kwargs):
        user = AddTenant.objects.get(account_user=self.request.user.email)
        
        details = get_object_or_404(AddTenant, account_user=self.request.user.email)
        expenses = Expenses.objects.filter(property_name=user.dorm)
        reminders = Reminder.objects.filter(property_name=user.dorm, next_service=date.today())
        histories = History.objects.filter(tenant=self.request.user).order_by('-date_paid')[:1]

        context = super(has_dorm, self).get_context_data(**kwargs)
        if details.is_paid == False and details.expense_is_paid == False:
            total_balance = details.balance + details.expense_balance
            context['total_balance'] = total_balance
        
        context['expenses'] = expenses
        context['details'] = details
        context["reminders"] = reminders
        context['histories'] = histories
        return context

def Home_Tenant(request):
    try:
        tenant = AddTenant.objects.get(account=request.user)
        print(tenant)
    except ObjectDoesNotExist:
        return redirect('tenant:no_dorm')
    return redirect('tenant:has_dorm')

class TenantFavorites(TemplateView):
    template_name = 'tenant/tenant_favorites.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        favorites = []

        properties = Property.objects.all()

        for p in properties:
            if p.favorite.filter(pk=user.pk).exists():
                favorites.append(p)
            else:
                pass
        print(favorites)

        context = super().get_context_data(**kwargs)
        context["favorites"] = favorites
        return context
    
def favorite_property(request, pk):
    current_property = get_object_or_404(Property, pk=pk)
    this_property = Property.objects.get(pk=current_property.pk)

    if current_property.favorite.filter(pk=request.user.pk).exists():
        this_property.favorite.remove(request.user)
    else:
        this_property.favorite.add(request.user)
    return redirect('tenant:view_property', pk=current_property.pk)
    

class TenantDormSearch(ListView):
    model = Property
    template_name = 'tenant/tenant_search.html'

    def get_context_data(self, **kwargs):
        order = self.kwargs['order']
        if order == 1:
            query = Property.objects.order_by('-created_at')
        elif order == 2:
            query = Property.objects.order_by('-views')
        else:
            query = Property.objects.all()

        context = super().get_context_data(**kwargs)
        context["order"] = order
        context["property_list"] = query
        return context
    

def tenant_map(request):
    url = "http://api.ipstack.com/check?access_key=41fc2af18a10d4c05cfa0d92f26ba0a8"
    location_request = requests.get(url)
    json_request = json.loads(location_request.text)
    latitude = json_request['latitude']
    longitude = json_request['longitude']

    tenant_map = folium.Map(location=[latitude, longitude], zoom_start=11)
    tooltip = 'Click for more info'

    marker_query = Property.objects.all()

    for marker in marker_query:
        folium.Marker([marker.latitude, marker.longitude], 
                      popup= folium.Popup("""   <a href="/tenant/search/property/{}" target="_self"> <h4 style="margin-bottom:0;">{}</h4> </a>
                                                <p style="margin-top:0;">{}</p>
                                                <img src="{}" alt="Dorm" width="250" height="150">""".format(marker.pk, marker.name, marker.address, marker.thumbnail.url)),
                      icon=folium.Icon(icon='home', color='blue')).add_to(tenant_map),

    # folium.CircleMarker(location=[latitude, longitude], radius=30, popup='Your Location', color='#3186cc', fill=True, fill_color='#3186cc').add_to(tenant_map),

    tenant_map.save('tenant/templates/tenant/tenant_map.html')
    return render(request, 'tenant/tenant_map.html')

class ViewPropertyDetailView(DetailView):
    model = Property
    template_name = 'tenant/view_property.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            tenant = AddTenant.objects.get(account=self.request.user)
            context['tenant'] = tenant
        except ObjectDoesNotExist:
            pass

        pk = self.kwargs['pk']
        query = Property.objects.get(pk=pk)
        users = query.favorite.all()

        # Add 1 view
        query.views += 1
        query.save()


        context["users"] = users
        return context



# NOTE Temporary, created so i can view my template
class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    model = Application
    template_name = 'tenant/application_form.html'

    def form_valid(self, form):
        form.instance.tenant = self.request.user
        pk = self.kwargs['pk']
        print(pk)
        query = Property.objects.get(pk=pk)
        print(query.name)
        form.instance.dorm = query

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        property_query = Property.objects.get(pk=pk)
        user_query = User.objects.get(pk=self.request.user.pk)

        context = super().get_context_data(**kwargs)
        context["property"] = property_query
        context["user"] = user_query
        return context

class No_Dorm_Messages(TemplateView):
    template_name = 'tenant/tenant_no_dorm_messages.html'

    def get_context_data(self, **kwargs):
        try:
            applicatons = Application.objects.filter(tenant=self.request.user)
        except ObjectDoesNotExist:
            applicatons = False

        context = super(No_Dorm_Messages, self).get_context_data(**kwargs)
        context["applications"] = applicatons 
        return context


class Has_Dorm_Messages(TemplateView):
    template_name = 'tenant/tenant_has_dorm_messages.html'

def Messages_Tenant(request):
    try:
        tenant_email = AddTenant.objects.get(account_user=request.user.email)
    except ObjectDoesNotExist:
        return redirect('tenant:no_dorm-messages')
    return redirect('tenant:messages_list')

def messages_list(request):
    context = {}

    user = request.user
    # tenant = AddTenant.objects.get(account=user)
    rooms = MessageRoom.objects.filter(members=request.user)
    context['rooms'] = rooms

    return render(request, 'tenant/tenant_has_dorm_messages.html', context)

def tenant_ind_messages(request, room_name):
    dorm = MessageRoom.objects.filter(name=room_name)[0]

    return render(request, 'tenant/tenant_ind_messages.html', {
        'room_name': room_name,
        'username': request.user.username,
        'dorm': dorm,
    })

def create_room(request):
    if request.method == "POST":
        recipient = request.POST.get('recipient')
        message = request.POST.get('message')

        if User.objects.filter(email=recipient).exists():
            user = User.objects.get(email=recipient)

            if user == request.user:
                messages.error(request, "You cannot send a message to yourself!")
                return redirect('tenant:create_room')
            else:
                room_name = "{}{}".format(user.username, request.user.username)
                room_name = room_name.replace(" ", "")
                # print(room_name)
                room = MessageRoom.objects.create(
                    name = room_name,
                )
                room.save()
                room.members.add(user)
                room.members.add(request.user)

                first_message = Message.objects.create(
                    room = room,
                    author = request.user,
                    content = message,
                )

                return redirect('tenant:messages')
                
        else:
            messages.error(request, "The recipient does not exist!")
            return redirect('tenant:create_room')

    else:
        return render(request, 'tenant/message_room_form.html')

# NOTE For Viewing Purposes only
class Request(TemplateView):
    template_name = 'tenant/request.html'
# class TenantIndMessages(TemplateView):
#     template_name = 'tenant/tenant_ind_messages.html'

class HistoryListView(ListView):
    # model = History
    template_name = 'tenant/payment_history.html'

    def get_queryset(self):
        return History.objects.filter(tenant=self.request.user).order_by('-date_paid')
        
    