Producci-n-Software/
│
├── app.py                  → Punto de entrada de la aplicación.
│                              Inicializa el servidor y define las rutas principales.
│
├── scraper.py              → Módulo de lógica externa.
│                              Encapsula funciones de extracción y procesamiento de datos.
│
├── templates/              → Capa de presentación (vistas HTML).
│                              Contiene las páginas renderizadas al usuario.
│
├── static/                 → Recursos estáticos del sistema.
│   ├── css/
│   │   └── style.css       → Hojas de estilo para el diseño visual.
│   ├── js/                 → Scripts JavaScript para interactividad.
│   └── img/                → Recursos gráficos (imágenes, íconos).
│
├── data/                   → Persistencia local de datos.
│   ├── users.csv           → Archivo de datos estructurado en formato CSV.
│   └── usuarios.json       → Archivo de datos estructurado en formato JSON.
│
├── instance/               → Configuración específica del entorno.
│                              Puede contener variables sensibles o configuraciones locales.
│
├── requirements.txt        → Dependencias del proyecto.
│                              Librerías necesarias para ejecutar la aplicación.
│
└── README.md               → Documentación general del proyecto.
                               Instrucciones de instalación y uso.
