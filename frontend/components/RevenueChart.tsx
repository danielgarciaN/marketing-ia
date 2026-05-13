"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { RevenuePoint } from "@/lib/types";
import type { Currency } from "@/lib/format";
import { formatCurrency } from "@/lib/format";

export function RevenueChart({
  data,
  title,
  subtitle,
  tooltipLabel,
  currency,
  sourceCurrency = "GBP",
}: {
  data: RevenuePoint[];
  title: string;
  subtitle: string;
  tooltipLabel: string;
  currency: Currency;
  sourceCurrency?: Currency;
}) {
  return (
    <div className="chart-panel">
      <div className="section-heading">
        <h2>{title}</h2>
        <span>
          {data.length} {subtitle}
        </span>
      </div>
      <div className="chart-height">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="revenueFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2B5D7E" stopOpacity={0.24} />
                <stop offset="100%" stopColor="#22D3EE" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" />
            <XAxis dataKey="month" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={(value) => formatCurrency(Number(value), currency, sourceCurrency)} tick={{ fontSize: 12 }} width={70} />
            <Tooltip formatter={(value) => [formatCurrency(Number(value), currency, sourceCurrency), tooltipLabel]} />
            <Area dataKey="revenue" type="monotone" stroke="#2B5D7E" strokeWidth={2} fill="url(#revenueFill)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
