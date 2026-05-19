"use client";

import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { AlertTriangle, CheckCircle2, Database, Info, RefreshCw, Settings2, Trash2, Upload, X } from "lucide-react";
import { api } from "@/lib/api";
import type { DataFieldMetadata, DataStatus, DataUploadResult, DatasetRecord, DatasetRegistry, PipelineConfig, SchemaInference } from "@/lib/types";
import { formatCurrency, type Currency } from "@/lib/format";

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
  onRefresh,
}: {
  labels: Record<string, string>;
  currency: Currency;
  onRefresh: () => Promise<void>;
}) {
  const [status, setStatus] = useState<DataStatus | null>(null);
  const [registry, setRegistry] = useState<DatasetRegistry | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [inference, setInference] = useState<SchemaInference | null>(null);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [config, setConfig] = useState<PipelineConfig>(defaultConfig);
  const [retrain, setRetrain] = useState(true);
  const [loading, setLoading] = useState(false);
  const [inferring, setInferring] = useState(false);
  const [mappingOpen, setMappingOpen] = useState(false);
  const [configOpen, setConfigOpen] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sourceCurrency = config.source.source_currency === "EUR" ? "EUR" : "GBP";
  const fieldMetadata = useMemo<DataFieldMetadata[]>(() => inference?.field_metadata ?? status?.required_fields ?? [], [inference, status]);

  const loadStatus = async () => {
    const [currentStatus, currentRegistry] = await Promise.all([api.dataStatus(), api.datasets()]);
    setStatus(currentStatus);
    setRegistry(currentRegistry);
    if (currentStatus.config) {
      setConfig(currentStatus.config);
      setMapping(currentStatus.config.source.column_mapping ?? {});
    }
  };

  useEffect(() => {
    loadStatus().catch((err) => setError(err instanceof Error ? err.message : labels.loadError));
  }, []);

  const handleFile = async (nextFile: File | null) => {
    setFile(nextFile);
    setInference(null);
    setError(null);
    setMessage(null);
    setMappingOpen(false);
    if (!nextFile) return;

    setInferring(true);
    try {
      const result = await api.inferSchema(nextFile);
      setInference(result);
      setMapping(result.mapping);
      setMessage(result.needs_manual_review ? labels.reviewNeeded : labels.autoMapped);
      if (result.needs_manual_review) setMappingOpen(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : labels.schemaFailed);
    } finally {
      setInferring(false);
    }
  };

  const configPayload = (): Partial<PipelineConfig> => ({
    source: { ...config.source, source_currency: config.source.source_currency, column_mapping: mapping },
    rfm: config.rfm,
    clustering: config.clustering,
  });

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
      const current = err instanceof Error ? err.message : labels.updateFailed;
      setError(current.includes("404") ? labels.backendOutdated : current);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    await runAction(() => api.uploadDataset(file, retrain, mapping, configPayload()));
  };

  const handleRetrain = async () => {
    await runAction(() => api.retrainData(configPayload()), labels.retrained);
  };

  const handleSaveConfig = async () => {
    await runAction(async () => {
      const saved = await api.saveConfig(configPayload());
      setConfig(saved);
      return { status: "saved", config: saved };
    }, labels.configSaved);
    setConfigOpen(false);
  };

  const toggleDataset = async (dataset: DatasetRecord) => {
    await runAction(() => api.setDatasetActive(dataset.id, !dataset.active), dataset.active ? labels.datasetDisabled : labels.datasetEnabled);
  };

  const removeDataset = async (dataset: DatasetRecord) => {
    await runAction(() => api.deleteDataset(dataset.id), labels.datasetDeleted);
  };

  const updateWeight = (key: keyof PipelineConfig["rfm"]["weights"], value: number) => {
    setConfig((current) => ({ ...current, rfm: { ...current.rfm, weights: { ...current.rfm.weights, [key]: value } } }));
  };

  return (
    <div className="view-stack">
      <section className="metrics-grid compact">
        <MiniMetric label={labels.activeDatasets} value={String(registry?.active_datasets ?? 0)} detail={`${registry?.total_datasets ?? 0} ${labels.totalDatasets}`} />
        <MiniMetric label={labels.activeCustomers} value={(registry?.active_customers ?? status?.customer_count ?? 0).toLocaleString()} detail={labels.feedsDashboard} />
        <MiniMetric label={labels.activeRows} value={(registry?.active_rows ?? 0).toLocaleString()} detail={formatCurrency(registry?.active_revenue ?? 0, currency, sourceCurrency)} />
      </section>

      <section className="data-management-grid">
        <article className="data-panel upload-center">
          <div className="section-heading">
            <div>
              <span className="eyebrow">{labels.dataCenter}</span>
              <h2>{labels.title}</h2>
            </div>
            <Upload size={22} />
          </div>
          <p>{labels.description}</p>
          <label>
            {labels.selectFile}
            <input type="file" accept=".csv,.xlsx,.xls,text/csv" onChange={(event) => handleFile(event.target.files?.[0] ?? null)} />
          </label>

          {inference ? (
            <div className={`smart-mapping-card ${inference.needs_manual_review ? "needs-review" : ""}`}>
              {inference.needs_manual_review ? <AlertTriangle size={20} /> : <CheckCircle2 size={20} />}
              <div>
                <strong>{inference.needs_manual_review ? labels.reviewNeeded : labels.autoMapped}</strong>
                <span>
                  {inference.columns.length} {labels.columnsDetected} - {inference.quality.rows.toLocaleString()} {labels.previewRows}
                </span>
              </div>
              <button className="secondary-button compact-button" onClick={() => setMappingOpen(true)}>
                <Settings2 size={15} />
                {labels.advancedMapping}
              </button>
            </div>
          ) : null}

          <label className="check-row">
            <input type="checkbox" checked={retrain} onChange={(event) => setRetrain(event.target.checked)} />
            {labels.retrain}
          </label>
          <div className="button-row">
            <button className="primary-button" onClick={handleUpload} disabled={!file || loading || inferring}>
              <Upload size={16} />
              {inferring ? labels.detecting : loading ? labels.uploading : labels.upload}
            </button>
            <button className="secondary-button" onClick={handleRetrain} disabled={loading}>
              <RefreshCw size={16} />
              {loading ? labels.refreshing : labels.retrainOnly}
            </button>
            <button className="secondary-button" onClick={() => setConfigOpen(true)}>
              <Settings2 size={16} />
              {labels.configureModel}
            </button>
          </div>
          {message ? <div className="success-state">{message}</div> : null}
          {error ? <div className="error-inline">{error}</div> : null}
        </article>

        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">{labels.status}</span>
              <h2>{labels.pipelineInputs}</h2>
            </div>
            <Database size={22} />
          </div>
          <div className="status-list">
            <StatusRow title={labels.rawDataset} info={status?.raw_dataset} labels={labels} />
            <StatusRow title={labels.processedCustomers} info={status?.processed_customers} labels={labels} />
          </div>
          <p>{labels.pipelineDescription}</p>
        </article>
      </section>

      <section className="data-panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">{labels.datasets}</span>
            <h2>{labels.datasetLibrary}</h2>
          </div>
          <InfoTip text={labels.datasetLibraryTip} />
        </div>
        <div className="dataset-list">
          {(registry?.datasets ?? []).map((dataset) => (
            <DatasetRow
              key={dataset.id}
              dataset={dataset}
              labels={labels}
              currency={currency}
              sourceCurrency={sourceCurrency}
              disabled={loading}
              onToggle={() => toggleDataset(dataset)}
              onDelete={() => removeDataset(dataset)}
            />
          ))}
          {registry && registry.datasets.length === 0 ? <div className="empty-state">{labels.noDatasets}</div> : null}
        </div>
      </section>

      {mappingOpen ? (
        <Modal title={labels.advancedMapping} onClose={() => setMappingOpen(false)}>
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
          {inference?.quality.warnings.length ? (
            <div className="warning-list">
              <strong>{labels.qualityWarnings}</strong>
              {inference.quality.warnings.map((warning) => (
                <span key={warning}>{warning}</span>
              ))}
            </div>
          ) : null}
        </Modal>
      ) : null}

      {configOpen ? (
        <Modal title={labels.configureModel} onClose={() => setConfigOpen(false)}>
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
          <div className="modal-actions">
            <button className="secondary-button" onClick={() => setConfigOpen(false)}>{labels.close}</button>
            <button className="primary-button" onClick={handleSaveConfig} disabled={loading}>{labels.saveConfig}</button>
          </div>
        </Modal>
      ) : null}
    </div>
  );
}

