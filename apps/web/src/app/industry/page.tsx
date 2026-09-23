"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Briefcase,
  Target,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  FileCode2,
  Shield,
  Layers,
  Sparkles,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";
import { getStoredUser, StoredUser } from "@/lib/api";

export default function IndustryPublicPage() {
  const [user, setUser] = useState<StoredUser | null>(null);
  const [selectedRole, setSelectedRole] = useState("Data Analyst / BI Analyst");

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const rolesData: Record<string, any> = {
    "Data Analyst / BI Analyst": {
      description: "Extracts business insights from large data warehouses, designs KPI executive dashboards, writes complex SQL window queries, and surfaces predictive metrics.",
      requiredSkills: [
        { code: "IND-SQL", name: "Advanced SQL & Warehousing", required: 4, current: 3, gap: 20 },
        { code: "IND-BI", name: "Power BI / Tableau Dashboards", required: 4, current: 3, gap: 20 },
        { code: "IND-PY", name: "Python Data Wrangling (Pandas)", required: 3, current: 3, gap: 0 },
        { code: "IND-GIT", name: "Version Control & Git Workflow", required: 3, current: 2, gap: 20 },
      ],
      suggestedProjects: [
        "Executive Sales & Churn Analytics Dashboard in Power BI with DAX time-intelligence calculations",
        "E-Commerce Transaction Data Pipeline using SQL Window Functions and Star Schema",
      ],
    },
    "Machine Learning Engineer": {
      description: "Designs, optimizes, and serves predictive AI/ML models into production APIs using Docker, Python, and cloud infrastructure.",
      requiredSkills: [
        { code: "IND-ML", name: "Applied Machine Learning (Scikit-Learn)", required: 4, current: 2, gap: 40 },
        { code: "IND-PY", name: "Python Data Wrangling", required: 4, current: 3, gap: 20 },
        { code: "IND-API", name: "REST API Development (FastAPI)", required: 3, current: 1, gap: 40 },
        { code: "IND-DOCK", name: "Docker Containerization", required: 3, current: 1, gap: 40 },
      ],
      suggestedProjects: [
        "Predictive Customer Retention Model deployed as a FastAPI Docker microservice",
        "NLP Sentiment & Intent Classifier with ground-truth validation pipeline",
      ],
    },
    "Analytics Engineer": {
      description: "Bridges the gap between data engineering and business analytics by building clean, tested, documented dimensional models in dbt and modern data lakes.",
      requiredSkills: [
        { code: "IND-SQL", name: "Data Warehousing & SQL", required: 5, current: 3, gap: 40 },
        { code: "IND-DBT", name: "Data Transformation (dbt)", required: 4, current: 1, gap: 60 },
        { code: "IND-CI", name: "CI/CD & Automated Testing", required: 3, current: 2, gap: 20 },
        { code: "IND-DOC", name: "Data Cataloging & Governance", required: 3, current: 2, gap: 20 },
      ],
      suggestedProjects: [
        "End-to-End Analytics Warehouse with dbt tests, incremental models, and automated documentation",
        "Microdata Anonymization pipeline satisfying enterprise data protection mandates",
      ],
    },
  };

  const role = rolesData[selectedRole] || rolesData["Data Analyst / BI Analyst"];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-6xl mx-auto px-6 py-12 space-y-10">
        {/* Logged in state banner */}
        {user && user.track === "INDUSTRY" && (
          <div className="p-4 rounded-lg bg-[#F7F1E6] border border-[#E2CEAB] flex items-center justify-between">
            <div className="flex items-center gap-2.5 text-xs text-gold-dark font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>You are logged in as {user.display_name} (Industry Professional)</span>
            </div>
            <Link
              href="/dashboard"
              className="text-xs font-bold text-gold-dark hover:text-ink flex items-center gap-1 underline underline-offset-2"
            >
              <span>Go to Active Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}

        {/* Top Track Banner */}
        <div className="card-institutional p-8 bg-paper border-[#E2CEAB] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-[#F7F1E6] text-gold-dark border border-[#E2CEAB] px-2.5 py-0.5 rounded">
                Industry & Professional Careers
              </span>
              <span className="text-xs text-[#5C5C5C]">
                Corporate Analytics & AI Workforce Development
              </span>
            </div>
            <h1 className="text-3xl font-bold text-ink font-serif mt-2">
              Industry Competency & Career Pathway
            </h1>
            <p className="text-xs text-[#5C5C5C] mt-2 max-w-2xl leading-relaxed">
              Target-role competency extraction, job requirement analysis, practical project sequencing,
              and verifiable portfolio evidence for data analysts, ML engineers, and analytics leaders.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
            <Link
              href="/register"
              className="px-5 py-2.5 rounded bg-gold-dark text-paper text-xs font-semibold hover:bg-gold-light transition-colors flex items-center justify-center gap-2 shadow-sm"
            >
              <Target className="w-4 h-4" />
              <span>Take Industry Diagnostic</span>
            </Link>
            <Link
              href="/login"
              className="px-5 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors text-center"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Industry Pathway Roadmap */}
        <div className="card-institutional p-6 bg-paper border-[#E6E0D2]">
          <p className="text-[10px] uppercase font-bold tracking-widest text-[#8C8275] mb-2">
            The Industry Pathway
          </p>
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-ink">
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Target Role</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F7F1E6] text-gold-dark font-bold border border-[#E2CEAB]">Requirements Extraction</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F9ECE7] text-terracotta font-bold border border-[#E5C1B4]">Skill Gap Comparison</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Applied Learning</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#EBF3ED] text-forest font-bold border border-[#C7DEC9]">Production Projects</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Verifiable Evidence</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-gold-dark text-paper font-bold">Career Growth</span>
          </div>
        </div>

        {/* Role Selector & Competency Breakdown */}
        <div className="card-institutional p-6 bg-paper border-[#E6E0D2] space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E6E0D2] pb-4">
            <div>
              <h2 className="text-xl font-bold text-ink font-serif">
                Select Target Industry Role
              </h2>
              <p className="text-xs text-[#5C5C5C] mt-0.5">
                Examine extracted skill profiles, required proficiency levels, and recommended capstone projects.
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              {Object.keys(rolesData).map((r) => (
                <button
                  key={r}
                  onClick={() => setSelectedRole(r)}
                  className={`px-3 py-1.5 rounded text-xs font-semibold transition-all ${
                    selectedRole === r
                      ? "bg-gold-dark text-paper shadow-xs"
                      : "border border-[#D1C8B4] text-[#5C5C5C] hover:bg-[#F2EDE1]"
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-serif font-bold text-base text-ink">{selectedRole}</h3>
            <p className="text-xs text-[#5C5C5C] mt-1 leading-relaxed max-w-3xl">
              {role.description}
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {role.requiredSkills.map((sk: any) => (
              <div key={sk.code} className="p-4 rounded-lg bg-[#FAF8F5] border border-[#E6E0D2] flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[10px] font-bold text-gold-dark bg-[#F7F1E6] px-1.5 py-0.5 rounded border border-[#E2CEAB]">
                      {sk.code}
                    </span>
                    <span className="text-xs font-bold text-ink">{sk.name}</span>
                  </div>
                  <p className="text-[11px] text-[#5C5C5C] mt-1">Target: Level {sk.required} • Current: Level {sk.current}</p>
                </div>
                {sk.gap > 0 ? (
                  <span className="text-xs font-bold text-terracotta bg-[#F9ECE7] px-2 py-0.5 rounded border border-[#E5C1B4]">
                    Gap: {sk.gap}%
                  </span>
                ) : (
                  <span className="text-xs font-bold text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
                    Met
                  </span>
                )}
              </div>
            ))}
          </div>

          <div className="p-4 rounded-lg bg-[#FAF8F3] border border-[#E6E0D2]">
            <h4 className="text-xs font-bold uppercase tracking-wider text-ink mb-2">
              Recommended Applied Production Projects
            </h4>
            <ul className="space-y-1.5 text-xs text-[#2A2A2A]">
              {role.suggestedProjects.map((p: string, idx: number) => (
                <li key={idx} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-gold-dark shrink-0 mt-0.5" />
                  <span>{p}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* CTA */}
        <div className="card-institutional p-8 bg-[#FAF8F5] border border-[#E6E0D2] text-center flex flex-col items-center">
          <h3 className="text-xl font-serif font-bold text-ink">
            Elevate Your Industry Technical Standing
          </h3>
          <p className="text-xs text-[#5C5C5C] mt-2 max-w-lg">
            Register your profile to evaluate your technical competency across SQL, Python, machine learning, and BI tooling.
          </p>
          <div className="mt-5 flex gap-3">
            <Link
              href="/register"
              className="px-6 py-2.5 rounded bg-gold-dark text-paper text-xs font-semibold hover:bg-gold-light transition-colors"
            >
              Register Industry Account
            </Link>
            <Link
              href="/login"
              className="px-6 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
