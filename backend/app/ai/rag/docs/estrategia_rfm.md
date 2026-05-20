# Estrategia RFM para Ecommerce — Guía Completa

## ¿Qué es el análisis RFM?

RFM es un modelo de segmentación de clientes basado en tres dimensiones del comportamiento de compra:

- **Recencia (R)**: ¿Cuántos días han pasado desde la última compra del cliente?
- **Frecuencia (F)**: ¿Cuántas veces ha comprado en el período analizado?
- **Monetario (M)**: ¿Cuánto dinero ha gastado en total?

El análisis RFM permite clasificar a los clientes de forma objetiva y priorizar acciones de marketing según el valor real de cada segmento.

## Cómo se calculan las puntuaciones RFM

Cada dimensión se puntúa de 1 a 5:

| Puntuación | Recencia | Frecuencia | Monetario |
|---|---|---|---|
| 5 (mejor) | Compró hace pocos días | Compra muy frecuentemente | Gasta mucho |
| 4 | Compró recientemente | Compra con frecuencia | Gasta bastante |
| 3 | Compra moderada | Frecuencia media | Gasto medio |
| 2 | Lleva tiempo sin comprar | Compra poco | Gasto bajo |
| 1 (peor) | Inactivo por mucho tiempo | Casi no compra | Apenas gasta |

La puntuación total RFM = R_Score + F_Score + M_Score (rango: 3–15)

## Segmentos RFM estándar y sus características

### 1. VIP Customers (Clientes VIP)
- **Perfil**: R≥4, F≥4, M≥4
- **Comportamiento**: Compran frecuentemente, gastaron mucho y recientemente
- **Valor de negocio**: Generan el 60–80% de los ingresos siendo solo el 5–10% de la base
- **Churn risk**: Bajo. Son los más fieles.
- **Acción recomendada**: Programas de lealtad exclusivos, acceso anticipado a productos, atención VIP

### 2. Loyal Customers (Clientes Leales)
- **Perfil**: F≥4, M≥3, R≥3
- **Comportamiento**: Alta frecuencia de compra, buen volumen de gasto
- **Valor de negocio**: Base sólida del negocio, candidatos a convertirse en VIP
- **Acción recomendada**: Upgrades de programa de fidelización, cross-selling, upselling

### 3. New Customers (Nuevos Clientes)
- **Perfil**: R=5, F=1, M variable
- **Comportamiento**: Primera o segunda compra reciente
- **Valor de negocio**: Alto potencial si se convierten en recurrentes
- **Acción recomendada**: Onboarding personalizado, descuento en segunda compra, educación de producto

### 4. At-Risk (En Riesgo)
- **Perfil**: R≤2, F≥3, M≥3
- **Comportamiento**: Solían comprar mucho pero llevan 60–120 días sin aparecer
- **Valor de negocio**: Crítico — tienen historial de valor alto pero están abandonando
- **Churn risk**: Alto
- **Acción recomendada**: Campaña de win-back urgente, encuesta de satisfacción, oferta especial personalizada

### 5. Lost Customers (Clientes Perdidos)
- **Perfil**: R=1, F=1–2, M=1–2
- **Comportamiento**: Más de 180 días sin comprar, bajo historial
- **Valor de negocio**: Bajo, pero recuperables con el mensaje correcto
- **Acción recomendada**: Campaña de reactivación de bajo coste, pregunta directa si quieren darse de baja

### 6. Occasional Buyers (Compradores Ocasionales)
- **Perfil**: R=3, F=2, M=3
- **Comportamiento**: Compran esporádicamente, sin patrón claro
- **Valor de negocio**: Medio — potencial de conversión a leales
- **Acción recomendada**: Identificar qué los motiva a comprar, campañas de activación basadas en comportamiento

### 7. High Potential (Alto Potencial)
- **Perfil**: R≥4, M≥4, F=2–3
- **Comportamiento**: Gasto alto por transacción pero baja frecuencia
- **Valor de negocio**: Alto — si aumentan frecuencia, se convierten en VIP
- **Acción recomendada**: Programas de frecuencia, bundles, suscripciones

## Métricas clave a monitorizar

- **Retention Rate**: % de clientes que repiten compra en el período. Objetivo: >40% en ecommerce.
- **Churn Rate**: % de clientes que no vuelven. Alarma si supera el 30% mensual.
- **Customer Lifetime Value (CLV)**: Valor económico esperado de un cliente durante toda la relación.
- **Average Order Value (AOV)**: Ticket medio. Aumentarlo con upselling mejora el margen.
- **Purchase Frequency**: Número de compras por cliente por año. Media sector: 2–4 veces.

## Reglas de segmentación RFM recomendadas

```
Si R>=4 Y F>=4 Y M>=4 → VIP Customers
Si F>=4 Y M>=3 → Loyal Customers
Si R=5 Y F<=2 → New Customers
Si R<=2 Y F>=3 Y M>=3 → At-Risk
Si R=1 Y F<=2 → Lost Customers
Si R>=4 Y M>=4 Y F<=3 → High Potential
Resto → Occasional Buyers
```

## Frecuencia recomendada de recalculo

- **Pequeño ecommerce** (< 10K clientes): Recalcular mensualmente
- **Ecommerce mediano** (10K–100K): Recalcular semanalmente
- **Gran plataforma** (> 100K): Recalcular diariamente o en tiempo real

## Ventajas del análisis RFM frente a otras técnicas

1. **Simplicidad**: Fácil de explicar a equipos no técnicos
2. **Accionabilidad**: Cada segmento tiene acciones claras asociadas
3. **Rapidez**: Se puede implementar con solo datos transaccionales
4. **Efectividad**: Predictor probado de comportamiento futuro
5. **Bajo coste**: No requiere modelos complejos de ML para empezar

## Errores comunes en implementación RFM

- Usar períodos de análisis demasiado cortos (< 90 días) — los resultados no son representativos
- No actualizar los segmentos con suficiente frecuencia
- Aplicar los mismos umbrales a negocios de diferente sector
- Ignorar la distribución asimétrica de los valores monetarios (usar percentiles, no medias)
