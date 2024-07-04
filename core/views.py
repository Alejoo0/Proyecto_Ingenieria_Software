from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from dal import autocomplete
from .models import Estudiante, Asignatura

def home(request):
    return render (request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


class EstudianteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Estudiante.objects.none()

        asignatura_id = self.forwarded.get('asignatura', None)

        if asignatura_id:
            return Estudiante.objects.filter(asignatura__id=asignatura_id)
        return Estudiante.objects.none()