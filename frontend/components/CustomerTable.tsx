import type { Customer } from "@/lib/types";
import { formatCurrency } from "@/lib/format";
import type { Locale } from "@/lib/i18n";
import { segmentLabel } from "@/lib/i18n";

export function CustomerTable({
  customers,
  locale,
  labels,
}: {
  customers: Customer[];
  locale: Locale;
  labels: {
    customer: string;
    country: string;
    segment: string;
    revenue: string;
    frequency: string;
    recency: string;
    cluster: string;
  };
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{labels.customer}</th>
            <th>{labels.country}</th>
            <th>{labels.segment}</th>
            <th>{labels.revenue}</th>
            <th>{labels.frequency}</th>
            <th>{labels.recency}</th>
            <th>{labels.cluster}</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.CustomerID}>
              <td>{customer.CustomerID}</td>
              <td>{customer.Country}</td>
              <td>{segmentLabel(customer.Segment, locale)}</td>
              <td>{formatCurrency(customer.Monetary)}</td>
              <td>{customer.Frequency}</td>
              <td>{customer.Recency}d</td>
              <td>{customer.Cluster}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
