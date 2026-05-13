import { useState, useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, Cell, PieChart, Pie, Legend, LineChart, Line, Area, AreaChart } from "recharts";

const DATA = {
  dashboard: { total_customers: 1984, total_revenue: 1347358.54, total_orders: 15243, avg_order_value: 88.39, avg_frequency: 7.68, active_customers: 881, inactive_customers: 299, top_country: "United Kingdom" },
  revenue: [
    { month: "Dec '10", revenue: 40979 }, { month: "Jan", revenue: 53240 }, { month: "Feb", revenue: 52618 },
    { month: "Mar", revenue: 78860 }, { month: "Apr", revenue: 83441 }, { month: "May", revenue: 103154 },
    { month: "Jun", revenue: 117245 }, { month: "Jul", revenue: 126119 }, { month: "Aug", revenue: 147673 },
    { month: "Sep", revenue: 154980 }, { month: "Oct", revenue: 164653 }, { month: "Nov", revenue: 174392 },
    { month: "Dec '11", revenue: 50005 }
  ],
  segments: [
    { segment: "VIP Customers", count: 535, total_revenue: 1166801, avg_monetary: 2180.94, avg_frequency: 19.14, avg_recency: 9.55, avg_order_value: 89.64, pct_revenue: 86.6, pct_customers: 27.0, color: "#2B5D7E" },
    { segment: "High Potential", count: 254, total_revenue: 96663, avg_monetary: 380.56, avg_frequency: 7.28, avg_recency: 40.48, avg_order_value: 47.05, pct_revenue: 7.2, pct_customers: 12.8, color: "#22D3EE" },
    { segment: "At-Risk Customers", count: 157, total_revenue: 36133, avg_monetary: 230.15, avg_frequency: 5.32, avg_recency: 104.24, avg_order_value: 41.03, pct_revenue: 2.7, pct_customers: 7.9, color: "#F59E0B" },
    { segment: "Loyal Customers", count: 146, total_revenue: 22673, avg_monetary: 155.29, avg_frequency: 5.41, avg_recency: 12.34, avg_order_value: 31.93, pct_revenue: 1.7, pct_customers: 7.4, color: "#10B981" },
    { segment: "Occasional Buyers", count: 293, total_revenue: 12611, avg_monetary: 43.04, avg_frequency: 2.48, avg_recency: 89.69, avg_order_value: 22.42, pct_revenue: 0.9, pct_customers: 14.8, color: "#8B8B8B" },
    { segment: "Lost Customers", count: 500, total_revenue: 8642, avg_monetary: 17.28, avg_frequency: 1.25, avg_recency: 192.9, avg_order_value: 14.12, pct_revenue: 0.6, pct_customers: 25.2, color: "#EF4444" },
    { segment: "New Customers", count: 99, total_revenue: 3836, avg_monetary: 38.74, avg_frequency: 1.75, avg_recency: 13.76, avg_order_value: 20.88, pct_revenue: 0.3, pct_customers: 5.0, color: "#7C3AED" }
  ],
  clusters: {
    0: { size: 312, avg_recency: 260, avg_frequency: 1.4, avg_monetary: 26, traits: ["Inactive/lapsed","Low frequency","Low spend"], label: "Dormant" },
    1: { size: 472, avg_recency: 58, avg_frequency: 3.5, avg_monetary: 93, traits: ["Recent","Low frequency","Low spend"], label: "Casual" },
    2: { size: 533, avg_recency: 26, avg_frequency: 9, avg_monetary: 446, traits: ["Very recent","Above-avg frequency","Moderate spend"], label: "Engaged" },
    3: { size: 376, avg_recency: 88, avg_frequency: 1.3, avg_monetary: 17, traits: ["Lapsed","Very low frequency","Minimal spend"], label: "Churned" },
    4: { size: 291, avg_recency: 9, avg_frequency: 27, avg_monetary: 3613, traits: ["Very recent","Very high frequency","High spend"], label: "Champions" }
  },
  clusterPlot: [{"x":-2.16,"y":-0.36,"c":3},{"x":1.68,"y":0.39,"c":4},{"x":1.0,"y":0.09,"c":2},{"x":-2.5,"y":0.84,"c":0},{"x":-1.33,"y":1.2,"c":0},{"x":2.77,"y":0.86,"c":4},{"x":1.3,"y":0.12,"c":2},{"x":0.59,"y":-0.34,"c":2},{"x":-0.24,"y":-0.21,"c":1},{"x":-2.03,"y":0.85,"c":0},{"x":-0.74,"y":0.31,"c":1},{"x":-1.71,"y":1.39,"c":0},{"x":1.52,"y":-0.08,"c":2},{"x":1.84,"y":0.53,"c":4},{"x":2.16,"y":0.32,"c":4},{"x":0.13,"y":-0.82,"c":1},{"x":0.69,"y":-0.51,"c":2},{"x":-1.72,"y":-0.63,"c":3},{"x":-2.45,"y":0.92,"c":0},{"x":-3.5,"y":1.51,"c":0},{"x":-1.04,"y":0.72,"c":0},{"x":-0.96,"y":-0.75,"c":3},{"x":0.98,"y":0.36,"c":2},{"x":-0.97,"y":-1.54,"c":3},{"x":1.73,"y":0.17,"c":2},{"x":-1.16,"y":-0.85,"c":3},{"x":-0.48,"y":0.58,"c":1},{"x":2.27,"y":0.52,"c":4},{"x":1.01,"y":-0.27,"c":2},{"x":-1.32,"y":-0.85,"c":3},{"x":1.08,"y":-0.11,"c":2},{"x":-0.49,"y":-1.04,"c":1},{"x":-2.36,"y":-0.27,"c":3},{"x":-0.61,"y":-0.57,"c":1},{"x":0.68,"y":-0.28,"c":2},{"x":0.06,"y":0.48,"c":1},{"x":0.42,"y":-0.62,"c":1},{"x":2.28,"y":0.38,"c":4},{"x":1.25,"y":0.02,"c":2},{"x":-0.48,"y":-0.81,"c":1},{"x":-1.4,"y":-1.56,"c":3},{"x":0.64,"y":-0.53,"c":2},{"x":1.62,"y":0.04,"c":2},{"x":-1.75,"y":0.96,"c":0},{"x":-0.58,"y":-0.72,"c":1},{"x":-3.3,"y":1.71,"c":0},{"x":-1.35,"y":0.6,"c":0},{"x":0.47,"y":-0.35,"c":1},{"x":-2.57,"y":1.34,"c":0},{"x":-0.4,"y":1.06,"c":1},{"x":-0.9,"y":-0.28,"c":3},{"x":-0.32,"y":-0.89,"c":1},{"x":-1.06,"y":0.08,"c":3},{"x":2.26,"y":0.59,"c":4},{"x":-0.59,"y":-0.17,"c":1},{"x":-0.25,"y":0.96,"c":1},{"x":1.22,"y":-0.2,"c":2},{"x":-1.7,"y":-0.77,"c":3},{"x":-0.2,"y":1.14,"c":1},{"x":-1.54,"y":-0.85,"c":3},{"x":-2.35,"y":0.28,"c":0},{"x":0.91,"y":-0.08,"c":2},{"x":0.53,"y":-0.46,"c":2},{"x":-0.71,"y":-0.58,"c":1},{"x":1.2,"y":-0.14,"c":2},{"x":0.39,"y":-0.16,"c":1},{"x":0.42,"y":0.16,"c":2},{"x":0.59,"y":-0.63,"c":2},{"x":-0.67,"y":-1.17,"c":3},{"x":-1.55,"y":-1.33,"c":3},{"x":0.46,"y":-0.41,"c":1},{"x":-1.24,"y":-0.61,"c":3},{"x":-1.16,"y":-1.22,"c":3},{"x":1.76,"y":0.4,"c":4},{"x":-1.63,"y":-1.09,"c":3},{"x":1.1,"y":0.0,"c":2},{"x":-0.97,"y":-0.33,"c":3},{"x":-1.09,"y":-0.28,"c":3},{"x":-1.93,"y":0.41,"c":0},{"x":2.23,"y":0.38,"c":4},{"x":1.12,"y":0.25,"c":2},{"x":2.88,"y":0.71,"c":4},{"x":-0.27,"y":1.1,"c":1},{"x":1.21,"y":0.12,"c":2},{"x":0.71,"y":0.18,"c":2},{"x":1.18,"y":-0.27,"c":2},{"x":-0.62,"y":-1.0,"c":3},{"x":1.14,"y":-0.29,"c":2},{"x":-1.94,"y":1.37,"c":0},{"x":0.28,"y":-0.74,"c":1},{"x":-0.0,"y":-0.12,"c":1},{"x":-1.65,"y":0.11,"c":3},{"x":-0.04,"y":-0.33,"c":1},{"x":1.4,"y":-0.06,"c":2},{"x":-2.2,"y":0.51,"c":0},{"x":0.21,"y":-0.57,"c":1},{"x":-2.82,"y":0.38,"c":0},{"x":1.54,"y":0.06,"c":2},{"x":0.83,"y":-0.04,"c":2},{"x":-2.31,"y":1.82,"c":0},{"x":-1.26,"y":-0.94,"c":3}],
  insights: [
    { id: "vip_concentration", category: "Revenue", title: "VIP revenue concentration", insight: "VIP Customers represent 27% of the customer base but generate 86.6% of total revenue (£1,166,801). Prioritize retention campaigns and exclusive benefits.", priority: "Critical", action: "Launch a VIP loyalty program with early access, premium support, and personalized offers.", impact: "High" },
    { id: "at_risk_alert", category: "Retention", title: "At-risk customer alert", insight: "157 customers (7.9%) are at risk of churn. They have an average frequency of 5.3 orders but haven't purchased in 104 days.", priority: "Critical", action: "Deploy a reactivation campaign with personalized discounts (15-20%) within the next 7 days.", impact: "High" },
    { id: "new_conversion", category: "Growth", title: "New customer conversion opportunity", insight: "99 new customers joined recently with an avg order value of £21. The window to convert them into repeat buyers is typically 30 days.", priority: "High", action: "Set up an automated onboarding email series with product recommendations.", impact: "Medium" },
    { id: "revenue_trend", category: "Revenue", title: "Revenue trend analysis", insight: "Revenue over the last 3 months shows a declining trend. November peaked at £174K but December dropped sharply.", priority: "High", action: "Investigate churn drivers and launch promotional campaigns targeting At-Risk segments.", impact: "High" },
    { id: "high_potential", category: "Growth", title: "High potential upsell opportunity", insight: "254 customers show high potential with an average spend of £381 and good recency (40 days). Cross-selling could increase their lifetime value.", priority: "High", action: "Implement personalized product recommendations and bundle offers.", impact: "High" },
    { id: "frequency_gap", category: "Engagement", title: "Purchase frequency gap", insight: "Average frequency is 7.7 orders but median is 4, indicating most customers buy infrequently while a few drive the average up.", priority: "Medium", action: "Design frequency-boosting programs targeting customers with 1-3 purchases.", impact: "High" }
  ],
  recommendations: {
    "VIP Customers": { campaigns: [{ type: "Loyalty Program", objective: "Retain and reward", priority: "High" }, { type: "Early Access", objective: "Increase engagement", priority: "High" }, { type: "Premium Offers", objective: "Increase AOV", priority: "Medium" }], goal: "Maximize retention and lifetime value." },
    "At-Risk Customers": { campaigns: [{ type: "Reactivation Email", objective: "Re-engage", priority: "Critical" }, { type: "Win-Back Survey", objective: "Understand churn", priority: "High" }, { type: "Personalized Offer", objective: "Trigger purchase", priority: "High" }], goal: "Prevent churn before they become lost." },
    "New Customers": { campaigns: [{ type: "Onboarding Series", objective: "Educate and engage", priority: "High" }, { type: "Welcome Discount", objective: "Encourage repeat", priority: "Medium" }], goal: "Convert one-time buyers into repeat customers." },
    "Lost Customers": { campaigns: [{ type: "Win-Back Campaign", objective: "Recovery attempt", priority: "Medium" }, { type: "Strong Incentive", objective: "Break inertia", priority: "Medium" }], goal: "Attempt recovery with strong incentives." },
    "High Potential": { campaigns: [{ type: "Cross-Selling", objective: "Expand range", priority: "High" }, { type: "Up-Selling", objective: "Increase value", priority: "High" }], goal: "Maximize value through cross-sell and up-sell." },
    "Loyal Customers": { campaigns: [{ type: "Referral Program", objective: "Advocacy", priority: "High" }, { type: "Cross-Sell", objective: "Expand basket", priority: "Medium" }], goal: "Nurture loyalty and turn into VIP." },
    "Occasional Buyers": { campaigns: [{ type: "Frequency Boost", objective: "Increase cadence", priority: "Medium" }, { type: "Bundle Offers", objective: "Increase AOV", priority: "Medium" }], goal: "Increase purchase frequency." }
  }
};