function MiniMetric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function DatasetRow({
  dataset,
  labels,
  currency,
  sourceCurrency,
  disabled,
  onToggle,
  onDelete,
}: {
  dataset: DatasetRecord;
  labels: Record<string, string>;
  currency: Currency;
  sourceCurrency: Currency;
  disabled: boolean;
  onToggle: () => void;
  onDelete: () => void;
}) {
  return (
    <article className="dataset-row">
      <div>
        <div className="dataset-title-row">
          <strong>{dataset.filename}</strong>
          <span className={`status-chip ${dataset.active ? "active" : ""}`}>{dataset.active ? labels.active : labels.inactive}</span>
        </div>
        <small>
          {dataset.file_type.toUpperCase()} - {formatBytes(dataset.size_bytes)} - {new Date(dataset.uploaded_at).toLocaleString()}
        </small>
      </div>
      <div className="dataset-stats">
        <span>{dataset.stats.customers.toLocaleString()} {labels.customers}</span>
        <span>{dataset.stats.rows.toLocaleString()} {labels.rows}</span>
        <span>{formatCurrency(dataset.stats.revenue, currency, sourceCurrency)}</span>
      </div>
      <div className="dataset-actions">
        <button className="secondary-button compact-button" onClick={onToggle} disabled={disabled}>
          {dataset.active ? labels.disable : labels.enable}
        </button>
        <button className="danger-button compact-button" onClick={onDelete} disabled={disabled}>
          <Trash2 size={15} />
          {labels.delete}
        </button>
      </div>
    </article>
  );
}

function Modal({ title, children, onClose }: { title: string; children: ReactNode; onClose: () => void }) {
  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true">
      <div className="modal-panel">
        <div className="section-heading">
          <h2>{title}</h2>
          <button className="icon-button" onClick={onClose} aria-label="Close"><X size={16} /></button>
        </div>
        {children}
      </div>
    </div>
  );
}

function InfoTip({ text }: { text: string }) {
  return (
    <span className="info-tip" tabIndex={0}>
      <Info size={15} />
      <span>{text}</span>
    </span>
  );
}

function NumberInput({ label, value, min, max, step, onChange }: { label: string; value: number; min: number; max: number; step: number; onChange: (value: number) => void }) {
  return (
    <label>
      {label}
      <input type="number" value={value} min={min} max={max} step={step} onChange={(event) => onChange(Number(event.target.value))} />
    </label>
  );
}

function StatusRow({ title, info, labels }: { title: string; info?: { exists: boolean; bytes?: number; modified_at?: number }; labels: Record<string, string> }) {
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

function formatBytes(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024).toLocaleString()} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}
