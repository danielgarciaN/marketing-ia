"use client";

import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { ClusterPoint } from "@/lib/types";
import { formatCurrency } from "@/lib/format";
import type { Currency } from "@/lib/format";

const COLORS = ["#2B5D7E", "#22D3EE", "#10B981", "#F59E0B", "#EF4444", "#7C3AED"];

export function ClusterScatterPlot({
  points,
  title,
  subtitle,
  revenueLabel,
  currency,
  sourceCurrency = "GBP",
}: {
  points: ClusterPoint[];
  title: string;
  subtitle: string;
  revenueLabel: string;
  currency: Currency;
  sourceCurrency?: Currency;
}) {
  const clusters = Array.from(new Set(points.map((point) => point.Cluster))).sort((a, b) => a - b);

  return (
    <div className="chart-panel">
      <div className="section-heading">
        <h2>{title}</h2>
        <span>{subtitle}</span>
      </div>
      <div className="chart-height">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 8, right: 12, bottom: 8, left: 0 }}>
            <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" />
            <XAxis dataKey="PCA_1" name="PC1" tick={{ fontSize: 12 }} />
            <YAxis dataKey="PCA_2" name="PC2" tick={{ fontSize: 12 }} />
            <Tooltip
              cursor={{ strokeDasharray: "3 3" }}
              formatter={(value, name) => {
                if (name === "Monetary") return [formatCurrency(Number(value), currency, sourceCurrency), revenueLabel];
                return [Number(value).toFixed(2), name];
              }}
            />
            {clusters.map((cluster) => (
              <Scatter
                key={cluster}
                data={points.filter((point) => point.Cluster === cluster)}
                fill={COLORS[cluster % COLORS.length]}
                name={`Cluster ${cluster}`}
              />
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      </div>
      <div className="legend-row">
        {clusters.map((cluster) => (
          <span key={cluster}>
            <i style={{ backgroundColor: COLORS[cluster % COLORS.length] }} />
            Cluster {cluster}
          </span>
        ))}
      </div>
    </div>
  );
}