const CLUSTER_COLORS = ["#EF4444", "#F59E0B", "#10B981", "#8B8B8B", "#2B5D7E"];
const fmt = (n) => n >= 1000000 ? `£${(n/1000000).toFixed(1)}M` : n >= 1000 ? `£${(n/1000).toFixed(0)}K` : `£${Math.round(n)}`;
const fmtN = (n) => n >= 1000 ? `${(n/1000).toFixed(1)}K` : String(n);

const TABS = ["Overview", "Segments", "Clustering", "Campaigns", "Insights"];

const priorityColors = { Critical: "#EF4444", High: "#F59E0B", Medium: "#22D3EE", Low: "#10B981" };

function KPI({ label, value, sub }) {
  return (
    <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "14px 16px" }}>
      <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 500 }}>{value}</div>
      {sub && <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

function Overview() {
  const d = DATA.dashboard;
  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 10, marginBottom: 24 }}>
        <KPI label="Total customers" value={fmtN(d.total_customers)} />
        <KPI label="Total revenue" value={fmt(d.total_revenue)} />
        <KPI label="Total orders" value={fmtN(d.total_orders)} />
        <KPI label="Avg order value" value={fmt(d.avg_order_value)} />
        <KPI label="Avg frequency" value={`${d.avg_frequency}x`} />
        <KPI label="Active customers" value={d.active_customers} sub="Last 30 days" />
        <KPI label="Inactive" value={d.inactive_customers} sub="> 180 days" />
        <KPI label="Top market" value="UK" sub="82% of customers" />
      </div>
      <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Monthly revenue</div>
      <div style={{ height: 260 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={DATA.revenue}>
            <defs><linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2B5D7E" stopOpacity={0.15}/><stop offset="100%" stopColor="#2B5D7E" stopOpacity={0}/></linearGradient></defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
            <XAxis dataKey="month" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={v => `£${(v/1000).toFixed(0)}K`} tick={{ fontSize: 11 }} width={55} />
            <Tooltip formatter={v => [`£${v.toLocaleString()}`, "Revenue"]} />
            <Area type="monotone" dataKey="revenue" stroke="#2B5D7E" strokeWidth={2} fill="url(#rg)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 24 }}>
        <div>
          <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Revenue by segment</div>
          <div style={{ height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={DATA.segments} dataKey="total_revenue" nameKey="segment" cx="50%" cy="50%" outerRadius={80} innerRadius={40} paddingAngle={2}>
                  {DATA.segments.map((s, i) => <Cell key={i} fill={s.color} />)}
                </Pie>
                <Tooltip formatter={v => fmt(v)} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div>
          <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Customer distribution</div>
          <div style={{ height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={DATA.segments} layout="vertical">
                <XAxis type="number" tick={{ fontSize: 10 }} />
                <YAxis dataKey="segment" type="category" width={100} tick={{ fontSize: 10 }} />
                <Tooltip formatter={v => [v, "Customers"]} />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {DATA.segments.map((s, i) => <Cell key={i} fill={s.color} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

function Segments() {
  const [selected, setSelected] = useState(null);
  const seg = selected ? DATA.segments.find(s => s.segment === selected) : null;
  const rec = selected ? DATA.recommendations[selected] : null;

  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 10, marginBottom: 20 }}>
        {DATA.segments.map(s => (
          <div key={s.segment} onClick={() => setSelected(s.segment)} style={{ background: selected === s.segment ? "var(--color-background-info)" : "var(--color-background-primary)", border: `0.5px solid ${selected === s.segment ? "var(--color-border-info)" : "var(--color-border-tertiary)"}`, borderRadius: "var(--border-radius-lg)", padding: "14px 16px", cursor: "pointer", transition: "all 0.15s" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
              <div style={{ width: 10, height: 10, borderRadius: 3, background: s.color, flexShrink: 0 }} />
              <div style={{ fontSize: 13, fontWeight: 500 }}>{s.segment}</div>
            </div>
            <div style={{ fontSize: 20, fontWeight: 500 }}>{s.count}</div>
            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{s.pct_revenue}% of revenue</div>
          </div>
        ))}
      </div>
      {seg && (
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "20px 24px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
            <div style={{ width: 14, height: 14, borderRadius: 4, background: seg.color }} />
            <div style={{ fontSize: 18, fontWeight: 500 }}>{seg.segment}</div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: 10, marginBottom: 20 }}>
            <KPI label="Customers" value={seg.count} sub={`${seg.pct_customers}% of total`} />
            <KPI label="Revenue" value={fmt(seg.total_revenue)} sub={`${seg.pct_revenue}% of total`} />
            <KPI label="Avg spend" value={fmt(seg.avg_monetary)} />
            <KPI label="Avg frequency" value={`${seg.avg_frequency.toFixed(1)}x`} />
            <KPI label="Avg recency" value={`${Math.round(seg.avg_recency)}d`} />
            <KPI label="Avg order" value={fmt(seg.avg_order_value)} />
          </div>
          {rec && (
            <div>
              <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 8, color: "var(--color-text-secondary)" }}>Recommended campaigns</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {rec.campaigns.map((c, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 14px", background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)" }}>
                    <div style={{ width: 6, height: 6, borderRadius: "50%", background: priorityColors[c.priority], flexShrink: 0 }} />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 13, fontWeight: 500 }}>{c.type}</div>
                      <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{c.objective}</div>
                    </div>
                    <div style={{ fontSize: 11, color: priorityColors[c.priority], fontWeight: 500 }}>{c.priority}</div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginTop: 12, fontStyle: "italic" }}>{rec.goal}</div>
            </div>
          )}
        </div>
      )}
      {!seg && <div style={{ fontSize: 13, color: "var(--color-text-secondary)", textAlign: "center", padding: 32 }}>Select a segment above to see details and campaign recommendations</div>}
    </div>
  );
}

