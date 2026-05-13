type DashboardCardProps = {
  label: string;
  value: string;
  detail?: string;
  tone?: "blue" | "green" | "orange" | "red" | "cyan";
};

export function DashboardCard({ label, value, detail, tone = "blue" }: DashboardCardProps) {
  return (
    <article className={`metric-card metric-card-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      {detail ? <small>{detail}</small> : null}
    </article>
  );
}
