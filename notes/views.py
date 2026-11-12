from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Note
from .forms import NoteForm, RegisterForm

# 1. User Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto log-in after registration
            return redirect('note_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# 2. List Notes (Protected & User-Isolated)
@login_required
def note_list(request):
    # Fetch ONLY notes belonging to the logged-in user
    notes = Note.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

# 3. Create Note
@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user  # Automatically assign current user as owner
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_create.html', {'form': form})

# 4. Delete Note (With Ownership Check)
@login_required
def note_delete(request, pk):
    # Ensures a user cannot delete someone else's note via URL manipulation
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})