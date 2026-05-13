import type { SegmentSummary } from "@/lib/types";
import { formatCurrency, segmentClass } from "@/lib/format";
import type { Currency } from "@/lib/format";
import type { Locale } from "@/lib/i18n";
import { segmentLabel } from "@/lib/i18n";

export function SegmentCard({
  segment,
  selected,
  onSelect,
  locale,
  revenueLabel,
  shareLabel,
  currency,
  sourceCurrency = "GBP",
}: {
  segment: SegmentSummary;
  selected: boolean;
  onSelect: (segment: string) => void;
  locale: Locale;
  revenueLabel: string;
  shareLabel: string;
  currency: Currency;
  sourceCurrency?: Currency;
}) {
  return (
    <button className={`segment-card ${selected ? "is-selected" : ""}`} onClick={() => onSelect(segment.segment)}>
      <span className={`segment-dot ${segmentClass(segment.segment)}`} />
      <span className="segment-name">{segmentLabel(segment.segment, locale)}</span>
      <strong>{segment.count.toLocaleString()}</strong>
      <small>
        {formatCurrency(segment.total_revenue, currency, sourceCurrency)} {revenueLabel} - {segment.pct_revenue}% {shareLabel}
      </small>
    </button>
  );
}
