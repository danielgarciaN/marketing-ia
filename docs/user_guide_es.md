# Guia de uso - AI Marketing Intelligence Platform

## Que es

AI Marketing Intelligence Platform es una plataforma de analitica de marketing para ecommerce. Convierte datos transaccionales de clientes en un dashboard de negocio con segmentacion RFM, clustering, recomendaciones de campanas, insights automaticos y simulacion de ROI.

El objetivo es responder preguntas como:

- Quienes son los mejores clientes.
- Que clientes estan en riesgo de abandono.
- Que segmentos generan mas ingresos.
- Que campana conviene enviar a cada segmento.
- Como evoluciona el revenue.
- Que acciones pueden mejorar retencion, upsell y reactivacion.

## Como funciona por dentro

El flujo principal es:

1. `generate_dataset.py` genera un dataset ecommerce con estructura tipo Online Retail.
2. `app/ml/preprocess.py` limpia transacciones invalidas.
3. `app/ml/rfm.py` calcula Recency, Frequency, Monetary, ticket medio y segmentos de negocio.
4. `app/ml/clustering.py` entrena KMeans y genera coordenadas PCA para visualizar clusters.
5. `app/ml/train_model.py` guarda CSV/JSON procesados y artefactos `.joblib`.
6. FastAPI expone los resultados mediante endpoints REST.
7. Next.js consume la API y muestra el portal visual.

## Como arrancar todo

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

## Como subir otro dataset desde la plataforma

El portal incluye una pantalla llamada:

```text
Data / Datos
```

Desde esa pantalla puedes:

1. Seleccionar un archivo CSV o Excel.
2. Ver una inferencia automatica de columnas.
3. Corregir el mapping si tu export usa nombres distintos.
4. Ajustar pesos RFM, dias activo/inactivo y numero de clusters.
5. Decidir si quieres reentrenar automaticamente despues de subirlo.
6. Subir el dataset.
7. Ver el estado del dataset raw y los datos procesados.
8. Reentrenar manualmente el dataset actual.

La plataforma normaliza internamente a estas columnas:

```text
InvoiceNo
StockCode
Description
Quantity
InvoiceDate
UnitPrice
CustomerID
Country
Revenue
```

Tu archivo no tiene que usar exactamente esos nombres. Por ejemplo, puede tener `order_id`, `created_at`, `customer_email`, `sku`, `qty` o `total_price`. La pantalla de Datos intentara mapearlos automaticamente.

Campos minimos:

- ID de pedido o factura.
- ID de cliente o email.
- Fecha de compra.
- Cantidad.
- Precio unitario o revenue total.

Campos opcionales que mejoran el analisis:

- SKU o producto.
- Descripcion de producto.
- Pais o mercado.

Cuando subes un archivo con `Retrain after upload` activado, el backend hace esto:

1. Lee CSV/XLSX.
2. Detecta columnas y tipos de datos.
3. Aplica el mapping elegido en el portal.
4. Normaliza el dataset al esquema interno.
5. Guarda el CSV canonico en `backend/app/data/raw/online_retail.csv`.
6. Ejecuta el pipeline completo de entrenamiento.
7. Regenera los CSV/JSON procesados.
8. Recarga los datos en memoria.
9. El frontend refresca el dashboard.

Endpoints usados:

```text
GET  /data/status
GET  /data/config
POST /data/config
POST /data/infer-schema
POST /data/upload
POST /data/retrain
```

Tambien puedes probarlos desde:

```text
http://localhost:8000/docs
```

## RFM configurable

En la pantalla `Data / Datos` puedes ajustar:

- Peso de Recency.
- Peso de Frequency.
- Peso de Monetary.
- Dias para considerar un cliente activo.
- Dias para considerar un cliente inactivo.
- Numero de clusters KMeans.
- Auto-seleccion de `k` por silhouette.

Esto permite adaptar el modelo a distintos negocios. Por ejemplo:

- Ecommerce de moda: dar mas peso a recency porque la recompra reciente importa mucho.
- B2B: dar mas peso a monetary porque hay menos pedidos pero tickets altos.
- Suscripcion o consumibles: dar mas peso a frequency para detectar recurrencia.

Cuando cambias estos valores y pulsas `Reentrenar dataset actual`, se regeneran segmentos, KPIs, clusters, insights y simulador sobre la nueva configuracion.

## Como regenerar datos y modelo desde terminal

Solo hace falta si cambias el dataset, reglas RFM, clustering o quieres refrescar los datos sin usar la pantalla Data:

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

## Moneda: libras o euros