function Clustering() {
  const [hoveredCluster, setHoveredCluster] = useState(null);
  const clusterData = DATA.clusterPlot;
  const clusterInfo = DATA.clusters;
  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 8, marginBottom: 16 }}>
        {Object.entries(clusterInfo).map(([id, c]) => (
          <div key={id} onMouseEnter={() => setHoveredCluster(Number(id))} onMouseLeave={() => setHoveredCluster(null)} style={{ background: hoveredCluster === Number(id) ? "var(--color-background-info)" : "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px", cursor: "pointer", transition: "background 0.15s", borderLeft: `3px solid ${CLUSTER_COLORS[id]}` }}>
            <div style={{ fontSize: 12, fontWeight: 500 }}>{c.label}</div>
            <div style={{ fontSize: 18, fontWeight: 500 }}>{c.size}</div>
            <div style={{ fontSize: 10, color: "var(--color-text-secondary)" }}>£{Math.round(c.avg_monetary)} avg</div>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Customer clusters (PCA projection)</div>
      <div style={{ height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
            <XAxis dataKey="x" name="PC1" tick={{ fontSize: 10 }} />
            <YAxis dataKey="y" name="PC2" tick={{ fontSize: 10 }} />
            <Tooltip formatter={(v, name) => [v.toFixed(2), name]} />
            {[0,1,2,3,4].map(cId => (
              <Scatter key={cId} name={clusterInfo[cId].label} data={clusterData.filter(p => p.c === cId)} fill={CLUSTER_COLORS[cId]} opacity={hoveredCluster !== null && hoveredCluster !== cId ? 0.15 : 0.7} r={4} />
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 14, marginTop: 8, justifyContent: "center" }}>
        {Object.entries(clusterInfo).map(([id, c]) => (
          <div key={id} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11, color: "var(--color-text-secondary)" }}>
            <div style={{ width: 8, height: 8, borderRadius: 2, background: CLUSTER_COLORS[id] }} />
            {c.label} ({c.size})
          </div>
        ))}
      </div>
      <div style={{ marginTop: 20 }}>
        <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Cluster comparison</div>
        <div style={{ height: 200 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={Object.entries(clusterInfo).map(([id, c]) => ({ name: c.label, frequency: c.avg_frequency, monetary: Math.round(c.avg_monetary / 100), recency: Math.round(c.avg_recency) }))}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
              <XAxis dataKey="name" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip />
              <Bar dataKey="frequency" fill="#2B5D7E" name="Avg frequency" radius={[3,3,0,0]} />
              <Bar dataKey="monetary" fill="#22D3EE" name="Avg spend (£100s)" radius={[3,3,0,0]} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function Campaigns() {
  const [segment, setSegment] = useState("VIP Customers");
  const [channel, setChannel] = useState("email");
  const [budget, setBudget] = useState(5000);
  const [discount, setDiscount] = useState(10);
  const [conversion, setConversion] = useState(5);

  const multipliers = { "VIP Customers": 1.5, "Loyal Customers": 1.3, "New Customers": 0.8, "At-Risk Customers": 0.6, "Lost Customers": 0.3, "Occasional Buyers": 0.7, "High Potential": 1.1 };
  const channelCosts = { email: 0.15, sms: 0.25, push: 0.05, retargeting: 0.80 };

  const seg = DATA.segments.find(s => s.segment === segment);
  const adjConv = Math.min(conversion * (multipliers[segment] || 1), 100) / 100;
  const costPer = channelCosts[channel] || 0.15;
  const reached = Math.min(seg.count, Math.floor(budget / costPer));
  const conversions = Math.round(reached * adjConv);
  const revPerConv = seg.avg_order_value * (1 - discount / 100);
  const estRevenue = Math.round(conversions * revPerConv);
  const totalCost = Math.round(reached * costPer + conversions * seg.avg_order_value * (discount / 100));
  const roi = totalCost > 0 ? Math.round(((estRevenue - totalCost) / totalCost) * 100) : 0;

  return (
    <div>
      <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 16 }}>Campaign simulator</div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div>
            <label style={{ fontSize: 12, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Target segment</label>
            <select value={segment} onChange={e => setSegment(e.target.value)} style={{ width: "100%" }}>
              {DATA.segments.map(s => <option key={s.segment} value={s.segment}>{s.segment} ({s.count})</option>)}
            </select>
          </div>
          <div>
            <label style={{ fontSize: 12, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Channel</label>
            <select value={channel} onChange={e => setChannel(e.target.value)} style={{ width: "100%" }}>
              <option value="email">Email (£0.15/user)</option>
              <option value="sms">SMS (£0.25/user)</option>
              <option value="push">Push (£0.05/user)</option>
              <option value="retargeting">Retargeting (£0.80/user)</option>
            </select>
          </div>
          <div>
            <label style={{ fontSize: 12, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Budget: £{budget.toLocaleString()}</label>
            <input type="range" min={500} max={20000} step={500} value={budget} onChange={e => setBudget(Number(e.target.value))} style={{ width: "100%" }} />
          </div>
          <div>
            <label style={{ fontSize: 12, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Discount: {discount}%</label>
            <input type="range" min={0} max={50} step={5} value={discount} onChange={e => setDiscount(Number(e.target.value))} style={{ width: "100%" }} />
          </div>
          <div>
            <label style={{ fontSize: 12, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Base conversion: {conversion}%</label>
            <input type="range" min={1} max={20} step={1} value={conversion} onChange={e => setConversion(Number(e.target.value))} style={{ width: "100%" }} />
          </div>
        </div>
        <div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 16 }}>
            <KPI label="Customers reached" value={reached} />
            <KPI label="Adj. conversion" value={`${(adjConv * 100).toFixed(1)}%`} />
            <KPI label="Expected conversions" value={conversions} />
            <KPI label="Est. revenue" value={fmt(estRevenue)} />
            <KPI label="Campaign cost" value={fmt(totalCost)} />
            <KPI label="Projected ROI" value={<span style={{ color: roi > 0 ? "#10B981" : "#EF4444" }}>{roi > 0 ? "+" : ""}{roi}%</span>} />
          </div>
          <div style={{ background: roi > 100 ? "var(--color-background-success)" : roi > 0 ? "var(--color-background-warning)" : "var(--color-background-danger)", borderRadius: "var(--border-radius-md)", padding: "12px 16px", fontSize: 13 }}>
            <div style={{ fontWeight: 500, marginBottom: 4, color: roi > 100 ? "var(--color-text-success)" : roi > 0 ? "var(--color-text-warning)" : "var(--color-text-danger)" }}>
              {roi > 200 ? "Excellent ROI — strongly recommended" : roi > 50 ? "Good ROI — viable campaign" : roi > 0 ? "Marginal ROI — consider A/B testing" : "Negative ROI — reconsider approach"}
            </div>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>
              {channel} campaign for {segment} with £{budget.toLocaleString()} budget
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Insights() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {DATA.insights.map(ins => (
        <div key={ins.id} style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "16px 20px", borderLeft: `3px solid ${priorityColors[ins.priority]}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
            <span style={{ fontSize: 10, fontWeight: 500, padding: "2px 8px", borderRadius: "var(--border-radius-md)", background: `${priorityColors[ins.priority]}18`, color: priorityColors[ins.priority] }}>{ins.priority}</span>
            <span style={{ fontSize: 10, color: "var(--color-text-secondary)" }}>{ins.category}</span>
          </div>
          <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 6 }}>{ins.title}</div>
          <div style={{ fontSize: 13, color: "var(--color-text-secondary)", lineHeight: 1.5, marginBottom: 10 }}>{ins.insight}</div>
          <div style={{ fontSize: 12, padding: "8px 12px", background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)" }}>
            <span style={{ fontWeight: 500, marginRight: 6 }}>Action:</span>{ins.action}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState("Overview");
  return (
    <div style={{ padding: "0 0 2rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
        <i className="ti ti-brain" aria-hidden="true" style={{ fontSize: 22, color: "#2B5D7E" }}></i>
        <span style={{ fontSize: 18, fontWeight: 500 }}>Marketing intelligence</span>
      </div>
      <div style={{ fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 20 }}>Customer segmentation, RFM analysis, clustering & campaign recommendations</div>
      <div style={{ display: "flex", gap: 2, marginBottom: 20, borderBottom: "0.5px solid var(--color-border-tertiary)", paddingBottom: 0 }}>
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)} style={{ padding: "8px 16px", fontSize: 13, fontWeight: tab === t ? 500 : 400, color: tab === t ? "#2B5D7E" : "var(--color-text-secondary)", background: "transparent", border: "none", borderBottom: tab === t ? "2px solid #2B5D7E" : "2px solid transparent", cursor: "pointer", transition: "all 0.15s" }}>
            {t}
          </button>
        ))}
      </div>
      {tab === "Overview" && <Overview />}
      {tab === "Segments" && <Segments />}
      {tab === "Clustering" && <Clustering />}
      {tab === "Campaigns" && <Campaigns />}
      {tab === "Insights" && <Insights />}
    </div>
  );
}
