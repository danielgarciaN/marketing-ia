import type { Insight } from "./types";

export type Locale = "en" | "es";

export const locales: Record<Locale, string> = {
  en: "English",
  es: "Espanol",
};

export const copy = {
  en: {
    brandSubtitle: "Customer analytics",
    platform: "AI Marketing Intelligence Platform",
    api: "API: localhost:8000",
    language: "Language",
    nav: {
      overview: "Overview",
      data: "Data",
      customers: "Customers",
      segments: "Segments",
      clustering: "Clustering",
      campaigns: "Campaigns",
      insights: "Insights",
      methodology: "Methodology",
    },
    titles: {
      overview: "Executive Dashboard",
      data: "Data Management",
      customers: "Customer Intelligence",
      segments: "Audience Segments",
      clustering: "ML Clustering",
      campaigns: "Campaign Simulator",
      insights: "Business Insights",
      methodology: "Methodology",
    },
    overview: {
      totalCustomers: "Total customers",
      rfmProfiles: "RFM profiles",
      revenue: "Revenue",
      cleanedTransactions: "Cleaned transactions",
      orders: "Orders",
      uniqueInvoices: "Unique invoices",
      avgOrderValue: "Avg order value",
      perInvoice: "Per invoice",
      activeCustomers: "Active customers",
      activeDetail: "Recency <= 30 days",
      inactiveCustomers: "Inactive customers",
      inactiveDetail: "Recency > 180 days",
      revenueBySegment: "Revenue by Segment",
      monetaryShare: "Share of monetary value",
      customerDistribution: "Customer Distribution",
      segmentSize: "Segment size",
    },
    revenueChart: {
      title: "Monthly Revenue",
      periods: "periods",
      tooltip: "Revenue",
    },
    customers: {
      title: "Top Customers by Revenue",
      available: "customers available",
      customer: "Customer",
      country: "Country",
      segment: "Segment",
      revenue: "Revenue",
      frequency: "Frequency",
      recency: "Recency",
      cluster: "Cluster",
    },
    segments: {
      customers: "Customers",
      revenue: "Revenue",
      avgRecency: "Avg recency",
      avgFrequency: "Avg frequency",
      share: "share",
      revenueLabel: "revenue",
    },
    clustering: {
      clusters: "Clusters",
      kmeansGroups: "KMeans groups",
      silhouette: "Silhouette",
      clusterSeparation: "Cluster separation",
      inertia: "Inertia",
      variance: "Within-cluster variance",
      title: "Customer Clusters",
      subtitle: "PCA projection",
      revenue: "Revenue",
    },
    campaigns: {
      segment: "Segment",
      campaignType: "Campaign type",
      budget: "Budget",
      discount: "Discount %",
      conversion: "Expected conversion %",
      simulate: "Simulate campaign",
      simulating: "Simulating",
      estimatedRevenue: "Estimated revenue",
      roi: "ROI",
      customersReached: "Customers reached",
      conversions: "Conversions",
      empty: "Run a simulation to estimate revenue, uplift and ROI.",
    },
    data: {
      title: "Upload a new dataset",
      description: "Upload CSV or Excel data from ecommerce, CRM or payment exports. The platform infers columns, lets you correct the mapping and retrains the pipeline.",
      selectFile: "Select data file",
      retrain: "Retrain after upload",
      upload: "Upload dataset",
      uploading: "Uploading",
      retrainOnly: "Retrain current dataset",
      refreshing: "Refreshing",
      status: "Dataset status",
      rawDataset: "Raw dataset",
      processedCustomers: "Processed customers",
      customers: "customers",
      requiredColumns: "Required columns",
      lastModified: "Last modified",
      notAvailable: "Not available",
      success: "Dataset updated successfully. Dashboard data has been refreshed.",
      currencyTitle: "Currency display",
      currencyDescription: "Revenue values are stored as source amounts. Use this control to display the portal in pounds or converted euros.",
      baseCurrency: "Base data: GBP",
      convertedCurrency: "Display: EUR",
      backendOutdated: "The data endpoint was not found. Restart the backend so the new /data routes are loaded.",
      mappingTitle: "Smart column mapping",
      mappingDescription: "Detected columns are mapped to the internal ecommerce schema. Review low-confidence fields before uploading.",
      inferReady: "Schema detected. Review the mapping and upload when ready.",
      missingFields: "Missing fields",
      qualityWarnings: "Data quality warnings",
      rfmTitle: "Configurable RFM and clustering",
      rfmDescription: "Tune how the platform scores customers, defines active/inactive users and trains KMeans clusters.",
      sourceCurrency: "Source currency",
      recencyWeight: "Recency weight",
      frequencyWeight: "Frequency weight",
      monetaryWeight: "Monetary weight",
      activeDays: "Active customer days",
      inactiveDays: "Inactive customer days",
      clusters: "KMeans clusters",
      autoClusters: "Auto-select best k by silhouette",
      saveConfig: "Save configuration",
      configSaved: "Configuration saved.",
    },
    insights: {
      action: "Action",
      impact: "Impact",
    },
    methodology: {
      steps: [
        {
          eyebrow: "1. Data cleaning",
          title: "Transaction quality layer",
          text: "Cancelled invoices, missing customers, invalid prices and duplicated rows are removed before feature engineering.",
        },
        {
          eyebrow: "2. RFM analysis",
          title: "Explainable customer value",
          text: "Customers are scored with Recency, Frequency and Monetary quantiles, then mapped to business-friendly CRM segments.",
        },
        {
          eyebrow: "3. Clustering",
          title: "KMeans plus PCA",
          text: "The model uses scaled and log-transformed RFM features. Current silhouette score:",
        },
        {
          eyebrow: "4. Activation",
          title: "Campaign decisioning",
          text: "Segment rules generate recommended campaigns, ROI simulations and automatic business insights for marketing teams.",
        },
      ],
    },
    states: {
      loading: "Loading platform data",
      backendTitle: "Backend is not reachable.",
      backendCommand: "Start the API with:",
    },
  },
  es: {
    brandSubtitle: "Analitica de clientes",
    platform: "AI Marketing Intelligence Platform",
    api: "API: localhost:8000",
    language: "Idioma",
    nav: {
      overview: "Resumen",
      data: "Datos",
      customers: "Clientes",
      segments: "Segmentos",
      clustering: "Clustering",
      campaigns: "Campanas",
      insights: "Insights",
      methodology: "Metodologia",
    },
    titles: {
      overview: "Dashboard Ejecutivo",
      data: "Gestion de Datos",
      customers: "Inteligencia de Clientes",
      segments: "Segmentos de Audiencia",
      clustering: "Clustering ML",
      campaigns: "Simulador de Campanas",
      insights: "Insights de Negocio",
      methodology: "Metodologia",
    },
    overview: {
      totalCustomers: "Clientes totales",
      rfmProfiles: "Perfiles RFM",
      revenue: "Ingresos",
      cleanedTransactions: "Transacciones limpias",
      orders: "Pedidos",
      uniqueInvoices: "Facturas unicas",
      avgOrderValue: "Ticket medio",
      perInvoice: "Por factura",
      activeCustomers: "Clientes activos",
      activeDetail: "Recency <= 30 dias",
      inactiveCustomers: "Clientes inactivos",
      inactiveDetail: "Recency > 180 dias",
      revenueBySegment: "Ingresos por Segmento",
      monetaryShare: "Peso sobre el valor monetario",
      customerDistribution: "Distribucion de Clientes",
      segmentSize: "Tamano del segmento",
    },
    revenueChart: {
      title: "Ingresos Mensuales",
      periods: "periodos",
      tooltip: "Ingresos",
    },
    customers: {
      title: "Clientes Top por Ingresos",
      available: "clientes disponibles",
      customer: "Cliente",
      country: "Pais",
      segment: "Segmento",
      revenue: "Ingresos",
      frequency: "Frecuencia",
      recency: "Recency",
      cluster: "Cluster",
    },
    segments: {
      customers: "Clientes",
      revenue: "Ingresos",
      avgRecency: "Recency media",
      avgFrequency: "Frecuencia media",
      share: "peso",
      revenueLabel: "ingresos",
    },
    clustering: {
      clusters: "Clusters",
      kmeansGroups: "Grupos KMeans",
      silhouette: "Silhouette",
      clusterSeparation: "Separacion de clusters",
      inertia: "Inercia",
      variance: "Varianza intra-cluster",
      title: "Clusters de Clientes",
      subtitle: "Proyeccion PCA",
      revenue: "Ingresos",
    },
    campaigns: {
      segment: "Segmento",
      campaignType: "Tipo de campana",
      budget: "Presupuesto",
      discount: "Descuento %",
      conversion: "Conversion esperada %",
      simulate: "Simular campana",
      simulating: "Simulando",
      estimatedRevenue: "Ingresos estimados",
      roi: "ROI",
      customersReached: "Clientes alcanzados",
      conversions: "Conversiones",
      empty: "Ejecuta una simulacion para estimar ingresos, uplift y ROI.",
    },
    data: {
      title: "Subir un nuevo dataset",
      description: "Sube CSV o Excel desde ecommerce, CRM o pagos. La plataforma detecta columnas, permite corregir el mapping y reentrena el pipeline.",
      selectFile: "Seleccionar archivo",
      retrain: "Reentrenar despues de subir",
      upload: "Subir dataset",
      uploading: "Subiendo",
      retrainOnly: "Reentrenar dataset actual",
      refreshing: "Actualizando",
      status: "Estado del dataset",
      rawDataset: "Dataset raw",
      processedCustomers: "Clientes procesados",
      customers: "clientes",
      requiredColumns: "Columnas requeridas",
      lastModified: "Ultima modificacion",
      notAvailable: "No disponible",
      success: "Dataset actualizado correctamente. El dashboard se ha refrescado.",
      currencyTitle: "Visualizacion de moneda",
      currencyDescription: "Los ingresos se guardan con los importes de origen. Usa este control para mostrar el portal en libras o euros convertidos.",
      baseCurrency: "Datos base: GBP",
      convertedCurrency: "Mostrar: EUR",
      backendOutdated: "No se encontro el endpoint de datos. Reinicia el backend para cargar las nuevas rutas /data.",
      mappingTitle: "Mapeo inteligente de columnas",
      mappingDescription: "Las columnas detectadas se asignan al esquema ecommerce interno. Revisa campos con baja confianza antes de subir.",
      inferReady: "Esquema detectado. Revisa el mapping y sube el archivo cuando este listo.",
      missingFields: "Campos pendientes",
      qualityWarnings: "Avisos de calidad de datos",
      rfmTitle: "RFM y clustering configurables",
      rfmDescription: "Ajusta como se puntuan clientes, como se definen activos/inactivos y como se entrena KMeans.",
      sourceCurrency: "Moneda origen",
      recencyWeight: "Peso recency",
      frequencyWeight: "Peso frequency",
      monetaryWeight: "Peso monetary",
      activeDays: "Dias cliente activo",
      inactiveDays: "Dias cliente inactivo",
      clusters: "Clusters KMeans",
      autoClusters: "Elegir mejor k por silhouette",
      saveConfig: "Guardar configuracion",
      configSaved: "Configuracion guardada.",
    },
    insights: {
      action: "Accion",
      impact: "Impacto",
    },
    methodology: {
      steps: [
        {
          eyebrow: "1. Limpieza de datos",
          title: "Capa de calidad transaccional",
          text: "Se eliminan facturas canceladas, clientes nulos, precios invalidos y duplicados antes del feature engineering.",
        },
        {
          eyebrow: "2. Analisis RFM",
          title: "Valor de cliente explicable",
          text: "Los clientes se puntuan con cuantiles de Recency, Frequency y Monetary, y se asignan a segmentos CRM accionables.",
        },
        {
          eyebrow: "3. Clustering",
          title: "KMeans mas PCA",
          text: "El modelo usa variables RFM escaladas y transformadas con log. Silhouette score actual:",
        },
        {
          eyebrow: "4. Activacion",
          title: "Decision de campanas",
          text: "Las reglas de segmento generan campanas recomendadas, simulaciones de ROI e insights automaticos para marketing.",
        },
      ],
    },
    states: {
      loading: "Cargando datos de la plataforma",
      backendTitle: "No se puede conectar con el backend.",
      backendCommand: "Arranca la API con:",
    },
  },
} as const;

