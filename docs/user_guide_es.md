# Guía de uso - AI Marketing Intelligence Platform

## Qué es

AI Marketing Intelligence Platform es una plataforma de analítica de marketing para ecommerce. Convierte datos transaccionales de clientes en un dashboard de negocio con segmentación RFM, clustering, recomendaciones de campañas, insights automáticos y simulación de ROI.

El objetivo es responder preguntas como:

- Quiénes son los mejores clientes.
- Qué clientes están en riesgo de abandono.
- Qué segmentos generan más ingresos.
- Qué campaña conviene enviar a cada segmento.
- Cómo evoluciona el revenue.
- Qué acciones pueden mejorar retención, upsell y reactivación.

## Cómo funciona por dentro

El flujo principal es:

1. `generate_dataset.py` genera un dataset ecommerce con estructura tipo Online Retail.
2. `app/ml/preprocess.py` limpia transacciones inválidas.
3. `app/ml/rfm.py` calcula Recency, Frequency, Monetary, ticket medio y segmentos de negocio.
4. `app/ml/clustering.py` entrena KMeans y genera coordenadas PCA para visualizar clusters.
5. `app/ml/train_model.py` guarda CSV/JSON procesados y artefactos `.joblib`.
6. FastAPI expone los resultados mediante endpoints REST.
7. Next.js consume la API y muestra el portal visual.

## Estructura importante

```text
files/
  backend/
    generate_dataset.py
    app/
      main.py
      api/
      services/
      ml/
      data/
        raw/
        processed/
      artifacts/
  frontend/
    app/
    components/
    lib/
  docs/
```

## Cómo arrancar todo

Abre PowerShell en:

```powershell
cd C:\Users\Daniel\Desktop\Proyectos\marketing-ia
```

Activa el entorno correcto:

```powershell
.\.venv311\Scripts\activate
```

### 1. Backend

En una terminal:

```powershell
cd files\backend
..\..\.venv311\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Comprueba la API en:

```text
http://localhost:8000/docs
```

### 2. Frontend

En otra terminal:

```powershell
cd C:\Users\Daniel\Desktop\Proyectos\marketing-ia\files\frontend
npm run dev
```

Abre el portal en:

```text
http://localhost:3000
```

## Cómo regenerar datos y modelo

Solo hace falta si cambias el dataset, reglas RFM, clustering o quieres refrescar los datos:

```powershell
cd C:\Users\Daniel\Desktop\Proyectos\marketing-ia\files\backend
..\..\.venv311\Scripts\python.exe .\generate_dataset.py
..\..\.venv311\Scripts\python.exe -m app.ml.train_model
```

Esto actualiza:

- `app/data/raw/online_retail.csv`
- `app/data/processed/online_retail_clean.csv`
- `app/data/processed/customers_rfm.csv`
- `app/data/processed/dashboard_summary.json`
- `app/data/processed/revenue_monthly.json`
- `app/data/processed/segment_summary.json`
- `app/data/processed/model_metrics.json`
- `app/artifacts/kmeans_model.joblib`
- `app/artifacts/scaler.joblib`
- `app/artifacts/pca.joblib`

## Idioma del portal

En la parte superior derecha del portal hay un selector:

```text
EN | ES
```

Sirve para cambiar la interfaz entre inglés y español. Traduce navegación, títulos, KPIs, etiquetas, segmentos, campañas, prioridades, metodología y textos principales del simulador.

Algunos textos largos que vienen generados por el backend pueden mantenerse parcialmente en inglés si contienen narrativa dinámica. La arquitectura permite extenderlo después con endpoints localizados o traducción mediante LLM.

## Pantallas del portal

### Overview / Resumen

Muestra KPIs ejecutivos:

- Clientes totales.
- Ingresos totales.
- Pedidos.
- Ticket medio.
- Clientes activos.
- Clientes inactivos.
- Revenue mensual.
- Revenue por segmento.
- Distribución de clientes.

Sirve para una lectura rápida del estado del negocio.

### Customers / Clientes

Muestra una tabla de clientes ordenada por revenue:

- CustomerID.
- País.
- Segmento.
- Revenue.
- Frecuencia.
- Recency.
- Cluster.

Sirve para identificar clientes de alto valor o clientes que deberían recibir acciones CRM específicas.

### Segments / Segmentos

Muestra segmentos RFM como:

- Clientes VIP.
- Clientes fieles.
- Clientes nuevos.
- Clientes en riesgo.
- Clientes perdidos.
- Compradores ocasionales.
- Alto potencial.

Al seleccionar un segmento se ven métricas y campañas recomendadas.

### Clustering

Muestra la parte de Machine Learning:

- Número de clusters.
- Silhouette score.
- Inertia.
- Scatter plot PCA.

Sirve para explicar que, además de reglas RFM, se usa clustering para descubrir patrones de comportamiento.

### Campaigns / Campañas

Incluye un simulador donde eliges:

- Segmento objetivo.
- Canal de campaña.
- Presupuesto.
- Descuento.
- Conversión esperada.

Devuelve:

- Ingresos estimados.
- ROI.
- Clientes alcanzados.
- Conversiones esperadas.
- Recomendación final.

### Insights

Genera insights automáticos orientados a negocio:

- Concentración de revenue en VIP.
- Riesgo de churn.
- Conversión de nuevos clientes.
- Recuperación de clientes perdidos.
- Tendencia de revenue.
- Oportunidades de upsell.

Sirve como capa narrativa para presentar acciones recomendadas.

### Methodology / Metodología

Resume el enfoque técnico:

- Limpieza de datos.
- RFM.
- KMeans + PCA.
- Activación mediante campañas e insights.

Es útil para portfolio porque explica las decisiones técnicas sin abrir el código.

## Endpoints principales

```text
GET  /dashboard/summary
GET  /dashboard/revenue
GET  /customers
GET  /customers/{id}
GET  /segments
GET  /segments/{name}
GET  /campaigns/recommendations
POST /campaigns/simulate
GET  /insights
GET  /model/metrics
GET  /model/clusters
GET  /model/cluster-points
```

Puedes probarlos desde:

```text
http://localhost:8000/docs
```

## Cómo presentarlo en portfolio

Puedes describirlo así:

> Plataforma de Marketing Intelligence que combina análisis RFM, segmentación de clientes, clustering con KMeans, recomendaciones de campañas e insights automáticos para ayudar a equipos CRM/ecommerce a priorizar acciones de retención, upsell y reactivación.

Puntos fuertes para explicar:

- No es solo un notebook: tiene backend, API y frontend.
- El pipeline es reproducible.
- Las métricas tienen interpretación de negocio.
- Las campañas se conectan con segmentos.
- Hay simulador de impacto económico.
- El producto es bilingüe ES/EN.

## Limitaciones actuales

- El dataset es sintético, aunque replica la estructura de Online Retail.
- Los insights son reglas de negocio, no LLM real.
- El MVP usa CSV/JSON en vez de base de datos.
- El simulador estima ROI con supuestos, no con experimentos A/B reales.

## Próximos pasos recomendados

- Añadir base de datos PostgreSQL o Supabase.
- Integrar datos reales de Shopify, WooCommerce o CRM.
- Añadir autenticación.
- Añadir traducción completa del backend por `?locale=es`.
- Añadir LLM para reescribir insights con tono ejecutivo.
- Desplegar frontend en Vercel y backend en Render/Railway.
