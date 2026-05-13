export const formatCurrency = (value: number) =>
  new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    maximumFractionDigits: value > 1000 ? 0 : 2,
  }).format(value);

export const formatNumber = (value: number) =>
  new Intl.NumberFormat("en-GB", { maximumFractionDigits: 1 }).format(value);

export const segmentClass = (segment: string) => {
  const key = segment.toLowerCase();
  if (key.includes("vip")) return "tone-blue";
  if (key.includes("loyal")) return "tone-green";
  if (key.includes("risk")) return "tone-orange";
  if (key.includes("lost")) return "tone-red";
  if (key.includes("new")) return "tone-cyan";
  if (key.includes("potential")) return "tone-purple";
  return "tone-neutral";
};
