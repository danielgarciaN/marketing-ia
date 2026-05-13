"use client";

import { useEffect, useState } from "react";
import { Database, RefreshCw, Upload } from "lucide-react";
import { api } from "@/lib/api";
import type { DataStatus, DataUploadResult } from "@/lib/types";
import type { Currency } from "@/lib/format";

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
  };
  currency: Currency;
  setCurrency: (currency: Currency) => void;
  onRefresh: () => Promise<void>;
}) {
  const [status, setStatus] = useState<DataStatus | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [retrain, setRetrain] = useState(true);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadStatus = async () => {
    setStatus(await api.dataStatus());
  };

  useEffect(() => {
    loadStatus().catch((err) => setError(err instanceof Error ? err.message : "Could not load data status"));
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    await runAction(() => api.uploadDataset(file, retrain));
  };

  const handleRetrain = async () => {
    await runAction(() => api.retrainData());
  };

  const runAction = async (action: () => Promise<DataUploadResult>) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      await action();
      await loadStatus();
      await onRefresh();
      setMessage(labels.success);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Data update failed";
      setError(message.includes("404") ? labels.backendOutdated : message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="view-stack">
      <section className="data-grid">
        <article className="data-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">CSV</span>
              <h2>{labels.title}</h2>
            </div>
            <Upload size={22} />
          </div>
          <p>{labels.description}</p>
          <label>
            {labels.selectFile}
            <input type="file" accept=".csv,text/csv" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
          </label>
          <label className="check-row">
            <input type="checkbox" checked={retrain} onChange={(event) => setRetrain(event.target.checked)} />
            {labels.retrain}
          </label>
          <div className="button-row">
            <button className="primary-button" onClick={handleUpload} disabled={!file || loading}>
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
