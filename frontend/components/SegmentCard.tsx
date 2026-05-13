import type { SegmentSummary } from "@/lib/types";
import { formatCurrency, segmentClass } from "@/lib/format";
import type { Locale } from "@/lib/i18n";
import { segmentLabel } from "@/lib/i18n";

export function SegmentCard({
  segment,
  selected,
  onSelect,
  locale,
  revenueLabel,
  shareLabel,
}: {
  segment: SegmentSummary;
  selected: boolean;
  onSelect: (segment: string) => void;
  locale: Locale;
  revenueLabel: string;
  shareLabel: string;
}) {
  return (
    <button className={`segment-card ${selected ? "is-selected" : ""}`} onClick={() => onSelect(segment.segment)}>
      <span className={`segment-dot ${segmentClass(segment.segment)}`} />
      <span className="segment-name">{segmentLabel(segment.segment, locale)}</span>
      <strong>{segment.count.toLocaleString()}</strong>
      <small>
        {formatCurrency(segment.total_revenue)} {revenueLabel} - {segment.pct_revenue}% {shareLabel}
      </small>
    </button>
  );
}
