import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Format a number with commas: 10127 → "10,127" */
export function formatNumber(n: number | null | undefined): string {
  if (n == null) return "0";
  return n.toLocaleString("en-US");
}

/** Format a percentage: 16.065 → "16.1%" */
export function formatPct(n: number | null | undefined, decimals = 1): string {
  if (n == null) return "0%";
  return `${n.toFixed(decimals)}%`;
}

/** Format currency: 12691.5 → "$12,692" */
export function formatCurrency(n: number | null | undefined): string {
  if (n == null) return "$0";
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

/** Shorten and format long category names for UI charts */
export function formatCategory(str: string | null | undefined): string {
  if (!str) return "Unknown";
  
  const mapping: Record<string, string> = {
    "Credit reporting, credit repair services, or other personal consumer reports": "Credit Reporting",
    "Checking or savings account": "Checking/Savings",
    "Credit card or prepaid card": "Credit/Prepaid Card",
    "Debt collection": "Debt Collection",
    "Payday loan, title loan, or personal loan": "Personal/Payday Loan",
    "Money transfer, virtual currency, or money service": "Money Transfer",
    "Vehicle loan or lease": "Vehicle Loan",
    "professional.course": "Prof. Course",
    "university.degree": "Univ. Degree",
    "high.school": "High School",
    "basic.9y": "Basic 9Y",
    "basic.6y": "Basic 6Y",
    "basic.4y": "Basic 4Y",
    "admin.": "Admin",
    "blue-collar": "Blue Collar",
    "self-employed": "Self Employed",
    "grocery_pos": "Grocery POS",
    "grocery_net": "Grocery Online",
    "shopping_pos": "Shopping POS",
    "shopping_net": "Shopping Online",
    "misc_pos": "Misc POS",
    "misc_net": "Misc Online",
    "health_fitness": "Health & Fitness",
    "food_dining": "Food & Dining",
    "personal_care": "Personal Care",
    "gas_transport": "Gas & Transport",
    "kids_pets": "Kids & Pets",
  };

  if (mapping[str]) return mapping[str];

  return str
    .replace(/[_\.]/g, " ")
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
