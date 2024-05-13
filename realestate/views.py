from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import LoginForm, PropertyForm, PropertyFilterForm, EventForm, ReportForm, ContactAgentForm, ContactForm
from .models import Event, Property, PropertyType, Neighborhood, SearchHistory
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
import calendar
from django.http import HttpResponse
from openpyxl import Workbook
from .models import SearchHistory
from django.contrib import messages


def index(request):
    featured_property = Property.objects.filter(featured=True).first()
    return render(request, 'index.html', {'featured_property': featured_property})


def about(request):
    return render(request, 'about.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def omaha_events(request):
    events = Event.objects.all()
    return render(request, 'omaha_events.html', {'events': events})


def property_listings(request):
    properties = Property.objects.all()

    form = PropertyFilterForm(request.GET)
    if form.is_valid():
        property_type = form.cleaned_data.get('property_type')
        neighborhood = form.cleaned_data.get('neighborhood')
        price_range = form.cleaned_data.get('price_range')
        if property_type:
            properties = properties.filter(property_type=property_type)
        if neighborhood:
            properties = properties.filter(neighborhood=neighborhood)
        if price_range:
            if price_range == '500000+':
                properties = properties.filter(price__gte=500000)
            else:
                min_price, max_price = map(int, price_range.split("-"))
                properties = properties.filter(price__gte=min_price, price__lte=max_price)

        if property_type or neighborhood or price_range:
            SearchHistory.objects.create(
                property_type=property_type,
                neighborhood=neighborhood,
                price_range=price_range
            )

    context = {
        'properties': properties,
        'form': form
    }
    return render(request, 'property_listings.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    return render(request, 'property_detail.html', {'property': property})


def mark_property_as_featured(request, pk):
    # Retrieve the new property object with the given primary key
    new_property = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        # Retrieve all properties with is_featured=True
        old_featured_properties = Property.objects.filter(featured=True)

        # Unmark all old featured properties
        for old_property in old_featured_properties:
            old_property.featured = False
            old_property.save()

        # Mark the new property as featured
        new_property.featured = True
        new_property.save()

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property_detail', args=[pk]))

    # If the request method is not POST, simply redirect to the property detail page
    return HttpResponseRedirect(reverse('property_detail', args=[pk]))


def change_property_status(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        property.status = new_status
        property.save()
        return HttpResponseRedirect(reverse('property_detail', args=[pk]))
    return HttpResponseRedirect(reverse('property_detail', args=[pk]))


def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to property detail page or any other appropriate page
            return redirect('property_listings')
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})


def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('property_detail', args=[pk]))
    else:
        form = PropertyForm(instance=property)
    return render(request, 'edit_property.html', {'form': form, 'property': property})


def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully.')
        return HttpResponseRedirect(reverse('property_listings'))
    return render(request, 'property_detail.html', {'property': property})


def generate_report(request):
    # Initialize form with session data
    year = request.session.get('year')
    month = request.session.get('month')
    form = ReportForm(initial={'year': year, 'month': month})

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            # Store year and month in session
            request.session['year'] = year
            request.session['month'] = month
            # Redirect back to the same view
            return redirect('generate_report')

    # Fetch searches based on year and month
    searches = SearchHistory.objects.filter(timestamp__year=year, timestamp__month=month)
    visitors_by_home_type = searches.filter(property_type__isnull=False).values(
        'property_type__property_type').annotate(count=Count('id'))
    visitors_by_neighborhood = searches.filter(neighborhood__isnull=False).values(
        'neighborhood__neighborhood').annotate(count=Count('id'))
    visitors_by_price_range = searches.exclude(price_range='').values('price_range').annotate(count=Count('id'))

    context = {
        'form': form,
        'visitors_by_home_type': visitors_by_home_type,
        'visitors_by_neighborhood': visitors_by_neighborhood,
        'visitors_by_price_range': visitors_by_price_range,
    }
    return render(request, 'generate_report.html', context)


def generate_excel_report(request):
    year = request.session.get('year')
    month = request.session.get('month')
    month = int(month)
    searches = SearchHistory.objects.filter(timestamp__year=year, timestamp__month=month)

    month_name = calendar.month_name[month]

    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    ws.append(["Time", "Property Type", "Neighborhood", "Price Range"])

    for search in searches:
        timestamp = search.timestamp.replace(tzinfo=None) if search.timestamp else None
        property_type = search.property_type.property_type if search.property_type else ''
        neighborhood = search.neighborhood.neighborhood if search.neighborhood else ''
        price_range = search.price_range
        ws.append([timestamp, property_type, neighborhood, price_range])

    filename = f"Report for {month_name} {year}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)

    return response


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def contact_form_page(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = ContactAgentForm(request.POST)
        if form.is_valid():
            return redirect('contact_agent', property_id=property_id)
    else:
        form = ContactAgentForm()
    return render(request, 'contact_form.html', {'form': form, 'property': property})


def contact_agent(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = ContactAgentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            subject = f"Message regarding property: {property.name}"
            body = f"Hi Carlos,\na message has been recieved from the customer named {name}\nEmail id: {email}\nPhone: {phone} \nis interested in the property :{property.name} \nMessage: {message}"
            send_mail(subject, body, 'carlos.k@gmail.com', ['carlos.k@gmail.com'])
            return redirect('thank_you_page')
    else:
        form = ContactAgentForm()
    return render(request, 'contact_form.html', {'form': form, 'property': property})


def thank_you_page(request):
    return render(request, 'thankyou.html')


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = "Message from CKRealEstate"
            email_content = f"Hi Carlos,\nMessage from a customer has been recieved: \nCustomer Name: {name}\nEmail: {email}\n Message: {message}\n\nFrom\nCKRealEstates"

            # Send the email
            send_mail(subject, email_content, 'carlos.k@gmail.com', ['carlos.k@gmail.com'])

            return redirect('thank_you_page')
    else:
        form = ContactForm()

    return render(request, 'about.html', {'form': form})


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return HttpResponseRedirect(reverse('events'))
    return render(request, 'omaha_events.html', {'event': event})