const segmentLabels: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    "VIP Customers": "Clientes VIP",
    "Loyal Customers": "Clientes Fieles",
    "New Customers": "Clientes Nuevos",
    "At-Risk Customers": "Clientes en Riesgo",
    "Lost Customers": "Clientes Perdidos",
    "Occasional Buyers": "Compradores Ocasionales",
    "High Potential": "Alto Potencial",
  },
};

const segmentDescriptions: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    "VIP Customers": "Clientes de maximo valor, con buena recencia, alta frecuencia y alto gasto. Son el segmento mas rentable y deben cuidarse con acciones exclusivas.",
    "Loyal Customers": "Clientes frecuentes y recientes con buen nivel de gasto. Son compradores recurrentes con potencial para convertirse en VIP.",
    "New Customers": "Clientes adquiridos recientemente y con pocas compras. El objetivo principal es conseguir una segunda compra pronto.",
    "At-Risk Customers": "Clientes que fueron activos y valiosos, pero llevan demasiado tiempo sin comprar. Requieren acciones de reactivacion.",
    "Lost Customers": "Clientes con baja actividad reciente y bajo valor actual. Probablemente han abandonado y solo conviene recuperarlos con incentivos selectivos.",
    "Occasional Buyers": "Clientes que compran de forma esporadica. Tienen margen para aumentar frecuencia con promociones y recordatorios.",
    "High Potential": "Clientes con buen gasto y recencia, pero con margen para crecer en frecuencia. Son buenos candidatos para upsell y cross-sell.",
  },
};

