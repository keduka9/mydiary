from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm
from rest_framework import generics, permissions
from .serializers import EntrySerializer

@login_required
def entry_list(request):
    entries = Entry.objects.filter(user=request.user)

    # 検索
    query = request.GET.get('q', '')
    if query:
        entries = entries.filter(title__icontains=query) | entries.filter(content__icontains=query)

    # 月別絞り込み
    month = request.GET.get('month', '')
    if month:
        year, m = month.split('_')
        entries = entries.filter(date__year=year, date__month = m)

    # 気分別絞り込み
    mood = request.GET.get('mood', '')
    if mood:
        entries = entries.filter(mood=mood)

    # ページネーション
    from django.core.paginator import Paginator
    paginator = Paginator(entries, 5)   # 1ページ5件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'diary/entry_list.html', {
        'page_obj': page_obj,
        'query': query,
        'month': month,
        'mood': mood,
        'mood_choices': Entry.MOOD_CHOICES,
    })

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
        form = EntryForm(instance=entry)
    return render(request, 'diary/entry_edit.html', {'form': form, 'entry': entry})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_lsit')
    return render(request, 'diary/entry_delete.html', {'entry': entry})

class EntryListAPI(generics.ListCreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EntryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)