"use client";

import React from "react";
import Link from "next/link";
import {
  Shield,
  Cpu,
  BarChart2,
  Lock,
  Database,
  Layers,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  FileCheck2,
  RefreshCw,
  Award,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";

export default function FeaturesPage() {
  const featureBlocks = [
    {
      title: "Deterministic Psychometric Scoring",
      category: "Assessment Engine",
      icon: FileCheck2,
      description:
        "Zero hallucinated scores. Every test question is scored against validated psychometric answer keys using deterministic backend scoring logic. Proficiency levels are calibrated into five tiers (Novice to Expert).",
      bullets: [
        "Calibrated percentage scores and target thresholds",
        "Deterministic blended scoring for repeated evaluations",
        "Zero arbitrary LLM score variations",
      ],
    },
    {
      title: "Immutable Competency History Ledger",
      category: "Competency Radar",
      icon: RefreshCw,
      description:
        "The competency radar updates directly from persisted database state. Each assessment snapshot logs score_before, score_after, delta, confidence, and attempt ID. No fake animations or frontend-only mocks.",
      bullets: [
        "Persisted score_before, score_after, and numerical delta",
        "Confidence score tracking (0.50 to 0.98)",
        "Instant React state invalidation across radar and skill cards",
      ],
    },
    {
      title: "Strict Multi-Track & Tenant Data Isolation",
      category: "Security & Governance",
      icon: Lock,
      description:
        "Enforced server-side in SQLAlchemy database queries. Academic users cannot access Industry records, Industry users cannot access Government records, and only Platform Admin accesses platform-wide audit logs.",
      bullets: [
        "Pre-retrieval role and tenant scope checks",
        "403 Forbidden enforcement on unauthorized cross-org requests",
        "Sanitized immutable audit trail preserving user privacy",
      ],
    },
    {
      title: "AI / RAG Permission Inheritance",
      category: "Knowledge Assistant",
      icon: Cpu,
      description:
        "The RAG knowledge assistant inherits the authenticated user's permissions. Authorization happens strictly before retrieval. Vector search filters only authorized uploaded documents and track-specific resources.",
      bullets: [
        "Zero cross-organization or cross-track vector leakage",
        "Document-grounded citations with exact page numbers",
        "MoSPI official handbook grounding for survey officers",
      ],
    },
    {
      title: "Real Database Aggregated Analytics",
      category: "Workforce Oversight",
      icon: BarChart2,
      description:
        "All metrics (average competency, skill gaps, learning progress, assessment attempts, and training demands) are aggregated live from real database rows without hard-coded numbers or fake random charts.",
      bullets: [
        "Live SQL aggregation per user, organization, and track",
        "Dynamic skill gap heatmaps and training demand forecasts",
        "New-user onboarding roadmap avoiding zero-state clutter",
      ],
    },
    {
      title: "iGOT Karmayogi & NSSTA TPAC Integration",
      category: "Capacity Building Hub",
      icon: Award,
      description:
        "Official course catalog integration for statistical capacity building. Automatically maps detected skill gaps to official government training courses with live API adapters and verified demo fallbacks.",
      bullets: [
        "Live iGOT Karmayogi & NSSTA TPAC course adapters",
        "Automated course recommendations per priority gap",
        "Direct link to national capacity building initiatives",
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-6xl mx-auto px-6 py-12 space-y-12">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full bg-[#EBF3ED] text-forest border border-[#C7DEC9] mb-4">
            <Shield className="w-3.5 h-3.5" />
            <span>Enterprise Technical Specification</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-serif font-bold text-ink tracking-tight">
            Platform Capabilities & Architecture
          </h1>
          <p className="mt-3 text-base text-[#5C5C5C] leading-relaxed">
            Engineered for high-integrity public sector and corporate deployment, combining deterministic psychometrics,
            grounded AI, and rigorous multi-tenant data isolation.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {featureBlocks.map((f, idx) => {
            const Icon = f.icon;
            return (
              <div
                key={idx}
                className="card-institutional p-6 bg-paper border-[#E6E0D2] shadow-xs flex flex-col justify-between hover:border-forest/40 transition-all"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="p-2 rounded bg-[#FAF8F5] text-forest border border-[#E6E0D2]">
                      <Icon className="w-5 h-5" />
                    </span>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#FAF8F5] text-[#8C8275] border border-[#E6E0D2]">
                      {f.category}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-ink font-serif">{f.title}</h3>
                  <p className="text-xs text-[#5C5C5C] mt-2 leading-relaxed">
                    {f.description}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-[#E6E0D2] space-y-1.5 text-xs text-[#2A2A2A]">
                  {f.bullets.map((b, bIdx) => (
                    <div key={bIdx} className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-forest shrink-0" />
                      <span>{b}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Technical Guarantee Banner */}
        <div className="card-institutional p-8 bg-[#FAF8F5] border border-[#E6E0D2] text-center flex flex-col items-center">
          <h3 className="text-xl font-serif font-bold text-ink">
            Ready to Verify Platform Integrity?
          </h3>
          <p className="text-xs text-[#5C5C5C] mt-2 max-w-lg">
            All 12 mandatory security and role isolation criteria are verified via automated end-to-end and integration tests.
          </p>
          <div className="mt-5 flex gap-3">
            <Link
              href="/register"
              className="px-6 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
            >
              Start Diagnostic Assessment
            </Link>
            <Link
              href="/faq"
              className="px-6 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors"
            >
              Read Architectural FAQ
            </Link>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