El dataset base usa importes con logica de libras (`GBP`), porque imita el dataset Online Retail original de ecommerce UK.

El portal permite cambiar la visualizacion a euros desde el selector superior:

```text
GBP | EUR
```

Tambien hay un control en la pantalla `Data / Datos`.

Que hace este cambio:

- Convierte visualmente KPIs, revenue, ticket medio, clientes, segmentos, clustering, simulador e importes de insights.
- No modifica el CSV original.
- No reentrena el modelo.
- Mantiene la misma escala de negocio, solo cambia la moneda mostrada.

La conversion actual usa una tasa fija definida en el frontend:

```text
1 GBP = 1.16 EUR
```

Si quieres cambiarla, edita:

```text
frontend/lib/format.ts
```

## Idioma del portal

En la parte superior derecha del portal hay un selector:

```text
EN | ES
```

Sirve para cambiar la interfaz entre ingles y espanol. Traduce navegacion, titulos, KPIs, etiquetas, segmentos, campanas, prioridades, metodologia y textos principales del simulador.

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
- Distribucion de clientes.

### Data / Datos

Sirve para gestionar el dataset:

- Subir un nuevo CSV o Excel.
- Detectar columnas automaticamente.
- Corregir mapping de columnas.
- Configurar pesos RFM.
- Configurar dias activo/inactivo.
- Configurar clusters KMeans.
- Reentrenar el pipeline.
- Ver estado de dataset raw y procesado.
- Consultar columnas internas del modelo.
- Cambiar visualizacion GBP/EUR.

### Customers / Clientes

Muestra una tabla de clientes ordenada por revenue:

- CustomerID.
- Pais.
- Segmento.
- Revenue.
- Frecuencia.
- Recency.
- Cluster.

### Segments / Segmentos

Muestra segmentos RFM como:

- Clientes VIP.
- Clientes fieles.
- Clientes nuevos.
- Clientes en riesgo.
- Clientes perdidos.
- Compradores ocasionales.
- Alto potencial.

Al seleccionar un segmento se ven metricas y campanas recomendadas.

### Clustering

Muestra la parte de Machine Learning:

- Numero de clusters.
- Silhouette score.
- Inertia.
- Scatter plot PCA.

### Campaigns / Campanas

Incluye un simulador donde eliges:

- Segmento objetivo.
- Canal de campana.
- Presupuesto.
- Descuento.
- Conversion esperada.

Devuelve:

- Ingresos estimados.
- ROI.
- Clientes alcanzados.
- Conversiones esperadas.
- Recomendacion final.

### Insights

Genera insights automaticos orientados a negocio:

- Concentracion de revenue en VIP.
- Riesgo de churn.
- Conversion de nuevos clientes.
- Recuperacion de clientes perdidos.
- Tendencia de revenue.
- Oportunidades de upsell.

### Methodology / Metodologia

Resume el enfoque tecnico:

- Limpieza de datos.
- RFM.
- KMeans + PCA.
- Activacion mediante campanas e insights.

## Endpoints principales

```text
GET  /data/status
GET  /data/config
POST /data/config
POST /data/infer-schema
POST /data/upload
POST /data/retrain
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

## Como presentarlo en portfolio

Puedes describirlo asi:

> Plataforma de Marketing Intelligence que permite subir datos ecommerce, recalcular segmentacion RFM, entrenar clustering, simular campanas y generar insights accionables para equipos CRM.

Puntos fuertes para explicar:

- No es solo un notebook: tiene backend, API y frontend.
- Permite subir nuevos datasets desde el portal.
- El pipeline es reproducible.
- Las metricas tienen interpretacion de negocio.
- Las campanas se conectan con segmentos.
- Hay simulador de impacto economico.
- El producto es bilingue ES/EN.
- Permite visualizar importes en GBP o EUR.

## Limitaciones actuales

- El dataset base es sintetico, aunque replica la estructura de Online Retail.
- Los insights son reglas de negocio, no LLM real.
- El MVP usa CSV/JSON en vez de base de datos.
- El simulador estima ROI con supuestos, no con experimentos A/B reales.
- La conversion GBP/EUR usa una tasa fija en frontend.

## Proximos pasos recomendados

- Anadir base de datos PostgreSQL o Supabase.
- Permitir mapeo de columnas en la subida de CSV.
- Integrar datos reales de Shopify, WooCommerce o CRM.
- Anadir autenticacion.
- Anadir LLM para reescribir insights con tono ejecutivo.
- Usar una API de tipo de cambio para GBP/EUR.
- Desplegar frontend en Vercel y backend en Render/Railway.