const businessGoals: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    "VIP Customers": "Maximizar retencion y lifetime value de los clientes mas rentables.",
    "Loyal Customers": "Reforzar fidelidad y empujarles hacia el segmento VIP mediante upselling.",
    "New Customers": "Convertir compradores recientes en clientes recurrentes durante los primeros 30 dias.",
    "At-Risk Customers": "Prevenir churn y recuperar actividad antes de que pasen a clientes perdidos.",
    "Lost Customers": "Intentar recuperacion selectiva y aprender los motivos de abandono.",
    "Occasional Buyers": "Aumentar frecuencia de compra y evolucionar hacia segmentos mas fieles.",
    "High Potential": "Incrementar valor mediante cross-selling, up-selling y bundles personalizados.",
  },
};

const campaignLabels: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    email: "email",
    sms: "sms",
    push: "push",
    direct_mail: "correo fisico",
    retargeting: "retargeting",
    "Loyalty Program": "Programa de fidelizacion",
    "Early Access": "Acceso anticipado",
    "Premium Offers": "Ofertas premium",
    "Referral Program": "Programa de referidos",
    "Cross-Sell": "Cross-selling",
    "Birthday Rewards": "Recompensas de cumpleanos",
    "Onboarding Series": "Secuencia de bienvenida",
    "Product Recommendations": "Recomendaciones de producto",
    "Welcome Discount": "Descuento de bienvenida",
    "Reactivation Email": "Email de reactivacion",
    "Win-Back Survey": "Encuesta de recuperacion",
    "Personalized Offer": "Oferta personalizada",
    "Win-Back Campaign": "Campana win-back",
    "Strong Incentive": "Incentivo fuerte",
    "Exit Survey": "Encuesta de salida",
    "Frequency Boost": "Impulso de frecuencia",
    "Bundle Offers": "Ofertas bundle",
    "Seasonal Campaign": "Campana estacional",
    "Cross-Selling": "Cross-selling",
    "Up-Selling": "Up-selling",
    "Personalized Bundles": "Bundles personalizados",
  },
};

