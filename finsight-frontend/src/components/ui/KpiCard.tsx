interface KpiCardProps {
  label: string;
  value: string;
  icon?: string;
  trend?: string;
  trendDirection?: "up" | "down" | "neutral";
  accentColor?: string;
}

/** KPI metric card for dashboard headers. */
export default function KpiCard({
  label,
  value,
  icon,
  trend,
  trendDirection = "neutral",
  accentColor,
}: KpiCardProps) {
  const trendColor =
    trendDirection === "up"
      ? "text-emerald-400"
      : trendDirection === "down"
        ? "text-rose-400"
        : "text-slate-400";

  return (
    <div className="kpi-card relative overflow-hidden">
      {/* Accent bar */}
      {accentColor && (
        <div
          className="absolute top-0 left-0 right-0 h-[3px] rounded-t-xl"
          style={{ background: accentColor }}
        />
      )}
      <div className="flex items-start justify-between">
        <div>
          <p className="kpi-label">{label}</p>
          <p className="kpi-value mt-1">{value}</p>
          {trend && (
            <p className={`text-xs mt-1.5 font-medium ${trendColor}`}>
              {trend}
            </p>
          )}
        </div>
        {icon && <span className="text-2xl opacity-60">{icon}</span>}
      </div>
    </div>
  );
}
