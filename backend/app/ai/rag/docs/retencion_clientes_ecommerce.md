# Retención de Clientes en Ecommerce — Estrategias y Métricas

## Por qué la retención es más rentable que la adquisición

Adquirir un nuevo cliente cuesta entre **5 y 25 veces más** que retener uno existente. Un aumento del 5% en la tasa de retención puede incrementar los beneficios entre un **25% y un 95%** (Harvard Business Review).

En ecommerce, los clientes recurrentes:
- Gastan un **67% más** que los nuevos clientes
- Tienen una **tasa de conversión** 5× mayor
- Generan el **40% de los ingresos** siendo solo el **8% de la base**

## Métricas fundamentales de retención

### Customer Retention Rate (CRR)
```
CRR = (Clientes al final - Nuevos clientes) / Clientes al inicio × 100
```
- **Benchmarks ecommerce**: 20–40% es aceptable; >50% es excelente
- Medirlo por cohorte (ej. clientes captados en enero, ¿cuántos siguen activos en julio?)

### Churn Rate (Tasa de Abandono)
```
Churn Rate = 1 - CRR
```
- **Churn mensual aceptable**: < 5%
- **Señal de alarma**: > 10% mensual
- **Churn predictivo**: Clientes con Recencia > 90 días tienen 3× más probabilidad de no volver

### Customer Lifetime Value (CLV)
```
CLV = AOV × Frecuencia_anual × Margen × (1 / Churn_Rate_mensual)
```
Ejemplo: AOV=€80, Frecuencia=3/año, Margen=30%, Churn mensual=5%
CLV = 80 × 3 × 0.30 × (1/0.05) = **€1.440**

### Net Promoter Score (NPS)
- Pregunta: "¿Con qué probabilidad recomendarías nuestra tienda?" (0-10)
- Promotores (9-10) tienen CLV 2–3× mayor que Detractores (0-6)
- Correlaciona directamente con la tasa de retención

## Estrategias de retención por segmento

### Para VIP Customers
**Objetivo**: Mantener el compromiso y evitar que se sientan ignorados

Tácticas:
- Programa de puntos/recompensas con beneficios exclusivos (envío gratuito, devoluciones extendidas)
- Acceso anticipado a nuevas colecciones o lanzamientos
- Gestor de cuenta personal o línea de atención prioritaria
- Invitaciones a eventos exclusivos o ventas privadas
- Comunicación personalizada (cumpleaños, aniversario de primera compra)

**KPI objetivo**: Mantener frecuencia de compra > 4 veces/año

### Para Loyal Customers
**Objetivo**: Aumentar frecuencia y ticket medio para convertirlos en VIP

Tácticas:
- Progresión visible en el programa de fidelización ("Te faltan €X para alcanzar nivel Premium")
- Recomendaciones de productos basadas en historial de compra
- Bundle offers y packs con descuento progresivo
- Email de reactivación preventiva si llevan >30 días sin comprar

**KPI objetivo**: Aumentar AOV en 15% y frecuencia en 20%

### Para New Customers
**Objetivo**: Lograr la segunda compra (el punto de inflexión hacia la fidelización)

Tácticas:
- Secuencia de emails de onboarding (días 1, 3, 7 post-compra)
- Descuento del 10–15% en segunda compra con límite de tiempo
- Encuesta de satisfacción post-entrega con seguimiento
- Contenido educativo sobre el producto o la marca

**KPI crítico**: Tasa de segunda compra. Benchmark: >25% en 90 días.

### Para At-Risk Customers
**Objetivo**: Reactivar antes de que se pierdan definitivamente

Señales de alerta:
- No han comprado en 60–120 días
- Tenían historial activo
- Sus emails tienen alta tasa de apertura histórica

Tácticas (secuencia recomendada):
1. **Día 60**: Email personalizado "Te echamos de menos" + contenido de valor
2. **Día 75**: Oferta especial 15% descuento, válida 10 días
3. **Día 85**: Último recordatorio con urgencia ("Tu oferta caduca en 3 días")
4. **Día 90**: Si no reactivó → mover a estrategia de recuperación de perdidos

**KPI objetivo**: Recuperar 20–30% de los At-Risk con la campaña

## Ciclo de vida del cliente y puntos de intervención

```
Captación → Primera Compra → Onboarding → Segunda Compra
     ↓                                         ↓
  Adquisición                          Fidelización activa
                                              ↓
                                      Compra recurrente
                                              ↓
                          (Señal de riesgo: > 45 días sin comprar)
                                              ↓
                                    Campaña de retención preventiva
                                              ↓
                          (Sin respuesta: > 90 días sin comprar)
                                              ↓
                                      Campaña de win-back
```

## Mejores prácticas para email de retención

1. **Personalización**: Incluir nombre, productos vistos o categorías favoritas
2. **Asunto**: Incluir nombre o referencia personal — aumenta apertura en 26%
3. **Timing**: Martes y jueves, 10:00–14:00 → mejor tasa de apertura
4. **CTA único**: Un solo llamado a la acción por email
5. **Mobile-first**: 60% de los emails se abren en móvil
6. **Frecuencia máxima**: No más de 2 emails/semana para evitar opt-outs

## Programas de fidelización que funcionan en ecommerce

### Modelo de puntos
- Por cada € gastado → X puntos
- Canjeable por descuentos o productos gratuitos
- Ventaja: Simple, fácil de entender
- Riesgo: Puede generar descuentos excesivos si no se calibra bien

### Modelo de niveles (tiers)
- Bronze → Silver → Gold → Platinum
- Cada nivel desbloquea beneficios adicionales
- Ventaja: Incentiva el aumento del gasto para subir de nivel
- Mejor para segmentos VIP y Loyal

### Modelo de suscripción (membresía de pago)
- Cliente paga €X/mes a cambio de beneficios premium
- Ej.: Envío gratuito ilimitado, descuentos fijos, contenido exclusivo
- Ventaja: Ingresos predecibles, altísima retención
- Requiere volumen de compra suficiente para que el cliente perciba valor

## Herramientas de medición recomendadas

- **Cohort analysis**: Para medir retención por fecha de adquisición
- **Survival curves**: Para predecir vida media del cliente
- **RFM scoring**: Para segmentar y priorizar campañas (ver documento específico)
- **Predictive CLV**: Modelos de ML para predecir valor futuro por cliente
