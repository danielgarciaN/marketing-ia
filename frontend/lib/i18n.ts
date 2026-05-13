import type { Insight } from "./types";

export type Locale = "en" | "es";

export const locales: Record<Locale, string> = {
  en: "English",
  es: "Español",
};

export const copy = {
  en: {
    brandSubtitle: "Customer analytics",
    platform: "AI Marketing Intelligence Platform",
    api: "API: localhost:8000",
    language: "Language",
    nav: {
      overview: "Overview",
      customers: "Customers",
      segments: "Segments",
      clustering: "Clustering",
      campaigns: "Campaigns",
      insights: "Insights",
      methodology: "Methodology",
    },
    titles: {
      overview: "Executive Dashboard",
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
    brandSubtitle: "Analítica de clientes",
    platform: "AI Marketing Intelligence Platform",
    api: "API: localhost:8000",
    language: "Idioma",
    nav: {
      overview: "Resumen",
      customers: "Clientes",
      segments: "Segmentos",
      clustering: "Clustering",
      campaigns: "Campañas",
      insights: "Insights",
      methodology: "Metodología",
    },
    titles: {
      overview: "Dashboard Ejecutivo",
      customers: "Inteligencia de Clientes",
      segments: "Segmentos de Audiencia",
      clustering: "Clustering ML",
      campaigns: "Simulador de Campañas",
      insights: "Insights de Negocio",
      methodology: "Metodología",
    },
    overview: {
      totalCustomers: "Clientes totales",
      rfmProfiles: "Perfiles RFM",
      revenue: "Ingresos",
      cleanedTransactions: "Transacciones limpias",
      orders: "Pedidos",
      uniqueInvoices: "Facturas únicas",
      avgOrderValue: "Ticket medio",
      perInvoice: "Por factura",
      activeCustomers: "Clientes activos",
      activeDetail: "Recency <= 30 días",
      inactiveCustomers: "Clientes inactivos",
      inactiveDetail: "Recency > 180 días",
      revenueBySegment: "Ingresos por Segmento",
      monetaryShare: "Peso sobre el valor monetario",
      customerDistribution: "Distribución de Clientes",
      segmentSize: "Tamaño del segmento",
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
      country: "País",
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
      clusterSeparation: "Separación de clusters",
      inertia: "Inercia",
      variance: "Varianza intra-cluster",
      title: "Clusters de Clientes",
      subtitle: "Proyección PCA",
      revenue: "Ingresos",
    },
    campaigns: {
      segment: "Segmento",
      campaignType: "Tipo de campaña",
      budget: "Presupuesto",
      discount: "Descuento %",
      conversion: "Conversión esperada %",
      simulate: "Simular campaña",
      simulating: "Simulando",
      estimatedRevenue: "Ingresos estimados",
      roi: "ROI",
      customersReached: "Clientes alcanzados",
      conversions: "Conversiones",
      empty: "Ejecuta una simulación para estimar ingresos, uplift y ROI.",
    },
    insights: {
      action: "Acción",
      impact: "Impacto",
    },
    methodology: {
      steps: [
        {
          eyebrow: "1. Limpieza de datos",
          title: "Capa de calidad transaccional",
          text: "Se eliminan facturas canceladas, clientes nulos, precios inválidos y duplicados antes del feature engineering.",
        },
        {
          eyebrow: "2. Análisis RFM",
          title: "Valor de cliente explicable",
          text: "Los clientes se puntúan con cuantiles de Recency, Frequency y Monetary, y se asignan a segmentos CRM accionables.",
        },
        {
          eyebrow: "3. Clustering",
          title: "KMeans más PCA",
          text: "El modelo usa variables RFM escaladas y transformadas con log. Silhouette score actual:",
        },
        {
          eyebrow: "4. Activación",
          title: "Decisión de campañas",
          text: "Las reglas de segmento generan campañas recomendadas, simulaciones de ROI e insights automáticos para marketing.",
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

const campaignLabels: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    email: "email",
    sms: "sms",
    push: "push",
    direct_mail: "correo físico",
    retargeting: "retargeting",
    "Loyalty Program": "Programa de fidelización",
    "Early Access": "Acceso anticipado",
    "Premium Offers": "Ofertas premium",
    "Referral Program": "Programa de referidos",
    "Cross-Sell": "Cross-selling",
    "Birthday Rewards": "Recompensas de cumpleaños",
    "Onboarding Series": "Secuencia de bienvenida",
    "Product Recommendations": "Recomendaciones de producto",
    "Welcome Discount": "Descuento de bienvenida",
    "Reactivation Email": "Email de reactivación",
    "Win-Back Survey": "Encuesta de recuperación",
    "Personalized Offer": "Oferta personalizada",
    "Win-Back Campaign": "Campaña win-back",
    "Strong Incentive": "Incentivo fuerte",
    "Exit Survey": "Encuesta de salida",
    "Frequency Boost": "Impulso de frecuencia",
    "Bundle Offers": "Ofertas bundle",
    "Seasonal Campaign": "Campaña estacional",
    "Cross-Selling": "Cross-selling",
    "Up-Selling": "Up-selling",
    "Personalized Bundles": "Bundles personalizados",
  },
};

const priorityLabels: Record<Locale, Record<string, string>> = {
  en: {},
  es: {
    Critical: "Crítica",
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
      title: "Concentración de ingresos en clientes VIP",
      action: "Lanzar un programa VIP con acceso anticipado, soporte premium y ofertas personalizadas.",
    },
    at_risk_alert: {
      category: "Retención",
      title: "Alerta de clientes en riesgo",
      action: "Activar una campaña de reactivación con descuentos personalizados y mensajes de urgencia en los próximos 7 días.",
    },
    new_conversion: {
      category: "Crecimiento",
      title: "Oportunidad de conversión de nuevos clientes",
      action: "Configurar una secuencia de onboarding con recomendaciones de producto e incentivo para segunda compra.",
    },
    lost_recovery: {
      category: "Retención",
      title: "Potencial de recuperación de clientes perdidos",
      action: "Ejecutar una campaña win-back con incentivo fuerte como último intento de recuperación.",
    },
    revenue_trend: {
      category: "Ingresos",
      title: "Análisis de tendencia de ingresos",
    },
    high_potential_upsell: {
      category: "Crecimiento",
      title: "Oportunidad de upsell en clientes de alto potencial",
      action: "Implementar recomendaciones personalizadas y bundles para este segmento.",
    },
    geo_concentration: {
      category: "Estrategia",
      title: "Riesgo de concentración geográfica",
      action: "Explorar campañas para mercados internacionales como Alemania, Francia y España.",
    },
    frequency_gap: {
      category: "Engagement",
      title: "Brecha de frecuencia de compra",
      action: "Diseñar programas de puntos, recordatorios y acciones de frecuencia para clientes con pocas compras.",
    },
  },
};

export function segmentLabel(segment: string, locale: Locale) {
  return segmentLabels[locale][segment] ?? segment;
}

export function campaignLabel(name: string, locale: Locale) {
  return campaignLabels[locale][name] ?? name.replace("_", " ");
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
