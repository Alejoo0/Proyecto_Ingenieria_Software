from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.http import JsonResponse
from django.db.models import Max, Q
from django.contrib import messages
import pytz
from django.utils import timezone
from django.urls import reverse
from .forms import *
from .models import *

def home(request):
    return render(request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def home(request):
    try:
        usuario_detalles = request.user.usuariodetalles
        nivel_educacional = usuario_detalles.nivel_educacional
        segundo_valor_nivel = None

        for tupla in NIVELES_CHOICES:
            if tupla[0] == nivel_educacional:
                segundo_valor_nivel = tupla[1]
                break
    except UsuarioDetalles.DoesNotExist:
        segundo_valor_nivel = "No especificado"
    
    return render(request, 'core/home.html', {'nivel_educacional': segundo_valor_nivel})

@login_required
def bandeja_entrada(request):
    zona_horaria = pytz.timezone('America/Santiago')
    timezone.activate(zona_horaria)
    try:
        usuario_detalles = request.user.usuariodetalles
        nivel_educacional = usuario_detalles.nivel_educacional
        segundo_valor_nivel = None

        for tupla in NIVELES_CHOICES:
            if tupla[0] == nivel_educacional:
                segundo_valor_nivel = tupla[1]
                break
    except UsuarioDetalles.DoesNotExist:
        segundo_valor_nivel = "No especificado"

    if request.method == 'POST':
        if 'accion' in request.POST and request.POST['accion'] == 'eliminar_conversacion':
            usuario_id = request.POST.get('usuario_id')
            
            # Verificar si el usuario_id es válido y no está vacío
            if usuario_id is None:
                messages.error(request, 'No se proporcionó un ID de usuario válido.')
                return redirect('bandeja_entrada')

            try:
                usuario_id = int(usuario_id)
            except ValueError:
                messages.error(request, 'El ID de usuario proporcionado no es válido.')
                return redirect('bandeja_entrada')

            try:
                usuario_destinatario = User.objects.get(id=usuario_id)
            except User.DoesNotExist:
                messages.error(request, 'El usuario destinatario no existe.')
                return redirect('bandeja_entrada')

            conversacion = Mensaje.objects.filter(
                (Q(remitente=request.user) & Q(destinatario=usuario_destinatario)) |
                (Q(remitente=usuario_destinatario) & Q(destinatario=request.user))
            )
            conversacion.delete()
            messages.success(request, 'Conversación eliminada correctamente.')
            return redirect('bandeja_entrada')

        elif request.POST['accion'] == 'enviar_mensaje':
            usuario_id = request.POST.get('usuario_id')
            usuario_destinatario = get_object_or_404(User, id=usuario_id)
            form_mensaje = MensajeForm(request.POST)
            if form_mensaje.is_valid():
                nuevo_mensaje = form_mensaje.save(commit=False)
                nuevo_mensaje.remitente = request.user
                nuevo_mensaje.destinatario = usuario_destinatario
                nuevo_mensaje.save()
                if usuario_id:
                    return redirect(reverse('bandeja_entrada') + f'?usuario_id={usuario_id}')
                else:
                    return redirect('bandeja_entrada')

    usuario = request.user
    form_nueva_conversacion = NuevaConversacionForm(usuario_actual=usuario)
    conversaciones = {}
    mensajes_recibidos = Mensaje.objects.filter(destinatario=usuario)
    mensajes_enviados = Mensaje.objects.filter(remitente=usuario)

    remitentes_recibidos = mensajes_recibidos.values('remitente').annotate(ultima_fecha=Max('timestamp'))
    destinatarios_enviados = mensajes_enviados.values('destinatario').annotate(ultima_fecha=Max('timestamp'))

    for remitente in remitentes_recibidos:
        ultimo_mensaje = mensajes_recibidos.filter(remitente=remitente['remitente'], timestamp=remitente['ultima_fecha']).first()
        conversaciones[remitente['remitente']] = {
            'usuario': User.objects.get(id=remitente['remitente']),
            'ultimo_mensaje': ultimo_mensaje.contenido if ultimo_mensaje else '',
            'timestamp': remitente['ultima_fecha'],
            'leido': ultimo_mensaje.leido if ultimo_mensaje else False,
            'es_remitente': False  # Marcar como False para los mensajes recibidos
        }

    for destinatario in destinatarios_enviados:
        ultimo_mensaje = mensajes_enviados.filter(destinatario=destinatario['destinatario'], timestamp=destinatario['ultima_fecha']).first()
        conversaciones[destinatario['destinatario']] = {
            'usuario': User.objects.get(id=destinatario['destinatario']),
            'ultimo_mensaje': ultimo_mensaje.contenido if ultimo_mensaje else '',
            'timestamp': destinatario['ultima_fecha'],
            'leido': ultimo_mensaje.leido if ultimo_mensaje else False,
            'es_remitente': True  # Marcar como True para los mensajes enviados
        }

    conversacion_seleccionada = None
    mensajes_agrupados = None
    form_mensaje = None

    if 'usuario_id' in request.GET:
        usuario_otro = get_object_or_404(User, id=request.GET['usuario_id'])
        mensajes = Mensaje.objects.filter(
            (Q(remitente=usuario) & Q(destinatario=usuario_otro)) |
            (Q(remitente=usuario_otro) & Q(destinatario=usuario))
        ).order_by('timestamp')

        form_mensaje = MensajeForm()

        # Marcar mensajes como leídos cuando se ve la conversación
        mensajes.filter(destinatario=usuario, leido=False).update(leido=True)

        mensajes_agrupados = {}
        for mensaje in mensajes:
            fecha_local = localtime(mensaje.timestamp).date()
            if fecha_local not in mensajes_agrupados:
                mensajes_agrupados[fecha_local] = []
            mensajes_agrupados[fecha_local].append({
                'mensaje': mensaje,
                'es_remitente': mensaje.remitente == request.user  # Marcar si el mensaje es del remitente
            })

        conversacion_seleccionada = {
            'usuario': usuario_otro,
            'mensajes_agrupados': mensajes_agrupados,
            'form_mensaje': form_mensaje
        }

    context = {
        'conversaciones': conversaciones.values(),
        'form_nueva_conversacion': form_nueva_conversacion,
        'conversacion_seleccionada': conversacion_seleccionada,
        'nivel_educacional': segundo_valor_nivel,
    }
    return render(request, 'core/bandeja_entrada.html', context)

@login_required
def crear_conversacion(request):
    if request.method == 'POST':
        form = NuevaConversacionForm(request.POST, usuario_actual=request.user)
        if form.is_valid():
            destinatario = form.cleaned_data['destinatario']

            # Verificar si ya existe una conversación con este destinatario
            conversacion_existente = Mensaje.objects.filter(
                (Q(remitente=request.user) & Q(destinatario=destinatario)) |
                (Q(remitente=destinatario) & Q(destinatario=request.user))
            ).exists()

            if conversacion_existente:
                messages.error(request, 'Ya existe una conversación con este usuario.')
            else:
                # Crear el primer mensaje solo si no hay conversación existente
                nueva_conversacion = Mensaje.objects.create(
                    remitente=request.user,
                    destinatario=destinatario,
                )
                messages.success(request, 'Conversación iniciada correctamente.')
                # Redirigir a la conversación recién creada
                return redirect(reverse('bandeja_entrada') + f'?usuario_id={destinatario.id}')

    else:
        form = NuevaConversacionForm(usuario_actual=request.user)
    
    return redirect('bandeja_entrada')

@login_required
def enviar_mensaje(request, usuario_id):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            destinatario = get_object_or_404(User, id=usuario_id)
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.destinatario = destinatario
            mensaje.save()
            return redirect('bandeja_entrada')
    return redirect('bandeja_entrada')