const campaignObjectives: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    "Retain and reward": "Retener y recompensar",
    "Increase engagement": "Aumentar engagement",
    "Increase AOV": "Aumentar ticket medio",
    "Acquisition via advocacy": "Captar clientes por recomendacion",
    "Expand basket": "Ampliar cesta",
    "Build emotional connection": "Construir relacion emocional",
    "Educate and engage": "Educar y activar",
    "Drive second purchase": "Impulsar segunda compra",
    "Encourage repeat purchase": "Fomentar recompra",
    "Re-engage": "Reactivar",
    "Understand churn drivers": "Entender motivos de abandono",
    "Trigger purchase": "Provocar compra",
    "Last attempt to recover": "Ultimo intento de recuperacion",
    "Break inertia": "Romper inercia",
    "Learn from churn": "Aprender del churn",
    "Increase purchase cadence": "Aumentar cadencia de compra",
    "Timely relevance": "Aportar relevancia estacional",
    "Expand product range": "Ampliar rango de productos",
    "Increase order value": "Aumentar valor del pedido",
    "Drive larger baskets": "Impulsar cestas mas grandes",
  },
};

const campaignMessages: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    "Loyalty Program": "Acceso VIP a novedades, soporte prioritario y beneficios exclusivos.",
    "Early Access": "Acceso anticipado solo para clientes especiales.",
    "Premium Offers": "Bundles premium seleccionados segun comportamiento de compra.",
    "Referral Program": "Invita a un amigo y ambos reciben una recompensa.",
    "Cross-Sell": "Productos complementarios recomendados segun compras previas.",
    "Birthday Rewards": "Un detalle especial para reforzar la relacion con el cliente.",
    "Onboarding Series": "Secuencia de bienvenida para explicar valor, categorias y beneficios.",
    "Product Recommendations": "Recomendaciones basadas en la primera compra.",
    "Welcome Discount": "Incentivo para acelerar la segunda compra.",
    "Reactivation Email": "Mensaje de reactivacion con descuento personalizado.",
    "Win-Back Survey": "Encuesta breve para entender por que dejo de comprar.",
    "Personalized Offer": "Oferta basada en productos o categorias de interes.",
    "Win-Back Campaign": "Campana de recuperacion con incentivo fuerte.",
    "Strong Incentive": "Descuento alto o envio gratis para romper la inactividad.",
    "Exit Survey": "Encuesta de salida para aprender de clientes perdidos.",
    "Frequency Boost": "Puntos extra o incentivo temporal para aumentar frecuencia.",
    "Bundle Offers": "Descuento por compra combinada o packs personalizados.",
    "Seasonal Campaign": "Campana alineada con temporada o momento de compra.",
    "Cross-Selling": "Productos complementarios para ampliar valor.",
    "Up-Selling": "Propuesta de versiones premium o mayor valor.",
    "Personalized Bundles": "Bundles adaptados al perfil y comportamiento del cliente.",
  },
};

