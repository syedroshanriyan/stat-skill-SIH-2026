"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Building2,
  Briefcase,
  GraduationCap,
  Shield,
  ArrowRight,
  CheckCircle2,
  Cpu,
  BarChart2,
  FileCheck2,
  Sparkles,
  Layers,
  Database,
  Lock,
  Compass,
  Zap,
  TrendingUp,
  Award,
  ChevronRight,
  Key,
  Globe2,
  Activity,
  Check,
  Scale,
  Users,
  BookOpen,
  FileText
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";

export default function HomePage() {
  const router = useRouter();

  // 4 steps of How it Works
  const howItWorksSteps = [
    {
      num: "01",
      title: "Get Started & Select Your Sector",
      desc: "Register your profile or choose from Government (MoSPI/ISS), Industry (Data Analytics), or Academia (Higher Education).",
      icon: Users,
      badge: "Onboarding"
    },
    {
      num: "02",
      title: "Take Adaptive Diagnostic",
      desc: "Complete scientifically calibrated baseline assessments across core statistical methodologies and frameworks.",
      icon: Activity,
      badge: "Diagnostic"
    },
    {
      num: "03",
      title: "Inspect Gap Radar & Shortfalls",
      desc: "Our automated gap engine computes mathematical shortfall deltas against national cadre standards in real-time.",
      icon: BarChart2,
      badge: "Gap Math"
    },
    {
      num: "04",
      title: "Upskill via iGOT & NSSTA Modules",
      desc: "Follow personalized learning paths with grounded national courses, document-generated quizzes, and verifiable credential passports.",
      icon: Award,
      badge: "Certification"
    }
  ];

  // 4 Core Platform Pillars
  const platformPillars = [
    {
      icon: Cpu,
      title: "Scientifically Calibrated Diagnostics",
      desc: "Psychometrically validated assessments mapping your strengths across official survey design, national accounts, and sampling theory.",
      metrics: "5-Stage Calibration"
    },
    {
      icon: TrendingUp,
      title: "Automated Skill Gap Detection",
      desc: "Instant mathematical shortfall calculation comparing individual proficiencies against ministry cadre benchmarks with zero guesswork.",
      metrics: "Precise Delta Math"
    },
    {
      icon: BookOpen,
      title: "Grounded iGOT & NSSTA Pathways",
      desc: "Direct integration with national learning repositories. Courses are matched strictly to detected shortfalls with zero hallucination.",
      metrics: "100% Grounded"
    },
    {
      icon: FileCheck2,
      title: "AI Document Quizzes & Evidence Vault",
      desc: "Upload statistical circulars or manuals to generate grounded quizzes, and store verifiable proof of competency growth in an immutable ledger.",
      metrics: "Verifiable Badges"
    }
  ];

  return (
    <div className="min-h-screen bg-ambient-luxury text-ink flex flex-col font-sans selection:bg-[#EBF3ED] selection:text-forest">
      <PublicNav />

      {/* HERO SECTION */}
      <main className="flex-1 max-w-7xl mx-auto px-6 pt-14 pb-20 flex flex-col items-center text-center">
        {/* Institutional Authority Pill */}
        <div className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-1.5 rounded-full bg-paper/90 border border-[#C7DEC9] text-forest mb-8 shadow-xs backdrop-blur-sm">
          <Shield className="w-4 h-4 text-forest" />
          <span className="tracking-wide">National Statistical Capacity Building Architecture &bull; MoSPI Standards</span>
          <span className="inline-block w-1.5 h-1.5 rounded-full bg-forest animate-pulse ml-1" />
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-serif font-bold text-ink max-w-5xl leading-[1.12] tracking-tight">
          AI-Powered Competency <br className="hidden sm:inline" />
          <span className="text-forest italic font-normal">Intelligence Platform</span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-[#555555] max-w-3xl leading-relaxed font-normal">
          A unified capacity intelligence platform designed for Government officers, Industry analysts, and Academic scholars. Experience standardized psychometric assessments, automated skill-gap analysis, grounded iGOT Karmayogi / NSSTA learning paths, and verifiable credential passports.
        </p>

        {/* Primary Action Buttons */}
        <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/register"
            className="px-8 py-4 rounded-lg bg-forest text-paper text-sm font-semibold hover:bg-forest-light transition-all flex items-center gap-2.5 shadow-sm hover:shadow-md hover:-translate-y-0.5"
          >
            <span>Get Started</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/login"
            className="px-8 py-4 rounded-lg border border-[#D1C8B4] bg-paper/90 backdrop-blur-sm text-ink text-sm font-semibold hover:bg-[#F5EFE4] hover:border-forest/40 transition-all flex items-center gap-2 shadow-xs"
          >
            <span>Sign In</span>
            <ArrowRight className="w-4 h-4 text-[#666666]" />
          </Link>
          <Link
            href="/legal-intelligence"
            className="px-6 py-4 rounded-lg border border-[#D1C8B4] bg-paper/80 backdrop-blur-sm text-[#444444] text-sm font-medium hover:text-ink hover:bg-[#F5EFE4] transition-all flex items-center gap-1.5"
          >
            <Scale className="w-4 h-4 text-warm-gold" />
            <span>Statutory Legal AI</span>
          </Link>
        </div>

        {/* Trust Badges Strip */}
        <div className="mt-12 grid grid-cols-2 sm:grid-cols-4 gap-4 w-full max-w-4xl text-left">
          <div className="p-3.5 rounded-lg bg-paper/70 border border-[#E8E2D5] flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-forest shrink-0" />
            <div>
              <p className="text-xs font-bold text-ink">3 Unified Tracks</p>
              <p className="text-[10px] text-[#666666]">Gov, Industry, Academia</p>
            </div>
          </div>
          <div className="p-3.5 rounded-lg bg-paper/70 border border-[#E8E2D5] flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-forest shrink-0" />
            <div>
              <p className="text-xs font-bold text-ink">Zero Hallucination</p>
              <p className="text-[10px] text-[#666666]">Deterministic Gap Math</p>
            </div>
          </div>
          <div className="p-3.5 rounded-lg bg-paper/70 border border-[#E8E2D5] flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-forest shrink-0" />
            <div>
              <p className="text-xs font-bold text-ink">iGOT & NSSTA</p>
              <p className="text-[10px] text-[#666666]">Grounded Course Repos</p>
            </div>
          </div>
          <div className="p-3.5 rounded-lg bg-paper/70 border border-[#E8E2D5] flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-forest shrink-0" />
            <div>
              <p className="text-xs font-bold text-ink">DPDP Act 2023</p>
              <p className="text-[10px] text-[#666666]">Data Privacy Compliant</p>
            </div>
          </div>
        </div>

        {/* SECTION 1: WHAT IS STAT-SKILL AI */}
        <section className="mt-20 w-full text-left">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-[11px] font-bold uppercase tracking-widest text-forest font-mono">
              About The Platform
            </span>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-ink mt-2">
              Everything You Need to Know About STAT-SKILL AI
            </h2>
            <p className="text-xs sm:text-sm text-[#5C5C5C] mt-2">
              An institutional solution addressing the critical need for continuous statistical competency development across national ministries, modern data teams, and academia.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {platformPillars.map((pillar, idx) => {
              const Icon = pillar.icon;
              return (
                <div key={idx} className="card-institutional p-6 bg-paper border-[#E2DBD0] flex flex-col justify-between">
                  <div>
                    <div className="w-10 h-10 rounded-lg bg-[#EBF3ED] text-forest flex items-center justify-center mb-4">
                      <Icon className="w-5 h-5" />
                    </div>
                    <h3 className="font-serif font-bold text-base text-ink">{pillar.title}</h3>
                    <p className="text-xs text-[#555555] mt-2 leading-relaxed">
                      {pillar.desc}
                    </p>
                  </div>
                  <div className="mt-5 pt-3 border-t border-[#F2EDE1] flex items-center justify-between text-[11px] font-mono text-forest font-semibold">
                    <span>{pillar.metrics}</span>
                    <Check className="w-3.5 h-3.5" />
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* SECTION 2: HOW IT WORKS */}
        <section className="mt-20 w-full text-left">
          <div className="card-institutional p-8 sm:p-10 bg-paper border-[#E2DBD0] shadow-sm">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[#F2EDE1] pb-6 mb-8">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-widest text-forest font-mono">
                  Simple 4-Step Process
                </span>
                <h2 className="text-2xl font-serif font-bold text-ink mt-1">
                  How STAT-SKILL AI Works
                </h2>
                <p className="text-xs text-[#5C5C5C] mt-1">
                  From initial registration to verifiable capacity growth in minutes.
                </p>
              </div>
              <Link
                href="/register"
                className="px-5 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-all flex items-center gap-1.5 shrink-0"
              >
                <span>Get Started Now</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {howItWorksSteps.map((step, idx) => {
                const Icon = step.icon;
                return (
                  <div key={idx} className="p-5 rounded-lg border border-[#E6E0D2] bg-[#FAF8F5] flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="font-mono text-xl font-bold text-forest">{step.num}</span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-paper border border-[#D5CCA8] text-[#5C5C5C]">
                          {step.badge}
                        </span>
                      </div>
                      <h3 className="font-serif font-bold text-sm text-ink">{step.title}</h3>
                      <p className="text-xs text-[#555555] mt-2 leading-relaxed">
                        {step.desc}
                      </p>
                    </div>
                    <div className="mt-4 pt-3 border-t border-[#E8E2D5] flex items-center text-forest text-xs font-semibold gap-1">
                      <Icon className="w-4 h-4" />
                      <span className="text-[11px]">Integrated Engine</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* SECTION 3: THE THREE TRACKS */}
        <section className="mt-20 w-full text-left">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-[11px] font-bold uppercase tracking-widest text-forest font-mono">
              Tailored Architecture
            </span>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-ink mt-2">
              Built for Three Specialized Sectors
            </h2>
            <p className="text-xs sm:text-sm text-[#5C5C5C] mt-2">
              One shared AI engine powering distinct frameworks, workflows, and taxonomies for Government, Industry, and Academia.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Government Track */}
            <div className="card-institutional p-7 flex flex-col justify-between border-forest/30 hover:border-forest shadow-sm bg-paper">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="p-2.5 rounded-lg bg-[#EBF3ED] text-forest">
                    <Building2 className="w-5 h-5" />
                  </span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-forest text-paper font-mono">
                    Public Sector
                  </span>
                </div>
                <h3 className="font-serif font-bold text-xl text-ink">Government & Official Statistics</h3>
                <p className="text-xs text-[#555555] mt-2.5 leading-relaxed">
                  Flagship MoSPI implementation. Covers national survey design, sampling, CPI/WPI index compilation, iGOT Karmayogi integration, and NSSTA training modules.
                </p>

                <div className="mt-5 p-3 rounded bg-[#FAF8F5] border border-[#E6E0D2] text-[11px] text-[#2A2A2A] font-mono">
                  <strong className="text-forest">Pathway:</strong> Profile &rarr; Diagnostic &rarr; Skill Gap &rarr; iGOT/NSSTA &rarr; Growth
                </div>

                <ul className="mt-4 space-y-2 text-xs text-[#333333]">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-forest shrink-0" />
                    <span>MoSPI Standards (STAT-01 to STAT-06)</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-forest shrink-0" />
                    <span>Live iGOT & NSSTA Catalog Adapters</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-forest shrink-0" />
                    <span>Departmental Analytics Heatmaps</span>
                  </li>
                </ul>
              </div>

              <div className="mt-7 pt-5 border-t border-[#F2EDE1]">
                <Link
                  href="/government"
                  className="w-full py-2.5 px-4 rounded-lg bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-all flex items-center justify-center gap-2 shadow-xs"
                >
                  <span>Explore Government Pathway</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>

            {/* Industry Track */}
            <div className="card-institutional p-7 flex flex-col justify-between border-gold/30 hover:border-gold-dark shadow-sm bg-paper">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="p-2.5 rounded-lg bg-[#FAF6EE] text-gold-dark">
                    <Briefcase className="w-5 h-5" />
                  </span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-[#B38A3E] text-paper font-mono">
                    Professional Sector
                  </span>
                </div>
                <h3 className="font-serif font-bold text-xl text-ink">Industry & Enterprise Careers</h3>
                <p className="text-xs text-[#555555] mt-2.5 leading-relaxed">
                  Target-role competency extraction, job requirement analysis, practical project roadmaps, and verifiable portfolios for data analysts and data engineers.
                </p>

                <div className="mt-5 p-3 rounded bg-[#FAF8F5] border border-[#E6E0D2] text-[11px] text-[#2A2A2A] font-mono">
                  <strong className="text-gold-dark">Pathway:</strong> Target Role &rarr; Requirements &rarr; Skill Gap &rarr; Projects &rarr; Growth
                </div>

                <ul className="mt-4 space-y-2 text-xs text-[#333333]">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-gold-dark shrink-0" />
                    <span>Role Profiles: BI Analyst, ML Engineer</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-gold-dark shrink-0" />
                    <span>Practical Production Project Roadmaps</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-gold-dark shrink-0" />
                    <span>Cross-Role Gap Benchmark Analysis</span>
                  </li>
                </ul>
              </div>

              <div className="mt-7 pt-5 border-t border-[#F2EDE1]">
                <Link
                  href="/industry"
                  className="w-full py-2.5 px-4 rounded-lg bg-[#B38A3E] text-paper text-xs font-semibold hover:bg-[#8F6E32] transition-all flex items-center justify-center gap-2 shadow-xs"
                >
                  <span>Explore Industry Pathway</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>

            {/* Academia Track */}
            <div className="card-institutional p-7 flex flex-col justify-between border-terracotta/30 hover:border-terracotta shadow-sm bg-paper">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="p-2.5 rounded-lg bg-[#FAF3F0] text-terracotta">
                    <GraduationCap className="w-5 h-5" />
                  </span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-terracotta text-paper font-mono">
                    Higher Education
                  </span>
                </div>
                <h3 className="font-serif font-bold text-xl text-ink">Academia & Curriculum Bridge</h3>
                <p className="text-xs text-[#555555] mt-2.5 leading-relaxed">
                  NEP 2020 and Outcome-Based Education alignment. Maps Course Outcomes (COs) to industry competencies, guides students through simulations, and scores internship readiness.
                </p>

                <div className="mt-5 p-3 rounded bg-[#FAF8F5] border border-[#E6E0D2] text-[11px] text-[#2A2A2A] font-mono">
                  <strong className="text-terracotta">Pathway:</strong> Academic Profile &rarr; Curriculum &rarr; Competency &rarr; Internship
                </div>

                <ul className="mt-4 space-y-2 text-xs text-[#333333]">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-terracotta shrink-0" />
                    <span>Course Outcome (CO) Crosswalk Mapping</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-terracotta shrink-0" />
                    <span>Simulation & Statistical Notebook Labs</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-terracotta shrink-0" />
                    <span>Internship Readiness Scoring</span>
                  </li>
                </ul>
              </div>

              <div className="mt-7 pt-5 border-t border-[#F2EDE1]">
                <Link
                  href="/academia"
                  className="w-full py-2.5 px-4 rounded-lg bg-terracotta text-paper text-xs font-semibold hover:bg-[#8A4934] transition-all flex items-center justify-center gap-2 shadow-xs"
                >
                  <span>Explore Academic Pathway</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 4: LIVE PLATFORM TELEMETRY PREVIEW */}
        <section className="mt-20 w-full text-left">
          <div className="card-institutional p-8 bg-paper border-[#E2DBD0] shadow-md relative overflow-hidden">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-[#F2EDE1] pb-5">
              <div>
                <span className="text-[10px] uppercase font-bold tracking-widest text-forest font-mono">
                  Live Platform Telemetry Preview
                </span>
                <h3 className="text-xl font-bold font-serif text-ink mt-1">
                  What You Experience Inside the Dashboard
                </h3>
                <p className="text-xs text-[#5C5C5C] mt-1">
                  Persisted baseline evaluations from verified MoSPI survey design standards.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#EBF3ED] text-forest border border-[#C7DEC9]">
                  <span className="w-2 h-2 rounded-full bg-forest" />
                  Live Database Connection
                </span>
                <span className="px-2.5 py-1 rounded text-xs font-mono bg-[#FAF7F0] border border-[#E6E0D2] text-[#5C5C5C]">
                  ISS Cadre 2026.1
                </span>
              </div>
            </div>

            {/* Interactive Preview Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
              {/* Radar Metric Card */}
              <div className="p-5 rounded-lg border border-[#E6E0D2] bg-[#FAF8F5] flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#8C8275] uppercase tracking-wider mb-2">
                    <span>Overall Proficiency</span>
                    <BarChart2 className="w-4 h-4 text-forest" />
                  </div>
                  <div className="flex items-baseline gap-3">
                    <span className="text-3xl font-serif font-bold text-ink">58.8%</span>
                    <span className="text-xs font-medium text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
                      Competent (Level 3)
                    </span>
                  </div>
                  <p className="text-xs text-[#5C5C5C] mt-2">
                    12 Tracked Official Competencies aggregated from baseline diagnostics.
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-[#E6E0D2] space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-[#555555]">Sampling Theory</span>
                    <span className="font-mono font-semibold text-ink">65%</span>
                  </div>
                  <div className="w-full bg-[#E8E2D5] h-1.5 rounded-full overflow-hidden">
                    <div className="bg-forest h-1.5 rounded-full" style={{ width: "65%" }} />
                  </div>

                  <div className="flex justify-between text-xs pt-1">
                    <span className="text-[#555555]">Survey Design (NSS)</span>
                    <span className="font-mono font-semibold text-ink">55%</span>
                  </div>
                  <div className="w-full bg-[#E8E2D5] h-1.5 rounded-full overflow-hidden">
                    <div className="bg-forest h-1.5 rounded-full" style={{ width: "55%" }} />
                  </div>

                  <div className="flex justify-between text-xs pt-1">
                    <span className="text-[#555555]">Data Governance (NDSAP)</span>
                    <span className="font-mono font-semibold text-ink">70%</span>
                  </div>
                  <div className="w-full bg-[#E8E2D5] h-1.5 rounded-full overflow-hidden">
                    <div className="bg-forest h-1.5 rounded-full" style={{ width: "70%" }} />
                  </div>
                </div>
              </div>

              {/* Gaps Preview */}
              <div className="p-5 rounded-lg border border-[#E6E0D2] bg-[#FAF8F5] flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#8C8275] uppercase tracking-wider mb-2">
                    <span>Critical Skill Shortfalls</span>
                    <TrendingUp className="w-4 h-4 text-terracotta" />
                  </div>
                  <div className="flex items-baseline gap-3">
                    <span className="text-3xl font-serif font-bold text-terracotta">-25 pts</span>
                    <span className="text-xs font-medium text-terracotta bg-[#FAF3F0] px-2 py-0.5 rounded border border-[#E5C1B4]">
                      Action Required
                    </span>
                  </div>
                  <p className="text-xs text-[#5C5C5C] mt-2">
                    Identified gaps between current proficiency and MoSPI Statistical Officer role benchmark.
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-[#E6E0D2] space-y-2.5">
                  <div className="p-2.5 rounded bg-paper border border-[#E6E0D2] flex items-center justify-between text-xs">
                    <div>
                      <p className="font-semibold text-ink">Complex Stratified Sampling</p>
                      <p className="text-[10px] text-[#5C5C5C]">Current: 55% | Target: 80%</p>
                    </div>
                    <span className="text-xs font-mono font-bold text-terracotta">-25 pts</span>
                  </div>
                  <div className="p-2.5 rounded bg-paper border border-[#E6E0D2] flex items-center justify-between text-xs">
                    <div>
                      <p className="font-semibold text-ink">CPI Base Revision Math</p>
                      <p className="text-[10px] text-[#5C5C5C]">Current: 60% | Target: 75%</p>
                    </div>
                    <span className="text-xs font-mono font-bold text-terracotta">-15 pts</span>
                  </div>
                </div>
              </div>

              {/* Recommended Courses Preview */}
              <div className="p-5 rounded-lg border border-[#E6E0D2] bg-[#FAF8F5] flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#8C8275] uppercase tracking-wider mb-2">
                    <span>Grounded iGOT / NSSTA Matches</span>
                    <Award className="w-4 h-4 text-gold-dark" />
                  </div>
                  <div className="flex items-baseline gap-3">
                    <span className="text-3xl font-serif font-bold text-gold-dark">2 Modules</span>
                    <span className="text-xs font-medium text-gold-dark bg-[#FAF6EE] px-2 py-0.5 rounded border border-[#E2CEAB]">
                      Matched to Gaps
                    </span>
                  </div>
                  <p className="text-xs text-[#5C5C5C] mt-2">
                    Live courses cataloged to close identified stratified sampling and survey gaps.
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-[#E6E0D2] space-y-2.5">
                  <div className="p-2.5 rounded bg-paper border border-[#E6E0D2] text-xs">
                    <div className="flex items-center justify-between">
                      <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-forest text-paper font-bold">
                        NSSTA
                      </span>
                      <span className="text-[10px] text-[#5C5C5C]">24 Hours</span>
                    </div>
                    <p className="font-semibold text-ink mt-1">Advanced Survey Sampling & Estimation</p>
                  </div>
                  <div className="p-2.5 rounded bg-paper border border-[#E6E0D2] text-xs">
                    <div className="flex items-center justify-between">
                      <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-[#B38A3E] text-paper font-bold">
                        iGOT Karmayogi
                      </span>
                      <span className="text-[10px] text-[#5C5C5C]">8 Hours</span>
                    </div>
                    <p className="font-semibold text-ink mt-1">Official Statistics & Data Governance Framework</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-5 border-t border-[#F2EDE1] flex flex-col sm:flex-row items-center justify-between gap-4">
              <span className="text-xs text-[#5C5C5C]">
                Ready to generate your personal competency radar and view your gaps?
              </span>
              <Link
                href="/register"
                className="px-6 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-all flex items-center gap-1.5"
              >
                <span>Get Started Now</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </section>

        {/* BEGIN YOUR JOURNEY - HIGH CONTRAST FINAL CALL TO ACTION */}
        <section className="mt-20 w-full text-center">
          <div 
            style={{ backgroundColor: "#143326" }}
            className="rounded-2xl p-10 sm:p-14 text-white border border-[#235841] shadow-2xl relative overflow-hidden"
          >
            {/* Subtle background ambient overlay */}
            <div className="absolute inset-0 bg-gradient-to-tr from-[#0F291E] via-[#143326] to-[#1E4D38] opacity-90 pointer-events-none" />
            
            <div className="relative z-10 max-w-3xl mx-auto space-y-4">
              <span className="inline-block text-xs uppercase font-extrabold tracking-widest text-[#7CE4B5] font-mono px-3.5 py-1 rounded-full bg-[#1B4332] border border-[#2D6A4F]">
                Begin Your Journey
              </span>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-white leading-tight">
                Ready to Advance Your Statistical Competency?
              </h2>
              <p className="text-sm sm:text-base text-[#E5F4ED] max-w-2xl mx-auto leading-relaxed">
                Take your free diagnostic assessment, view your mathematical shortfall gap radar, and connect to grounded iGOT & NSSTA learning paths today.
              </p>

              <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
                <Link
                  href="/register"
                  className="px-8 py-4 rounded-lg bg-white text-[#143326] hover:bg-[#F2EDE1] text-sm font-bold transition-all flex items-center gap-2 shadow-lg hover:shadow-xl hover:-translate-y-0.5"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-4 h-4 text-[#143326]" />
                </Link>
                <Link
                  href="/login"
                  className="px-8 py-4 rounded-lg border-2 border-white/60 text-white hover:bg-white/10 text-sm font-semibold transition-all flex items-center gap-2"
                >
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4 text-white" />
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <PublicFooter />
    </div>
  );
}
