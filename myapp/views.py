from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Producto
from .forms import ProductoForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views.generic import DetailView



class ListaProductosView(View):
    def get(self, request):
        productos = Producto.objects.all()
        return render(request, 'productos.html', {'productos': productos})


class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'detalle_producto.html'
    
    

def buscar_productos(request):
    q = request.GET.get('q')
    if q:
        productos = Producto.objects.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )
    else:
        productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos, 'query': q})


class CrearProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('lista_productos')
    template_name = 'agregar_producto.html'


class BuscarProductoView(FormView):
    template_name = 'buscar_producto.html'
    form_class = ProductoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        return context

    def form_valid(self, form):
        busqueda = form.cleaned_data['busqueda']
        productos = Producto.objects.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda)
        )
        context = self.get_context_data()
        context['productos'] = productos
        return self.render_to_response(context)