const priorityLabels: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    Critical: "Critica",
    High: "Alta",
    Medium: "Media",
    Low: "Baja",
  },
};

const insightLabels: Record<Locale, Record<string, Partial<Insight>>> = {
  en: {},
  es: {
    vip_concentration: {
      category: "Ingresos",
      title: "Concentracion de ingresos en clientes VIP",
      insight: "Los clientes VIP representan una parte reducida de la base, pero concentran una parte muy alta de los ingresos. Conviene priorizar retencion, beneficios exclusivos y acciones de fidelizacion para proteger este valor.",
      action: "Lanzar un programa VIP con acceso anticipado, soporte premium y ofertas personalizadas.",
    },
    at_risk_alert: {
      category: "Retencion",
      title: "Alerta de clientes en riesgo",
      insight: "Existe un grupo de clientes en riesgo con buen historial de compra, pero sin actividad reciente. Es una oportunidad clara de reactivacion antes de que pasen a clientes perdidos.",
      action: "Activar una campana de reactivacion con descuentos personalizados y mensajes de urgencia en los proximos 7 dias.",
    },
    new_conversion: {
      category: "Crecimiento",
      title: "Oportunidad de conversion de nuevos clientes",
      insight: "Los clientes nuevos estan en una ventana critica para conseguir la segunda compra. Una buena secuencia de bienvenida puede acelerar su conversion a clientes recurrentes.",
      action: "Configurar una secuencia de onboarding con recomendaciones de producto e incentivo para segunda compra.",
    },
    lost_recovery: {
      category: "Retencion",
      title: "Potencial de recuperacion de clientes perdidos",
      insight: "Los clientes perdidos acumulan valor historico, pero necesitan incentivos fuertes para volver. La recuperacion debe tratarse como una campana puntual y muy segmentada.",
      action: "Ejecutar una campana win-back con incentivo fuerte como ultimo intento de recuperacion.",
    },
    revenue_trend: {
      category: "Ingresos",
      title: "Analisis de tendencia de ingresos",
      insight: "La tendencia reciente de ingresos ayuda a detectar si el negocio esta creciendo o necesita intervencion. Si hay caida, conviene revisar churn, promociones y segmentos en riesgo.",
    },
    high_potential_upsell: {
      category: "Crecimiento",
      title: "Oportunidad de upsell en clientes de alto potencial",
      insight: "Los clientes de alto potencial tienen buena relacion reciente con la marca y margen para aumentar valor. Son buenos candidatos para cross-selling, upselling y bundles personalizados.",
      action: "Implementar recomendaciones personalizadas y bundles para este segmento.",
    },
    geo_concentration: {
      category: "Estrategia",
      title: "Riesgo de concentracion geografica",
      insight: "La base de clientes esta concentrada en el mercado principal. Diversificar mercados puede reducir riesgo y abrir nuevas oportunidades de crecimiento internacional.",
      action: "Explorar campanas para mercados internacionales como Alemania, Francia y Espana.",
    },
    frequency_gap: {
      category: "Engagement",
      title: "Brecha de frecuencia de compra",
      insight: "La diferencia entre frecuencia media y mediana indica que pocos clientes compran mucho mientras la mayoria compra pocas veces. Hay margen para aumentar recurrencia.",
      action: "Disenar programas de puntos, recordatorios y acciones de frecuencia para clientes con pocas compras.",
    },
  },
};

export function segmentLabel(segment: string, locale: Locale) {
  return segmentLabels[locale][segment] ?? segment;
}

export function segmentDescription(segment: string, fallback: string, locale: Locale) {
  return segmentDescriptions[locale][segment] ?? fallback;
}

export function businessGoal(segment: string, fallback: string, locale: Locale) {
  return businessGoals[locale][segment] ?? fallback;
}

export function campaignLabel(name: string, locale: Locale) {
  return campaignLabels[locale][name] ?? name.replace("_", " ");
}

export function campaignObjective(objective: string, locale: Locale) {
  return campaignObjectives[locale][objective] ?? objective;
}

export function campaignMessage(type: string, fallback: string, locale: Locale) {
  return campaignMessages[locale][type] ?? fallback;
}

export function priorityLabel(priority: string, locale: Locale) {
  return priorityLabels[locale][priority] ?? priority;
}

export function localizedInsight(insight: Insight, locale: Locale): Insight {
  return {
    ...insight,
    ...(insightLabels[locale][insight.id] ?? {}),
  };
}
