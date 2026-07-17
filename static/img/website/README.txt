# Imágenes de la página principal (website)

Ruta del proyecto:
  static/img/website/

Portada (inicio):
  static/img/website/portada.jpg

Registro Sin limites (columna izquierda):
  static/img/website/niño.jpg
  (alternativa: nino.jpg)

URL en plantillas:
  {% load static %}
  <img src="{% static 'img/website/niño.jpg' %}" alt="">
