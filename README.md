# Documentación Completa - Aplicación Flask de Búsqueda de Lugares

## Índice
1. [Introducción](#introducción)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Explicación del Backend (app.py)](#explicación-del-backend-apppy)
4. [Explicación del Frontend](#explicación-del-frontend)
5. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)

---

## Introducción

Esta aplicación web utiliza **Flask** para crear un buscador de lugares geográficos que consulta la API de **OpenStreetMap (Nominatim)** y visualiza los resultados en un mapa interactivo usando **Leaflet.js**.

**Tecnologías utilizadas:**
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- APIs: Nominatim (OpenStreetMap)
- Mapas: Leaflet.js
- Iconos: Lucide Icons

---

## Estructura del Proyecto
```
proyecto/
│
├── app.py                  # Servidor Flask (backend)
│
└── templates/              # Plantillas HTML
    ├── index.html          # Página de inicio
    └── map.html            # Página de búsqueda y mapa
```

---

## Explicación del Backend (app.py)

### 1. Importaciones
```python
from flask import Flask, render_template, request
import requests
```

- **Flask**: Clase principal para crear la aplicación web
- **render_template**: Renderiza plantillas HTML con datos dinámicos
- **request**: Accede a datos de formularios y peticiones HTTP
- **requests**: Realiza peticiones HTTP a APIs externas (Nominatim)

---

### 2. Inicialización de la Aplicación
```python
app = Flask(__name__)
```

- Crea la instancia de Flask
- `__name__` permite localizar carpetas `templates/` y `static/`

---

### 3. Ruta Principal (`/`)
```python
@app.route('/')
def index():
    return render_template('index.html')
```

- **Decorador `@app.route('/')`**: Define la URL raíz de la aplicación
- **Función `index()`**: Renderiza y devuelve `index.html` (página de bienvenida)

---

### 4. Ruta de Búsqueda (`/buscar`)
```python
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        lugar = request.form['lugar']
```

- Acepta **GET** (mostrar página) y **POST** (procesar búsqueda)
- `request.form['lugar']`: Extrae el nombre del lugar del formulario

---

### 5. Consulta a la API de Nominatim
```python
url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": lugar,           # Término de búsqueda
    "format": "json",     # Formato de respuesta
    "limit": 1            # Solo 1 resultado
}
headers = {
    "User-Agent": "Flask-Educational-App"  # Identificación requerida
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
```

- **GET request** a Nominatim para geocodificar el lugar
- **Headers User-Agent**: Nominatim requiere identificar la aplicación
- **response.json()**: Convierte respuesta JSON a diccionario Python

---

### 6. Procesamiento de Resultados
```python
if data:
    lat = data[0]['lat']
    lon = data[0]['lon']
    nombre = data[0]['display_name']
    
    return render_template('map.html', lat=lat, lon=lon, nombre=nombre)

return render_template('map.html', error="")
```

- Si hay resultados: extrae latitud, longitud y nombre
- Renderiza `map.html` pasando las variables como parámetros
- Si no hay resultados: renderiza `map.html` con error vacío

---

### 7. Ejecución del Servidor
```python
if __name__=='__main__':
    app.run(debug=True)
```

- **`if __name__=='__main__'`**: Solo ejecuta si el script se corre directamente
- **`debug=True`**: Modo desarrollo (recarga automática, errores detallados)
- ⚠️ **Nunca usar `debug=True` en producción**

---

## Explicación del Frontend

### Pantalla 1: Página de Inicio (index.html)

**Ubicación en el flujo:** Primera pantalla que ve el usuario al acceder a la aplicación (`/`)

**Funcionalidad:**
- Página de bienvenida que presenta la aplicación al usuario
- Muestra el título "Buscador de Lugares" en la barra de navegación
- Presenta un mensaje de bienvenida: "Bienvenido a Flask"
- Incluye una breve descripción del propósito educativo de la aplicación
- Contiene un botón principal llamado "Buscar un lugar en el mapa"

**Elementos visuales:**
- Barra de navegación superior con icono de mapa y título
- Sección central (hero) con diseño minimalista y centrado
- Botón destacado con icono de búsqueda y efecto hover
- Paleta de colores azul (#2563eb) como color principal
- Tipografía moderna (Raleway de Google Fonts)

**Flujo de navegación:**
1. Usuario accede a `http://localhost:5000/`
2. Flask renderiza y muestra `index.html`
3. Usuario lee la información de bienvenida
4. Usuario hace clic en el botón "Buscar un lugar en el mapa"
5. Redirige a la ruta `/buscar` (Pantalla 2)

---

<img width="1899" height="905" alt="image" src="https://github.com/user-attachments/assets/8364e035-603c-4ca6-9f90-6c588cc47b5a" />

---

### Pantalla 2: Página de Búsqueda y Mapa (map.html)

**Ubicación en el flujo:** Segunda pantalla accesible desde el botón de inicio (`/buscar`)

**Funcionalidad:**

Esta pantalla tiene múltiples funciones según el estado de la búsqueda:

#### Estado 1: Formulario vacío (GET inicial)
- Muestra la barra de navegación con un enlace "Volver al inicio"
- Presenta un formulario de búsqueda con un campo de texto
- Campo de entrada con placeholder "Ej. París, México..."
- Botón "Buscar" para enviar el formulario

#### Estado 2: Búsqueda en tiempo real (JavaScript)
- Al escribir en el campo (más de 3 caracteres), se activa el autocompletado
- Aparece una lista desplegable con hasta 5 sugerencias de lugares
- Las sugerencias se obtienen en tiempo real de la API Nominatim
- Cada sugerencia muestra el nombre completo del lugar con un icono
- Si no hay resultados, muestra mensaje "No se encontraron resultados"
- Usuario debe seleccionar una opción de la lista antes de enviar

#### Estado 3: Error de búsqueda
- Si el lugar no se encuentra, muestra un mensaje de error en rojo
- El mensaje indica: "No se encontró el lugar. Intenta con otro nombre o verifica la ortografía"
- El formulario permanece visible para intentar otra búsqueda

#### Estado 4: Resultado exitoso (Mapa visible)
- Muestra el formulario de búsqueda en la parte superior
- Debajo aparece una sección de resultados con el nombre completo del lugar encontrado
- Se renderiza un mapa interactivo de 500px de altura
- El mapa está centrado en las coordenadas del lugar (latitud y longitud)
- Incluye un marcador (pin) en la ubicación exacta
- Al hacer clic en el marcador, aparece un popup con el nombre del lugar
- El mapa es interactivo: permite zoom, arrastre y navegación

**Elementos técnicos:**
- **Formulario HTML** con método POST que envía datos a Flask
- **JavaScript** para autocompletado asíncrono con debounce de 400ms
- **Jinja2** para mostrar/ocultar elementos según datos de Flask
- **Leaflet.js** para renderizar el mapa interactivo
- **Tiles de OpenStreetMap** como capa base del mapa


**Validaciones:**
- El campo no puede estar vacío
- Debe seleccionarse una sugerencia válida de la lista
- Si no se selecciona, aparece alerta: "Debes seleccionar un lugar válido de la lista"

---

<img width="1876" height="904" alt="image" src="https://github.com/user-attachments/assets/dad5a433-cd3a-485c-96a8-d9544f1ae099" />

---

## Conceptos Clave

### Flask
- **Rutas**: URLs que definen puntos de acceso (`@app.route()`)
- **Métodos HTTP**: GET (obtener), POST (enviar datos)
- **render_template**: Combina Python con HTML dinámico

### Jinja2 (Motor de Plantillas)
- **`{{ variable }}`**: Imprime valores de Python en HTML
- **`{% if ... %}`**: Condicionales para mostrar/ocultar contenido
- **`| tojson`**: Filtro que convierte Python a JSON seguro

### APIs y Peticiones
- **request.form**: Accede a datos de formularios
- **requests.get()**: Realiza peticiones HTTP a APIs externas
- **response.json()**: Convierte respuesta JSON a diccionario

### Frontend
- **Leaflet.js**: Librería para mapas interactivos
- **Fetch API**: Peticiones asíncronas en JavaScript para autocompletado
- **Event Listeners**: Manejo de eventos del usuario (input, click, submit)

---

## Conclusión

Esta aplicación demuestra la integración completa de:
- **Backend Flask** que maneja rutas y lógica del servidor
- **API externa (Nominatim)** para geocodificación
- **Frontend dinámico** con Jinja2 y JavaScript
- **Visualización de datos** en mapas interactivos con Leaflet
- **Experiencia de usuario fluida** con autocompletado y validaciones

Es un ejemplo educativo perfecto para entender cómo Flask conecta Python con la web, maneja peticiones HTTP, consume APIs externas y renderiza interfaces dinámicas.
