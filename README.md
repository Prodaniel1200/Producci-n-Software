# 🎓 CONIITI 2026 — Sistema Web de Gestión de Agenda

Aplicación web desarrollada con **Flask** para la gestión y visualización de la agenda del **Congreso Internacional de Ingeniería, Tecnología e Innovación (CONIITI)**. Permite a los asistentes consultar eventos, ponentes y reservar sesiones directamente en su calendario de Outlook.

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Rutas de la Aplicación](#rutas-de-la-aplicación)
- [Módulos Principales](#módulos-principales)
- [Integración con Microsoft Outlook](#integración-con-microsoft-outlook)
- [Base de Datos (CSV)](#base-de-datos-csv)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Créditos](#créditos)

---

## 📖 Descripción General

Este sistema fue desarrollado como proyecto académico en la **Universidad Católica de Colombia** para centralizar la información del congreso CONIITI. Los usuarios registrados pueden:

- Consultar la agenda oficial con eventos, fechas, modalidades y sedes.
- Ver el listado de ponentes nacionales e internacionales con sus banderas de país.
- Reservar ponencias directamente en su calendario de **Microsoft Outlook** a través de la API de Microsoft Graph.
- Navegar por el contenido del sitio oficial de CONIITI (vía scraping).

---

## ✨ Características

- **Autenticación de usuarios** con Flask-Login (registro, inicio de sesión, cierre de sesión).
- **Agenda paginada** con información detallada de cada evento (fecha, hora, tipo, modalidad, sede y salón).
- **Ponentes internacionales** con representación visual de su bandera de país.
- **Reserva en Outlook** — integración con Microsoft Graph API para crear eventos en el calendario del usuario, con alarma de 15 minutos antes.
- **Scraping de CONIITI** — extracción automática de información desde el sitio oficial `coniiti.com`.
- **Interfaz responsiva** usando Bootstrap 5 con identidad visual institucional (colores de la Universidad Católica).
- **Modal de confirmación** al realizar una reserva exitosa.

---

## 🗂️ Estructura del Proyecto

```
Produccion-Software/
│
├── app.py                        # Punto de entrada — rutas y lógica principal
├── scraper.py                    # Módulo de scraping del sitio oficial CONIITI
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Documentación del proyecto
│
├── templates/                    # Vistas HTML (Jinja2)
│   ├── base.html                 # Plantilla base con navbar
│   ├── login.html                # Formulario de inicio de sesión
│   ├── register.html             # Formulario de registro
│   ├── inicio.html               # Página de bienvenida
│   ├── agenda.html               # Agenda de eventos y ponentes
│   ├── coniiti.html              # Información scrapeada del sitio oficial
│   ├── dashboard.html            # Panel de usuario
│   ├── pagina1.html              # Página de contenido adicional
│   ├── acerca.html               # Página "Acerca de"
│   └── contacto.html             # Página de contacto
│
├── static/                       # Recursos estáticos
│   ├── css/
│   │   ├── style.css             # Estilos principales (Bootstrap + institucional)
│   │   └── login.css             # Estilos específicos del login
│   ├── js/
│   │   └── scripts.js            # Lógica frontend (reserva Outlook, modal)
│   ├── logos/
│   │   ├── ucat.png              # Escudo Universidad Católica
│   │   ├── coniiti.png           # Logo CONIITI
│   │   └── ucat-coniiti.png      # Imagen combinada para inicio
│   └── banderas/                 # Imágenes de banderas por país
│       ├── colombia.png
│       ├── mexico.png
│       ├── argentina.png
│       ├── alemania.png
│       ├── francia.png
│       ├── brasil.png
│       └── panama.png
│
├── data/                         # Persistencia local de datos
│   ├── users.csv                 # Registro de usuarios (email, nombre, contraseña)
│   └── usuarios.json             # Versión JSON del registro de usuarios
│
└── instance/                     # Configuración de entorno (variables locales/sensibles)
```

---

## ✅ Requisitos Previos

- **Python 3.8+**
- **pip**
- Cuenta de **Microsoft Azure** (solo si se desea activar la integración con Outlook)
- Conexión a internet (para el scraping de CONIITI y las banderas)

---

## 🚀 Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/Produccion-Software.git
cd Produccion-Software
```

**2. Crear y activar un entorno virtual**

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Ejecutar la aplicación**

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

---

## ⚙️ Configuración

### Variables principales en `app.py`

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `app.secret_key` | Clave secreta para sesiones Flask | `"secretkey123"` ⚠️ Cambiar en producción |
| `CLIENT_ID` | ID de la aplicación en Azure AD | `'TU_CLIENT_ID'` |
| `CLIENT_SECRET` | Secreto de cliente de Azure | `'TU_SECRET_VALOR'` |
| `TENANT_ID` | ID del tenant de Azure AD | `'TU_TENANT_ID'` |

> ⚠️ **Importante:** Nunca subas claves reales al repositorio. Usa variables de entorno o un archivo `.env` con `python-dotenv` en producción.

### Usuarios de prueba incluidos

| Email | Contraseña |
|---|---|
| `nslopez90@ucatolica.edu.co` | `12345` |
| `jperez@example.com` | `12345` |

---

## 💻 Uso

### Flujo básico

1. Acceder a `http://127.0.0.1:5000` — redirige automáticamente al login.
2. Iniciar sesión con un usuario existente o registrar uno nuevo.
3. En la página de **Inicio**, hacer clic en **"Ver Agenda"**.
4. En la **Agenda**, explorar los eventos y ponentes.
5. Hacer clic en **"Reservar en Outlook"** para programar un evento en el calendario personal.
   - Si no se ha vinculado una cuenta Microsoft, se redirige al flujo de autenticación OAuth.
6. Al confirmar la reserva, aparece un **modal** con los detalles del evento agendado.

---

## 🗺️ Rutas de la Aplicación

| Método | Ruta | Descripción | Protegida |
|---|---|---|---|
| GET | `/` | Redirige a `/inicio` | ✅ |
| GET/POST | `/login` | Inicio de sesión | ❌ |
| GET/POST | `/register` | Registro de usuario | ❌ |
| GET | `/logout` | Cerrar sesión | ✅ |
| GET | `/inicio` | Página de bienvenida | ✅ |
| GET | `/agenda` | Agenda de eventos y ponentes | ✅ |
| GET | `/coniiti` | Info scrapeada de CONIITI | ✅ |
| GET | `/api/coniiti` | Endpoint JSON con datos de CONIITI | ✅ |
| GET | `/login-outlook` | Iniciar OAuth con Microsoft | ✅ |
| GET | `/callback` | Callback OAuth de Microsoft | — |
| POST | `/crear-evento` | Crear evento en Outlook | ✅ |
| GET | `/acerca` | Página "Acerca de" | ❌ |
| GET | `/contacto` | Página de contacto | ❌ |

---

## 🧩 Módulos Principales

### `app.py`
Archivo central de la aplicación. Contiene:
- Inicialización de Flask y Flask-Login.
- Carga de usuarios desde `data/users.csv`.
- Definición de todas las rutas (vistas y API).
- Lógica de la agenda con datos de ponentes y eventos.
- Integración con Microsoft Graph API para creación de eventos en Outlook.

### `scraper.py`
Módulo independiente de extracción de datos. Realiza:
- Petición HTTP al sitio oficial `https://coniiti.com/`.
- Parsing del HTML con **BeautifulSoup**.
- Extracción de bloques de eventos (título, tipo, ponente, país, fecha, hora).
- Retorna una lista de diccionarios lista para ser usada en las vistas.

### `static/js/scripts.js`
Lógica frontend para la funcionalidad de reserva:
- `reservarEnOutlook(titulo, ponente, horaStr)` — construye el objeto de evento y lo envía al servidor Flask vía `fetch`.
- `mostrarModalExito(datos)` — genera dinámicamente el contenido del modal de confirmación.
- `cerrarModal()` — oculta el modal.

---

## 📅 Integración con Microsoft Outlook

La aplicación utiliza **MSAL (Microsoft Authentication Library)** y la **Microsoft Graph API** para crear eventos en el calendario del usuario.

### Flujo de autenticación OAuth 2.0

```
Usuario → /login-outlook → Microsoft Login → /callback → Token guardado en sesión → /crear-evento
```

### Configuración en Azure Portal

1. Ir a [portal.azure.com](https://portal.azure.com) → **Azure Active Directory** → **Registros de aplicaciones**.
2. Crear una nueva aplicación y copiar el **Application (client) ID** y el **Directory (tenant) ID**.
3. En **Certificados y secretos**, crear un nuevo secreto de cliente.
4. En **Permisos de API**, agregar: `Calendars.ReadWrite` y `User.Read` (Microsoft Graph).
5. En **Autenticación**, agregar la URI de redireccionamiento: `http://127.0.0.1:5000/callback`.
6. Actualizar `CLIENT_ID`, `CLIENT_SECRET` y `TENANT_ID` en `app.py`.

### Estructura del evento creado en Outlook

```json
{
  "subject": "Título de la ponencia",
  "body": { "contentType": "HTML", "content": "Ponente: ... Lugar: ..." },
  "start": { "dateTime": "YYYY-MM-DDTHH:MM:SS", "timeZone": "SA Pacific Standard Time" },
  "end": { "dateTime": "YYYY-MM-DDTHH:MM:SS", "timeZone": "SA Pacific Standard Time" },
  "location": { "displayName": "Auditorio / Universidad Católica" },
  "isReminderOn": true,
  "reminderMinutesBeforeStart": 15
}
```

---

## 🗄️ Base de Datos (CSV)

Los usuarios se almacenan en `data/users.csv` con el siguiente formato:

```csv
name,email,password
Nicolas Lopez,nslopez90@ucatolica.edu.co,12345
Juan Pérez,jperez@example.com,12345
```

> ⚠️ Las contraseñas se almacenan en texto plano. Para un entorno de producción, se recomienda implementar hashing con `werkzeug.security` o `bcrypt`.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| **Python 3** | Lenguaje principal |
| **Flask** | Framework web backend |
| **Flask-Login** | Gestión de autenticación y sesiones |
| **MSAL** | Autenticación con Microsoft Azure AD |
| **BeautifulSoup4** | Scraping del sitio oficial CONIITI |
| **Requests** | Peticiones HTTP (scraping y Graph API) |
| **Bootstrap 5** | Framework CSS responsivo |
| **Jinja2** | Motor de plantillas HTML |
| **JavaScript (Vanilla)** | Lógica de reserva y modal en el frontend |
| **CSV** | Persistencia de usuarios |

---

## 👥 Créditos

Desarrollado por estudiantes de la **Universidad Católica de Colombia** como proyecto de la asignatura **Producción de Software**.


---

## 📄 Licencia

Este proyecto es de uso académico. Para cualquier uso externo, contactar a los autores.
