export type Currency = "GBP" | "EUR";

export const EUR_RATE = 1.16;

export const convertCurrency = (value: number, currency: Currency, sourceCurrency: Currency = "GBP") => {
  if (currency === sourceCurrency) return value;
  if (sourceCurrency === "GBP" && currency === "EUR") return value * EUR_RATE;
  if (sourceCurrency === "EUR" && currency === "GBP") return value / EUR_RATE;
  return value;
};

export const convertToBaseCurrency = (value: number, currency: Currency, sourceCurrency: Currency = "GBP") =>
  convertCurrency(value, sourceCurrency, currency);

export const formatCurrency = (value: number, currency: Currency = "GBP", sourceCurrency: Currency = "GBP") =>
  new Intl.NumberFormat(currency === "EUR" ? "es-ES" : "en-GB", {
    style: "currency",
    currency,
    maximumFractionDigits: value > 1000 ? 0 : 2,
  }).format(convertCurrency(value, currency, sourceCurrency));

export const convertCurrencyText = (text: string, currency: Currency, sourceCurrency: Currency = "GBP") => {
  if (currency === sourceCurrency) return text;

  return text.replace(/(?:GBP|EUR)\s?([0-9][0-9,]*(?:\.[0-9]+)?)/g, (_, rawAmount: string) => {
    const value = Number(rawAmount.replace(/,/g, ""));
    if (Number.isNaN(value)) return rawAmount;
    return formatCurrency(value, currency, sourceCurrency);
  });
};

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
