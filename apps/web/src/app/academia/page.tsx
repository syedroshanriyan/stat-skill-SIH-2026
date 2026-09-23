"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  GraduationCap,
  BookOpen,
  ArrowRight,
  CheckCircle2,
  Award,
  Layers,
  Sparkles,
  Info,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";
import { getStoredUser, StoredUser } from "@/lib/api";

export default function AcademiaPublicPage() {
  const [user, setUser] = useState<StoredUser | null>(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const courseMappings = [
    {
      course: "CS301: Database Management Systems",
      courseOutcome: "CO3: Formulate complex relational queries and normalize schemas to 3NF/BCNF",
      industryCompetency: "IND-SQL: Advanced SQL & Data Warehousing",
      alignmentPct: 88,
    },
    {
      course: "STAT204: Probability & Mathematical Statistics",
      courseOutcome: "CO2: Perform hypothesis testing, ANOVA, and compute p-values for decision analysis",
      industryCompetency: "STAT-02: Sampling & Statistical Inference",
      alignmentPct: 92,
    },
    {
      course: "CS405: Applied Machine Learning",
      courseOutcome: "CO4: Train and evaluate supervised classifiers with cross-validation in Python",
      industryCompetency: "IND-ML: Production Machine Learning",
      alignmentPct: 84,
    },
    {
      course: "DS202: Data Structures & Algorithms",
      courseOutcome: "CO1: Implement graph traversal and dynamic programming with complexity proofs",
      industryCompetency: "TECH-01: Algorithmic Efficiency & Engineering",
      alignmentPct: 95,
    },
  ];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-6xl mx-auto px-6 py-12 space-y-10">
        {/* Logged in state banner */}
        {user && user.track === "ACADEMIA" && (
          <div className="p-4 rounded-lg bg-[#F9ECE7] border border-[#E5C1B4] flex items-center justify-between">
            <div className="flex items-center gap-2.5 text-xs text-terracotta font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>You are logged in as {user.display_name} (Academic Student / Faculty)</span>
            </div>
            <Link
              href="/dashboard"
              className="text-xs font-bold text-terracotta hover:text-ink flex items-center gap-1 underline underline-offset-2"
            >
              <span>Go to Active Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}

        {/* Top Track Banner */}
        <div className="card-institutional p-8 bg-paper border-[#E5C1B4] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-[#F9ECE7] text-terracotta border border-[#E5C1B4] px-2.5 py-0.5 rounded">
                Higher Education & OBE Curriculum
              </span>
              <span className="text-xs text-[#5C5C5C]">
                National Education Policy (NEP 2020) Bridge
              </span>
            </div>
            <h1 className="text-3xl font-bold text-ink font-serif mt-2">
              Academia & Outcome-Based Education Track
            </h1>
            <p className="text-xs text-[#5C5C5C] mt-2 max-w-2xl leading-relaxed">
              Bridges higher education coursework with practical industry and official statistical standards.
              Directly translates Course Outcomes (COs) into competency benchmarks, provides guided lab simulations,
              and establishes verifiable internship readiness.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
            <Link
              href="/register"
              className="px-5 py-2.5 rounded bg-terracotta text-paper text-xs font-semibold hover:bg-terracotta-light transition-colors flex items-center justify-center gap-2 shadow-sm"
            >
              <GraduationCap className="w-4 h-4" />
              <span>Take Academic Diagnostic</span>
            </Link>
            <Link
              href="/login"
              className="px-5 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors text-center"
            >
              Student / Faculty Sign In
            </Link>
          </div>
        </div>

        {/* Academia Pathway Roadmap */}
        <div className="card-institutional p-6 bg-paper border-[#E6E0D2]">
          <p className="text-[10px] uppercase font-bold tracking-widest text-[#8C8275] mb-2">
            The Academia Pathway
          </p>
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-ink">
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Academic Profile</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F9ECE7] text-terracotta font-bold border border-[#E5C1B4]">Curriculum CO Mapping</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#EBF3ED] text-forest font-bold border border-[#C7DEC9]">Competency Evaluation</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F7F1E6] text-gold-dark font-bold border border-[#E2CEAB]">Industry Gap Crosswalk</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#FAF8F5] border border-[#E6E0D2]">Lab Projects</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-[#F9ECE7] text-terracotta font-bold border border-[#E5C1B4]">Internship Readiness</span>
            <span className="text-[#8C8275]">→</span>
            <span className="px-2.5 py-1 rounded bg-terracotta text-paper font-bold">Career Placement</span>
          </div>
        </div>

        {/* Course Outcome (CO) to Industry Competency Crosswalk */}
        <div className="card-institutional p-6 bg-paper border-[#E6E0D2] space-y-4">
          <div>
            <h2 className="text-xl font-bold text-ink font-serif">
              Course Outcome (CO) to Competency Crosswalk
            </h2>
            <p className="text-xs text-[#5C5C5C] mt-0.5">
              Demonstrating automated cross-mapping between university syllabi and real-world competency requirements.
            </p>
          </div>

          <div className="space-y-3">
            {courseMappings.map((m, idx) => (
              <div key={idx} className="p-4 rounded-lg bg-[#FAF8F5] border border-[#E6E0D2] flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <span className="font-mono text-[10px] font-bold text-terracotta bg-[#F9ECE7] px-2 py-0.5 rounded border border-[#E5C1B4]">
                    {m.course}
                  </span>
                  <p className="text-xs font-bold text-ink mt-1">{m.courseOutcome}</p>
                  <p className="text-[11px] text-[#5C5C5C]">Maps to: <strong className="text-ink">{m.industryCompetency}</strong></p>
                </div>

                <div className="shrink-0 flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-forest bg-[#EBF3ED] px-2.5 py-1 rounded border border-[#C7DEC9]">
                    {m.alignmentPct}% Alignment
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="card-institutional p-8 bg-[#FAF8F5] border border-[#E6E0D2] text-center flex flex-col items-center">
          <h3 className="text-xl font-serif font-bold text-ink">
            Establish Your Academic Competency Portfolio
          </h3>
          <p className="text-xs text-[#5C5C5C] mt-2 max-w-lg">
            Register as a student or faculty member to map coursework, evaluate skills against MoSPI and industry benchmarks, and build a verified evidence portfolio.
          </p>
          <div className="mt-5 flex gap-3">
            <Link
              href="/register"
              className="px-6 py-2.5 rounded bg-terracotta text-paper text-xs font-semibold hover:bg-terracotta-light transition-colors"
            >
              Register Academic Account
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
