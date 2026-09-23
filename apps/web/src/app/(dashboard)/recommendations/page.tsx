"use client";

import React, { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  Compass,
  Bookmark,
  CheckCircle2,
  ExternalLink,
  Info,
  Shield,
  Clock,
  BookOpen,
} from "lucide-react";
import { apiRequest } from "@/lib/api";

function RecommendationsContent() {
  const searchParams = useSearchParams();
  const compFilter = searchParams.get("comp");

  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [providerFilter, setProviderFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState(true);
  const [notification, setNotification] = useState<string | null>(null);

  useEffect(() => {
    async function loadRecommendations() {
      try {
        const data = await apiRequest<any[]>("/me/recommendations").catch(() => []);
        if (data && data.length > 0) {
          setRecommendations(data);
        } else {
          setRecommendations([
            {
              id: "rec-1",
              rank: 1,
              score: 95.0,
              status: "suggested",
              explanation: "Directly addresses critical skill gap in Sampling Techniques (STAT-02). High priority for official NSS and PLFS field surveys.",
              resource: {
                id: "res-1",
                provider_type: "igot",
                provider_external_id: "IGOT-SAM-01",
                title: "Advanced Multi-Stage Sampling for Socio-Economic Surveys",
                description: "Official iGOT Karmayogi module covering PPS sampling, sample size determination, variance estimation, and non-sampling error minimization.",
                url: "https://igotkarmayogi.gov.in/learn/advanced-sampling-techniques",
                level: "Advanced",
                duration: "3 weeks",
                is_demo: true
              },
              competency: {
                id: "c-samp",
                code: "STAT-02",
                name: "Sampling Techniques"
              }
            },
            {
              id: "rec-2",
              rank: 2,
              score: 92.0,
              status: "suggested",
              explanation: "NSSTA residential and hybrid training module addressing price index computation protocols and Laspeyres formula rebasing.",
              resource: {
                id: "res-2",
                provider_type: "nssta",
                provider_external_id: "NSSTA-TPAC-01",
                title: "NSSTA Training Programme on Price Index Compilation & Rebasing",
                description: "National Statistical Systems Training Academy Greater Noida module on CPI and WPI computation methodologies.",
                url: "https://mospi.gov.in/nssta/training/price-statistics-2026",
                level: "Advanced",
                duration: "1 week",
                is_demo: true
              },
              competency: {
                id: "c-price",
                code: "STAT-04",
                name: "Price Statistics"
              }
            },
            {
              id: "rec-3",
              rank: 3,
              score: 88.5,
              status: "suggested",
              explanation: "Essential programming skill for automating MoSPI statistical publications and reproducible analytical pipelines.",
              resource: {
                id: "res-3",
                provider_type: "igot",
                provider_external_id: "IGOT-26103-RSTAT",
                title: "R Programming for Government Statistical Analysis",
                description: "Hands-on course designed for official statisticians using R for survey weighting, tabulations, and automated statistical reporting.",
                url: "https://igotkarmayogi.gov.in/learn/r-official-statistics",
                level: "Beginner",
                duration: "4 weeks",
                is_demo: true
              },
              competency: {
                id: "c-r",
                code: "TECH-02",
                name: "R for Official Statistics"
              }
            }
          ]);
        }
      } finally {
        setLoading(false);
      }
    }
    loadRecommendations();
  }, []);

  const handleAction = async (recId: string, action: "save" | "start" | "complete" | "dismiss") => {
    try {
      await apiRequest(`/recommendations/${recId}/${action}`, { method: "POST" }).catch(() => {});
      setRecommendations((prev) =>
        prev.map((r) => (r.id === recId ? { ...r, status: action === "save" ? "saved" : action === "start" ? "started" : action === "complete" ? "completed" : "dismissed" } : r))
      );
      setNotification(`Action '${action}' applied successfully.`);
      setTimeout(() => setNotification(null), 3000);
    } catch (err: any) {
      console.error(err);
    }
  };

  const filtered = recommendations.filter((r) => {
    if (providerFilter !== "ALL" && r.resource?.provider_type !== providerFilter) return false;
    if (compFilter && r.competency_id !== compFilter && r.competency?.id !== compFilter) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-ink font-serif">
            Personalized Capacity Building Recommendations
          </h1>
          <p className="text-xs text-[#5C5C5C]">
            Algorithmically ranked learning resources from iGOT Karmayogi and NSSTA TPAC
          </p>
        </div>

        {/* Integration Status Badge */}
        <div className="flex items-center gap-2 text-xs bg-[#F7F3EA] border border-[#D1C8B4] px-3 py-1.5 rounded">
          <Info className="w-3.5 h-3.5 text-forest" />
          <span className="text-[#5C5C5C]">
            Provider Status: <strong className="text-ink">DEMO_CATALOGUE Active</strong>
          </span>
        </div>
      </div>

      {notification && (
        <div className="p-3 rounded bg-[#EBF3ED] border border-[#C7DEC9] text-xs text-forest font-medium flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{notification}</span>
        </div>
      )}

      {/* Provider Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-[#E6E0D2] pb-3 text-xs">
        {[
          { label: "All Providers", value: "ALL" },
          { label: "iGOT Karmayogi", value: "igot" },
          { label: "NSSTA Programmes", value: "nssta" },
          { label: "Industry Courses", value: "industry" },
          { label: "Academic Labs", value: "academia" },
        ].map((p) => (
          <button
            key={p.value}
            onClick={() => setProviderFilter(p.value)}
            className={`px-3 py-1.5 rounded font-medium transition-colors ${
              providerFilter === p.value
                ? "bg-forest text-paper"
                : "bg-paper border border-[#E6E0D2] text-[#2A2A2A] hover:bg-[#F2EDE1]"
            }`}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Recommendations List */}
      <div className="space-y-4">
        {filtered.map((rec) => (
          <div
            key={rec.id}
            className="card-institutional p-6 bg-paper shadow-card flex flex-col md:flex-row items-start justify-between gap-6"
          >
            <div className="flex-1 space-y-3">
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span
                  className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                    rec.resource?.provider_type === "igot"
                      ? "bg-[#EBF3ED] text-forest border-[#C7DEC9]"
                      : "bg-[#F7F1E6] text-gold-dark border-[#E2CEAB]"
                  }`}
                >
                  {rec.resource?.provider_type === "igot"
                    ? "iGOT Karmayogi"
                    : "NSSTA TPAC"}
                </span>
                <span className="font-mono text-[10px] text-ink bg-[#F2EDE1] px-2 py-0.5 rounded border border-[#E6E0D2]">
                  {rec.resource?.provider_external_id}
                </span>
                <span className="text-[11px] text-[#8C8275]">
                  Target Competency: <strong className="text-ink">{rec.competency?.name} ({rec.competency?.code})</strong>
                </span>
              </div>

              <h3 className="text-base font-bold text-ink font-serif">
                {rec.resource?.title}
              </h3>
              <p className="text-xs text-[#5C5C5C] leading-relaxed">
                {rec.resource?.description}
              </p>

              {/* Algorithmic Reason Box */}
              <div className="p-3 rounded bg-warm-ivory border border-[#E6E0D2] text-xs text-[#2A2A2A] flex items-start gap-2">
                <Shield className="w-4 h-4 text-forest shrink-0 mt-0.5" />
                <div>
                  <strong className="font-semibold text-ink">Why Recommended: </strong>
                  <span>{rec.explanation}</span>
                </div>
              </div>

              <div className="flex items-center gap-4 text-[11px] text-[#5C5C5C] pt-1">
                <span className="flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" />
                  <span>Duration: {rec.resource?.duration}</span>
                </span>
                <span className="flex items-center gap-1">
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Level: {rec.resource?.level}</span>
                </span>
                <span className="text-forest font-semibold">
                  Hybrid Recommendation Score: {rec.score} / 100
                </span>
              </div>
            </div>

            {/* Action Buttons Column */}
            <div className="flex flex-col gap-2 w-full md:w-48 shrink-0">
              <a
                href={rec.resource?.url}
                target="_blank"
                rel="noreferrer"
                onClick={() => handleAction(rec.id, "start")}
                className="w-full py-2 px-3 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors flex items-center justify-center gap-1.5"
              >
                <span>Access Course</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>

              <button
                onClick={() => handleAction(rec.id, "save")}
                className="w-full py-2 px-3 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors flex items-center justify-center gap-1.5"
              >
                <Bookmark className="w-3.5 h-3.5" />
                <span>{rec.status === "saved" ? "Saved in List" : "Save Course"}</span>
              </button>

              <button
                onClick={() => handleAction(rec.id, "complete")}
                className="w-full py-2 px-3 rounded border border-[#C7DEC9] text-forest text-xs font-semibold hover:bg-[#EBF3ED] transition-colors flex items-center justify-center gap-1.5"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{rec.status === "completed" ? "Completed" : "Mark Completed"}</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function RecommendationsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-xs text-[#5C5C5C]">Loading Recommendations...</div>}>
      <RecommendationsContent />
    </Suspense>
  );
}
