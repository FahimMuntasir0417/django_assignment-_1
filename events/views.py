from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.http import Http404
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def manager_dashboard(request):
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=timezone.now().date()).count()
    past_events_count = Event.objects.filter(date__lt=timezone.now().date()).count()
    total_participants = Participant.objects.count()

    counts = {
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'total_participants': total_participants,
    }

    event_filter_type = request.GET.get('type', 'all')

    filtered_events = Event.objects.select_related('category').annotate(participant_count=Count('participants'))

    if event_filter_type == 'upcoming':
        filtered_events = filtered_events.filter(date__gte=timezone.now().date())
    elif event_filter_type == 'past':
        filtered_events = filtered_events.filter(date__lt=timezone.now().date())

    filtered_events = filtered_events.order_by('date', 'time')

    context = {
        "filtered_events": filtered_events,
        "counts": counts,
        "current_filter_type": event_filter_type,
    }
    return render(request, "events/dashboard.html", context)

def create_event(request):
    event_form = EventForm()

    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('event_list')

    context = {"form": event_form, "title": "Create New Event"}
    return render(request, "events/event_form.html", context)

def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    event_form = EventForm(instance=event)

    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event_detail', pk=pk)

    context = {"form": event_form, "title": "Update Event"}
    return render(request, "events/event_form.html", context)

def delete_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event, 'type': 'Event'})

def event_list(request):
    events = Event.objects.all().select_related('category').annotate(participant_count=Count('participants'))

    search_query = request.GET.get('q')
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category__id=category_id)

    events = events.order_by('date', 'time')
    categories = Category.objects.all().order_by('name')

    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    try:
        event = Event.objects.prefetch_related('participants').get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    return render(request, 'events/event_detail.html', {'event': event})

def participant_list(request):
    participants = Participant.objects.all().order_by('name')
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_detail(request, pk):
    try:
        participant = Participant.objects.prefetch_related('events').get(pk=pk)
    except Participant.DoesNotExist:
        raise Http404("Participant does not exist")
    return render(request, 'events/participant_detail.html', {'participant': participant})

def participant_create(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Created Successfully")
            return redirect('participant_list')
    return render(request, 'events/participant_form.html', {'form': form, 'title': 'Add New Participant'})

def participant_update(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        raise Http404("Participant does not exist")
    form = ParticipantForm(instance=participant)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Updated Successfully")
            return redirect('participant_detail', pk=pk)
    return render(request, 'events/participant_form.html', {'form': form, 'title': 'Update Participant'})

def participant_delete(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        raise Http404("Participant does not exist")
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant Deleted Successfully')
        return redirect('participant_list')
    return render(request, 'events/confirm_delete.html', {'object': participant, 'type': 'Participant'})

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'events/category_list.html', {'categories': categories})

def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    events_in_category = Event.objects.filter(category=category).order_by('date', 'time')
    return render(request, 'events/category_detail.html', {'category': category, 'events_in_category': events_in_category})

def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Create New Category'})

def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('category_detail', pk=pk)
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Update Category'})

def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category, 'type': 'Category'})

def view_categories_with_event_counts(request):
    categories = Category.objects.annotate(num_events=Count('event')).order_by('num_events')
    return render(request, "events/category_event_counts.html", {"categories": categories})


# Create your views here.
