# Odoo Mountrix Technical Test

Bienvenido al repositorio **odoo-mountrix-technical-test**.  
Este proyecto contiene un add-on para Odoo, desarrollado como parte de una prueba técnica.  
El objetivo es demostrar conocimientos en desarrollo de módulos Odoo, buenas prácticas de organización y documentación.

---

## Tabla de Contenido

- [Descripción General](#descripción-general)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Descripción General

Este módulo de Odoo permite comparar eficientemente las cotizaciones de diferentes proveedores para facilitar la toma de decisiones en el proceso de compras.
Características principales:

* Comparación lado a lado de cotizaciones de proveedores
* Análisis de precios con identificación automática de las mejores ofertas
* Ranking de proveedores por monto total y tiempo de entrega
* Reporte comparativo en formato PDF con análisis detallado
* Interfaz integrada en las órdenes de compra para acceso rápido
* Optimización automática que identifica la mejor combinación de precios por producto

#### Funcionalidad:
El módulo extiende las órdenes de compra de Odoo agregando un botón "Comparison" que abre una vista comparativa de todas las cotizaciones recibidas para un mismo acuerdo de compra, permitiendo evaluar fácilmente precios, fechas de entrega y condiciones de cada proveedor.

---

## Requisitos

- **Docker** y **Docker Compose** instalados en tu sistema  
  - [Guía de instalación de Docker](https://docs.docker.com/get-docker/)
  - [Guía de instalación de Docker Compose](https://docs.docker.com/compose/install/)

---

## Instalación

Sigue estos pasos para instalar y activar el módulo:

1. **Clona este repositorio en tu computadora o servidor Odoo:**
   ```bash
   git clone https://github.com/ka-dm/odoo-mountrix-technical-test.git
   ```
2. **Entra al directorio del proyecto:**
   ```bash
   cd odoo-mountrix-technical-test
   ```
3. **Levanta el entorno con Docker Compose:**
   ```bash
   docker-compose up -d
   ```
4. **Accede a la instancia de Odoo:**  
   Abre tu navegador y entra a [http://localhost:8069](http://localhost:8069)

5. **Busca el módulo por su nombre *purchase_rfq_comparator* en Odoo Apps y haz clic en **Instalar**.

---

## Configuración

Después de instalar el módulo:

1. Accede al menú correspondiente creado por el módulo.
2. Configura los parámetros iniciales si aplica (por ejemplo, permisos, reglas de acceso, datos maestros, etc.).

---

## Uso

A continuación, se describe paso a paso cómo utilizar el módulo:

1. **Acceso inicial:**  
   [Describe el acceso al menú o funcionalidad principal]

2. **Flujo básico de uso:**  
   1. [Primer paso: por ejemplo, crear un registro]
   2. [Segundo paso: editar o procesar información]
   3. [Tercer paso: visualizar resultados, reportes, etc.]

3. **Funciones avanzadas:**  
   [Opcional: Describe cualquier funcionalidad adicional o avanzada]

---

## Capturas de Pantalla

A continuación, se muestran capturas de pantalla que ilustran el funcionamiento del módulo paso a paso:

> **INSTRUCCIONES:**  
> Inserta aquí tus capturas de pantalla siguiendo el flujo de uso.  
> Ejemplo:
>
> 1. **Instalación del módulo desde Apps**
>    ![image1](image1)
>
> 2. **Acceso al menú principal**
>    ![image2](image2)
>
> 3. **Creación de un registro**
>    ![image3](image3)
>
> 4. **Visualización de resultados**
>    ![image4](image4)
>
> [Agrega tantas imágenes como sea necesario para cubrir el flujo completo]

---

## Estructura del Repositorio

```
odoo-mountrix-technical-test/
│
├── extra-addons/
│   └── purchase_rfq_comparator/
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── controllers/
│       │   ├── __init__.py
│       │   └── controllers.py
│       ├── demo/
│       │   └── demo.xml
│       ├── models/
│       │   ├── __init__.py
│       │   ├── filename.py
│       │   └── purchase_requisition.py
│       ├── report/
│       │   ├── report_purchase_rfq_comparator_action.xml
│       │   └── report_purchase_rfq_comparator_template.xml
│       ├── security/
│       │   └── ir.model.access.csv
│       ├── static/
│       │   └── src/
│       │       ├── img/
│       │       │   ├── data-analysis.png
│       │       │   ├── fast-delivery.png
│       │       │   └── savings.png
│       │       ├── js/
│       │       │   └── report.js
│       │       └── xml/
│       │           └── report.xml
│       └── views/
│           └── purchase_requisition_views.xml
├── docker-compose.yml
├── odoo.conf
├── README.md
└── ...
```

- **purchase_rfq_comparator/**: Carpeta principal del add-on.
- **__manifest__.py**: Archivo de declaración del módulo.
- **models/**: Definición de modelos y lógica de negocio.
- **views/**: Vistas, menús y acciones del módulo.
- **docker-compose.yml**: Archivo para levantar el entorno de Odoo y sus dependencias con Docker.
- **README.md**: Este archivo de documentación.
