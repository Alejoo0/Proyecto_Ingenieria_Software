from django.shortcuts           import render, redirect
from django.contrib.auth.views  import PasswordResetView
from django.contrib.auth.models import User
from django.urls                import reverse_lazy
from django                     import forms
from django.shortcuts           import render
from .models                    import Curso
from django.contrib.auth.decorators import login_required
from .models import Estudiante

@login_required
def home(request):
    return render (request, 'core/home.html')

def cursos(request):
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        cursos = estudiante.cursos_inscritos.all()
        return render(request, 'core/cursos.html', {'cursos': cursos})
    except Estudiante.DoesNotExist:
        return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            form.add_error('email', forms.ValidationError("Este correo electrónico no está registrado."))
            return self.form_invalid(form)
        return super().form_valid(form)