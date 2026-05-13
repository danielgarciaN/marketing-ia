import type { Insight } from "@/lib/types";
import type { Locale } from "@/lib/i18n";
import { localizedInsight, priorityLabel } from "@/lib/i18n";

const priorityClass = (priority: string) => {
  const value = priority.toLowerCase();
  if (value === "critical") return "priority-critical";
  if (value === "high") return "priority-high";
  if (value === "medium") return "priority-medium";
  return "priority-low";
};

export function InsightCard({
  insight,
  locale,
  actionLabel,
  impactLabel,
}: {
  insight: Insight;
  locale: Locale;
  actionLabel: string;
  impactLabel: string;
}) {
  const localized = localizedInsight(insight, locale);

  return (
    <article className="insight-card">
      <div>
        <span className="eyebrow">{localized.category}</span>
        <h3>{localized.title}</h3>
      </div>
      <p>{localized.insight}</p>
      <div className="insight-action">
        <strong>{actionLabel}</strong>
        <span>{localized.action}</span>
      </div>
      <div className="chip-row">
        <span className={`chip ${priorityClass(insight.priority)}`}>{priorityLabel(insight.priority, locale)}</span>
        <span className="chip">
          {impactLabel} {priorityLabel(insight.impact, locale)}
        </span>
      </div>
    </article>
  );
}
