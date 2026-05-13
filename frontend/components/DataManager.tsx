"use client";

import { useEffect, useMemo, useState } from "react";
import { Database, RefreshCw, Settings2, Upload } from "lucide-react";
import { api } from "@/lib/api";
import type { DataFieldMetadata, DataStatus, DataUploadResult, PipelineConfig, SchemaInference } from "@/lib/types";
import type { Currency } from "@/lib/format";

const defaultConfig: PipelineConfig = {
  source: { filename: "online_retail.csv", source_currency: "GBP", column_mapping: {} },
  rfm: {
    score_quantiles: 5,
    weights: { recency: 1, frequency: 1, monetary: 1 },
    active_days: 30,
    inactive_days: 180,
    new_customer_max_frequency: 2,
    segment_thresholds: {
      vip: { r: 4, f: 4, m: 4 },
      loyal: { r: 4, f: 3, m: 3 },
      at_risk: { r: 2, f: 3, m: 3 },
      lost: { r: 2, f: 2, m: 2 },
      high_potential: { r: 3, f: 2, m: 3 },
    },
  },
  clustering: { n_clusters: 5, auto_select_k: false },
};

export function DataManager({
  labels,
  currency,
  setCurrency,
  onRefresh,
}: {
  labels: {
    title: string;
    description: string;
    selectFile: string;
    retrain: string;
    upload: string;
    uploading: string;
    retrainOnly: string;
    refreshing: string;
    status: string;
    rawDataset: string;
    processedCustomers: string;
    customers: string;
    requiredColumns: string;
    lastModified: string;
    notAvailable: string;
    success: string;
    currencyTitle: string;
    currencyDescription: string;
    baseCurrency: string;
    convertedCurrency: string;
    backendOutdated: string;
    mappingTitle: string;
    mappingDescription: string;
    inferReady: string;
    missingFields: string;
    qualityWarnings: string;
    rfmTitle: string;
    rfmDescription: string;
    sourceCurrency: string;
    recencyWeight: string;
    frequencyWeight: string;
    monetaryWeight: string;
    activeDays: string;
    inactiveDays: string;
    clusters: string;
    autoClusters: string;
    saveConfig: string;
    configSaved: string;
  };
  currency: Currency;
  setCurrency: (currency: Currency) => void;
  onRefresh: () => Promise<void>;
}) {
  const [status, setStatus] = useState<DataStatus | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [inference, setInference] = useState<SchemaInference | null>(null);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [config, setConfig] = useState<PipelineConfig>(defaultConfig);
  const [retrain, setRetrain] = useState(true);
  const [loading, setLoading] = useState(false);
  const [inferring, setInferring] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fieldMetadata = useMemo<DataFieldMetadata[]>(() => {
    return inference?.field_metadata ?? status?.required_fields ?? [];
  }, [inference, status]);

  const loadStatus = async () => {
    const currentStatus = await api.dataStatus();
    setStatus(currentStatus);
    if (currentStatus.config) {
      setConfig(currentStatus.config);
      setMapping(currentStatus.config.source.column_mapping ?? {});
    }
  };

  useEffect(() => {
    loadStatus().catch((err) => setError(err instanceof Error ? err.message : "Could not load data status"));
  }, []);

  const handleFile = async (nextFile: File | null) => {
    setFile(nextFile);
    setInference(null);
    setError(null);
    setMessage(null);
    if (!nextFile) return;

    setInferring(true);
    try {
      const result = await api.inferSchema(nextFile);
      setInference(result);
      setMapping(result.mapping);
      setMessage(labels.inferReady);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Schema inference failed");
    } finally {
      setInferring(false);
    }
  };

  const configPayload = (): Partial<PipelineConfig> => ({
    source: {
      ...config.source,
      source_currency: config.source.source_currency,
      column_mapping: mapping,
    },
    rfm: config.rfm,
    clustering: config.clustering,
  });

  const handleUpload = async () => {
    if (!file) return;
    await runAction(() => api.uploadDataset(file, retrain, mapping, configPayload()));
  };

  const handleRetrain = async () => {
    await runAction(() => api.retrainData(configPayload()));
  };

  const handleSaveConfig = async () => {
    await runAction(async () => {
      const saved = await api.saveConfig(configPayload());
      setConfig(saved);
      return { status: "saved", config: saved };
    }, labels.configSaved);
  };

  const runAction = async (action: () => Promise<DataUploadResult>, successMessage = labels.success) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      await action();
      await loadStatus();
      await onRefresh();
      setMessage(successMessage);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Data update failed";
      setError(message.includes("404") ? labels.backendOutdated : message);
    } finally {
      setLoading(false);
    }
  };

  const updateWeight = (key: keyof PipelineConfig["rfm"]["weights"], value: number) => {
    setConfig((current) => ({
      ...current,
      rfm: { ...current.rfm, weights: { ...current.rfm.weights, [key]: value } },
    }));
  };

  return (
    <div className="view-stack">
      <section className="data-grid">
        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">CSV / Excel</span>
              <h2>{labels.title}</h2>
            </div>
            <Upload size={22} />
          </div>
          <p>{labels.description}</p>
          <label>
            {labels.selectFile}
            <input type="file" accept=".csv,.xlsx,.xls,text/csv" onChange={(event) => handleFile(event.target.files?.[0] ?? null)} />
          </label>
          <label className="check-row">
            <input type="checkbox" checked={retrain} onChange={(event) => setRetrain(event.target.checked)} />
            {labels.retrain}
          </label>
          <div className="button-row">
            <button className="primary-button" onClick={handleUpload} disabled={!file || loading || inferring}>
              <Upload size={16} />
              {loading ? labels.uploading : labels.upload}
            </button>
            <button className="secondary-button" onClick={handleRetrain} disabled={loading}>
              <RefreshCw size={16} />
              {loading ? labels.refreshing : labels.retrainOnly}
            </button>
          </div>
          {message ? <div className="success-state">{message}</div> : null}
          {error ? <div className="error-inline">{error}</div> : null}
        </article>

        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">AI Mapping</span>
              <h2>{labels.mappingTitle}</h2>
            </div>
            <Settings2 size={22} />
          </div>
          <p>{labels.mappingDescription}</p>
          <div className="mapping-grid">
            {fieldMetadata.map((field) => (
              <label key={field.field}>
                {field.label}
                <select value={mapping[field.field] ?? ""} onChange={(event) => setMapping((current) => ({ ...current, [field.field]: event.target.value }))}>
                  <option value="">{field.required ? labels.missingFields : labels.notAvailable}</option>
                  {(inference?.columns ?? Object.values(mapping)).map((column) => (
                    <option key={`${field.field}-${column}`} value={column}>
                      {column}
                      {inference?.confidence[field.field] ? ` (${Math.round(inference.confidence[field.field] * 100)}%)` : ""}
                    </option>
                  ))}
                </select>
              </label>
            ))}
          </div>
          {inference?.missing_fields.length ? <div className="error-inline">{`${labels.missingFields}: ${inference.missing_fields.join(", ")}`}</div> : null}
          {inference?.quality.warnings.length ? (
            <div className="warning-list">
              <strong>{labels.qualityWarnings}</strong>
              {inference.quality.warnings.map((warning) => (
                <span key={warning}>{warning}</span>
              ))}
            </div>
          ) : null}
        </article>

        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">RFM</span>
              <h2>{labels.rfmTitle}</h2>
            </div>
          </div>
          <p>{labels.rfmDescription}</p>
          <div className="config-grid">
            <label>
              {labels.sourceCurrency}
              <select value={config.source.source_currency} onChange={(event) => setConfig((current) => ({ ...current, source: { ...current.source, source_currency: event.target.value } }))}>
                <option value="GBP">GBP</option>
                <option value="EUR">EUR</option>
              </select>
            </label>
            <NumberInput label={labels.recencyWeight} value={config.rfm.weights.recency} min={0} max={5} step={0.1} onChange={(value) => updateWeight("recency", value)} />
            <NumberInput label={labels.frequencyWeight} value={config.rfm.weights.frequency} min={0} max={5} step={0.1} onChange={(value) => updateWeight("frequency", value)} />
            <NumberInput label={labels.monetaryWeight} value={config.rfm.weights.monetary} min={0} max={5} step={0.1} onChange={(value) => updateWeight("monetary", value)} />
            <NumberInput label={labels.activeDays} value={config.rfm.active_days} min={1} max={3650} step={1} onChange={(value) => setConfig((current) => ({ ...current, rfm: { ...current.rfm, active_days: value } }))} />
            <NumberInput label={labels.inactiveDays} value={config.rfm.inactive_days} min={1} max={3650} step={1} onChange={(value) => setConfig((current) => ({ ...current, rfm: { ...current.rfm, inactive_days: value } }))} />
            <NumberInput label={labels.clusters} value={config.clustering.n_clusters} min={2} max={12} step={1} onChange={(value) => setConfig((current) => ({ ...current, clustering: { ...current.clustering, n_clusters: value } }))} />
            <label className="check-row">
              <input
                type="checkbox"
                checked={config.clustering.auto_select_k}
                onChange={(event) => setConfig((current) => ({ ...current, clustering: { ...current.clustering, auto_select_k: event.target.checked } }))}
              />
              {labels.autoClusters}
            </label>
          </div>
          <button className="secondary-button fit-button" onClick={handleSaveConfig} disabled={loading}>
            <Settings2 size={16} />
            {labels.saveConfig}
          </button>
        </article>

        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">{labels.status}</span>
              <h2>{status?.customer_count ? `${status.customer_count.toLocaleString()} ${labels.customers}` : labels.notAvailable}</h2>
            </div>
            <Database size={22} />
          </div>
          <div className="status-list">
            <StatusRow title={labels.rawDataset} info={status?.raw_dataset} labels={labels} />
            <StatusRow title={labels.processedCustomers} info={status?.processed_customers} labels={labels} />
          </div>
          <div>
            <strong>{labels.requiredColumns}</strong>
            <div className="column-list">
              {(status?.required_columns ?? []).map((column) => (
                <span key={column}>{column}</span>
              ))}
            </div>
          </div>
        </article>

        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">GBP / EUR</span>
              <h2>{labels.currencyTitle}</h2>
            </div>
          </div>
          <p>{labels.currencyDescription}</p>
          <div className="currency-switch">
            <button className={currency === "GBP" ? "active" : ""} onClick={() => setCurrency("GBP")}>
              {labels.baseCurrency}
            </button>
            <button className={currency === "EUR" ? "active" : ""} onClick={() => setCurrency("EUR")}>
              {labels.convertedCurrency}
            </button>
          </div>
        </article>
      </section>
    </div>
  );
}

function NumberInput({
  label,
  value,
  min,
  max,
  step,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (value: number) => void;
}) {
  return (
    <label>
      {label}
      <input type="number" value={value} min={min} max={max} step={step} onChange={(event) => onChange(Number(event.target.value))} />
    </label>
  );
}

function StatusRow({
  title,
  info,
  labels,
}: {
  title: string;
  info?: { exists: boolean; bytes?: number; modified_at?: number };
  labels: { lastModified: string; notAvailable: string };
}) {
  return (
    <div>
      <strong>{title}</strong>
      <span>{info?.exists ? `${Math.round((info.bytes ?? 0) / 1024).toLocaleString()} KB` : labels.notAvailable}</span>
      <small>
        {labels.lastModified}: {info?.modified_at ? new Date(info.modified_at * 1000).toLocaleString() : labels.notAvailable}
      </small>
    </div>
  );
}
