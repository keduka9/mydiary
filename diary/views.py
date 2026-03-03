from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm

@login_required
def entry_list(request):
    entries = Entry.objects.filter(user=request.user)
    return render(request, 'diary/entry_list.html', {'entries': entries})

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    return render(request, 'diary/entry_detail.html', {'entry': entry})

@login_required
def entry_new(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('entry_detail', pk=entry.pk)
        
    else:
        form = EntryForm()
    return render(request, 'diary/entry_new.html', {'form': form})

@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm(instandce=entry)
    return render(request, 'diary/entry_edit.html', {'form': form, 'entry': entry})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_lsit')
    return render(request, 'diary/entry_delete.html', {'entry': entry})