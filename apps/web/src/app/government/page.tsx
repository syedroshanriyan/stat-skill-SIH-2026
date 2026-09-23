"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Building2,
  ShieldCheck,
  FileCheck2,
  Compass,
  ArrowRight,
  CheckCircle2,
  ExternalLink,
  BookOpen,
  Info,
  Layers,
  Sparkles,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";
import { getStoredUser, StoredUser } from "@/lib/api";

export default function GovernmentPublicPage() {
  const [user, setUser] = useState<StoredUser | null>(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const statisticalDomains = [
    { name: "Survey Design & Instrumentation", code: "STAT-01", level: "Level 3 Target", status: "Evaluated (72%)", desc: "Questionnaire design, household schedule formulation, and non-sampling error reduction." },
    { name: "Sampling Techniques & Estimation", code: "STAT-02", level: "Level 4 Target", status: "Critical Gap (55%)", desc: "Multi-stage stratified sampling, PPS selection, weighting procedures, and variance calculation." },
    { name: "National Accounts & GVA Compilation", code: "STAT-03", level: "Level 3 Target", status: "Evaluated (68%)", desc: "System of National Accounts (SNA 2008), gross value added, and institutional sector accounts." },
    { name: "Price Statistics (CPI / WPI)", code: "STAT-04", level: "Level 3 Target", status: "High Gap (45%)", desc: "Laspeyres index compilation, price quotation validation, substitution bias, and base revision." },
    { name: "SDG Indicators Monitoring Framework", code: "STAT-05", level: "Level 3 Target", status: "Evaluated (58%)", desc: "National Indicator Framework (NIF), metadata standards, and inter-agency data synchronization." },
    { name: "Data Quality Frameworks (DQAF)", code: "STAT-06", level: "Level 4 Target", status: "Benchmark Met (80%)", desc: "IMF DQAF and MoSPI Data Quality standards: accuracy, timeliness, accessibility, and credibility." },
  ];

  const technicalDomains = [
    { name: "Python for Official Data Analytics", code: "TECH-01", target: "Pandas & Numerical Modeling", focus: "Automated survey data validation scripts" },
    { name: "R for Official Statistics", code: "TECH-02", target: "Survey Package by Lumley", focus: "Complex survey weighting and stratified sample estimation" },
    { name: "SQL & Relational Microdata Queries", code: "TECH-03", target: "Analytical Window Functions", focus: "Large-scale census and NSS microdata extraction" },
    { name: "GIS & Spatial Boundary Profiling", code: "TECH-04", target: "District Boundary Shapefiles", focus: "QGIS integration for census enumeration block mapping" },
    { name: "Cybersecurity & DPDP Act Compliance", code: "GOV-01", target: "Digital Personal Data Protection", focus: "Microdata anonymization & Statistical Disclosure Limitation (SDL)" },
  ];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-6xl mx-auto px-6 py-12 space-y-10">
        {/* Logged in state banner */}
        {user && user.track === "GOVERNMENT" && (
          <div className="p-4 rounded-lg bg-[#EBF3ED] border border-[#C7DEC9] flex items-center justify-between">
            <div className="flex items-center gap-2.5 text-xs text-forest font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>You are logged in as {user.display_name} (Government Official)</span>
            </div>
            <Link
              href="/dashboard"
              className="text-xs font-bold text-forest hover:text-forest-dark flex items-center gap-1 underline underline-offset-2"
            >
              <span>Go to Active Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}

        {/* Top Track Banner */}
        <div className="card-institutional p-8 bg-paper border-forest/40 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-[#EBF3ED] text-forest border border-[#C7DEC9] px-2.5 py-0.5 rounded">
                Official Capacity Framework
              </span>
              <span className="text-xs text-[#5C5C5C]">
                MoSPI / DIID Official Statistical Framework
              </span>
            </div>
            <h1 className="text-3xl font-bold text-ink font-serif mt-2">
              Government & Official Statistics Track
            </h1>
            <p className="text-xs text-[#5C5C5C] mt-2 max-w-2xl leading-relaxed">
              Automated institutional competency evaluation, continuous skill-gap identification,
              iGOT Karmayogi course alignment, and NSSTA TPAC statistical training for statistical officers,
              ISS probationers, and directorate analysts.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
            <Link
              href="/register"
              className="px-5 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors flex items-center justify-center gap-2 shadow-sm"
            >
              <FileCheck2 className="w-4 h-4" />
              <span>Take Diagnostic Assessment</span>
            </Link>
            <Link
              href="/login"
              className="px-5 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors text-center"
            >
              Official Sign In
            </Link>
          </div>
        </div>

        {/* Government Track Pathway Roadmap */}
        <div className="card-institutional p-6 bg-paper border-[#E6E0D2]">
          <p className="text-[10px] uppercase font-bold tracking-widest text-[#8C8275] mb-2">
            The Government Pathway
          </p>
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-ink">
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Official Profile</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#EBF3ED] text-forest font-bold border border-[#C7DEC9]">Diagnostic Assessment</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F9ECE7] text-terracotta font-bold border border-[#E5C1B4]">Skill Gap Analysis</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F7F1E6] text-gold-dark font-bold border border-[#E2CEAB]">iGOT / NSSTA Hub</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Cohort Training</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#EBF3ED] text-forest font-bold border border-[#C7DEC9]">Grounded Assessment</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-forest text-paper font-bold">Competency Growth</span>
          </div>
        </div>

        {/* Integration Architecture */}
        <div className="p-4 rounded-lg bg-[#FAF8F3] border border-[#E6E0D2] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-xs">
          <div className="flex items-center gap-3">
            <Info className="w-5 h-5 text-forest shrink-0" />
            <div>
              <h4 className="font-bold text-ink">
                Official MoSPI Provider Integration Architecture
              </h4>
              <p className="text-[11px] text-[#5C5C5C]">
                iGOT Karmayogi and NSSTA TPAC live adapters run with verified DEMO_CATALOGUE fallback.
                Ready for immediate production API token binding without code changes.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="px-2.5 py-1 rounded bg-[#EBF3ED] text-forest border border-[#C7DEC9] font-mono text-[10px] font-bold">
              iGOT: INTEGRATED
            </span>
            <span className="px-2.5 py-1 rounded bg-[#F7F1E6] text-gold-dark border border-[#E2CEAB] font-mono text-[10px] font-bold">
              NSSTA: INTEGRATED
            </span>
          </div>
        </div>

        {/* MoSPI Statistical Domains Matrix */}
        <div className="space-y-4">
          <div>
            <h2 className="text-xl font-bold text-ink font-serif">
              MoSPI Official Statistics Competencies Matrix
            </h2>
            <p className="text-xs text-[#5C5C5C] mt-0.5">
              Standards calibrated against National Statistical Framework 2026 and United Nations Statistical Division principles.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {statisticalDomains.map((dom) => (
              <div key={dom.code} className="card-institutional p-5 bg-paper shadow-xs flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs mb-2">
                    <span className="font-mono text-[10px] font-bold text-forest bg-[#EBF3ED] px-1.5 py-0.5 rounded border border-[#C7DEC9]">
                      {dom.code}
                    </span>
                    <span className="text-[11px] font-medium text-[#8C8275]">
                      {dom.level}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-ink">{dom.name}</h3>
                  <p className="text-[11px] text-[#5C5C5C] mt-1 leading-normal">{dom.desc}</p>
                </div>
                <div className="mt-4 pt-3 border-t border-[#E6E0D2] flex items-center justify-between text-[11px]">
                  <span className="text-[#8C8275]">Baseline:</span>
                  <span className={`font-semibold ${dom.status.includes("Critical") ? "text-terracotta" : dom.status.includes("High") ? "text-gold-dark" : "text-forest"}`}>
                    {dom.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Technical & Digital Governance Standards */}
        <div className="space-y-4">
          <div>
            <h2 className="text-xl font-bold text-ink font-serif">
              Technical & Digital Governance Standards
            </h2>
            <p className="text-xs text-[#5C5C5C] mt-0.5">
              Statistical computing languages, microdata security, and DPDP Act 2023 compliance.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {technicalDomains.map((tech) => (
              <div key={tech.code} className="card-institutional p-4 bg-paper shadow-xs flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[10px] font-bold text-forest bg-[#EBF3ED] px-1.5 py-0.5 rounded border border-[#C7DEC9]">
                      {tech.code}
                    </span>
                    <span className="text-xs font-bold text-ink">{tech.name}</span>
                  </div>
                  <p className="text-[11px] text-[#5C5C5C] mt-1.5">Standard: {tech.target}</p>
                  <p className="text-[11px] text-[#8C8275] mt-0.5">{tech.focus}</p>
                </div>
                <CheckCircle2 className="w-4 h-4 text-forest shrink-0 mt-0.5" />
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="card-institutional p-8 bg-[#FAF8F5] border border-[#E6E0D2] text-center flex flex-col items-center">
          <h3 className="text-xl font-serif font-bold text-ink">
            Begin Official Capacity Building
          </h3>
          <p className="text-xs text-[#5C5C5C] mt-2 max-w-lg">
            Register your official credentials to establish your baseline competency score and receive instant iGOT recommendations.
          </p>
          <div className="mt-5 flex gap-3">
            <Link
              href="/register"
              className="px-6 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
            >
              Register Official Account
            </Link>
            <Link
              href="/login"
              className="px-6 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors"
            >
              Sign In Existing User
            </Link>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
