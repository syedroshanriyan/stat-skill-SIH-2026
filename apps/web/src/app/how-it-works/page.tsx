"use client";

import React from "react";
import Link from "next/link";
import {
  Shield,
  ArrowRight,
  CheckCircle2,
  Cpu,
  BarChart2,
  FileCheck2,
  Compass,
  Award,
  Layers,
  HelpCircle,
  TrendingUp,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";

export default function HowItWorksPage() {
  const stages = [
    {
      step: "01",
      title: "Onboarding & Institutional Cadre Mapping",
      summary: "Profile & Role Baseline",
      detail:
        "Learners select their sector (Government, Industry, or Academia) and declare target roles (e.g., Statistical Officer, Data Analyst, or Student). Role profiles establish clear benchmark requirements according to official MoSPI or industry competency matrices.",
      icon: Layers,
    },
    {
      step: "02",
      title: "Diagnostic Baseline Assessment",
      summary: "Calibrated Psychometrics",
      detail:
        "A formal diagnostic assessment measures competency baseline across statistical design, sampling, national accounts, pricing, and analytics tooling. Scoring is strictly deterministic—zero LLM grading—calibrated against psychometric answer keys.",
      icon: FileCheck2,
    },
    {
      step: "03",
      title: "Dynamic Competency Spectrum & Radar",
      summary: "Real-Time Skill Profiling",
      detail:
        "The system maps raw scores to defined 5-level proficiency tiers (Novice, Beginner, Competent, Advanced, Expert) and renders the visual Competency Radar Chart, reading directly from database records.",
      icon: BarChart2,
    },
    {
      step: "04",
      title: "Automated Skill-Gap Identification",
      summary: "Delta vs Target Benchmark",
      detail:
        "Each competency is evaluated against the role benchmark level. Shortfalls are prioritized into Critical, High, Medium, or Low gaps, accompanied by institutional explanations.",
      icon: TrendingUp,
    },
    {
      step: "05",
      title: "Targeted Capacity Building Roadmap",
      summary: "Sequenced Learning Paths",
      detail:
        "The engine synthesizes an active learning path with sequential milestones, balancing foundational theory, practical statistical tooling, and policy governance.",
      icon: Compass,
    },
    {
      step: "06",
      title: "Grounded Remediation via iGOT & NSSTA",
      summary: "Official Course Integration",
      detail:
        "Curated modules from iGOT Karmayogi and the National Statistical Systems Training Academy (NSSTA) are mapped directly to open skill gaps, guaranteeing that public officials and students receive authoritative training.",
      icon: Cpu,
    },
    {
      step: "07",
      title: "AI Grounded Quizzes & Competency Updates",
      summary: "Document-Grounded Evaluation",
      detail:
        "Learners take psychometric quizzes generated strictly from uploaded guidelines and manuals. Quizzes configured as competency assessments calculate score gains and update competencies deterministically.",
      icon: HelpCircle,
    },
    {
      step: "08",
      title: "Immutable Competency History Ledger",
      summary: "Persistent Delta Ledger",
      detail:
        "Every assessment event persists score_before, score_after, delta, confidence_before, confidence_after, and attempt ID. The competency radar and dashboard update live without manual browser refresh.",
      icon: Shield,
    },
    {
      step: "09",
      title: "Verifiable Evidence & Institutional Oversight",
      summary: "Workforce Intelligence",
      detail:
        "Officers submit project deliverables, code repositories, or survey fieldwork evidence. Department administrators access aggregate competency heatmaps and training demand forecasts with strict tenant isolation.",
      icon: Award,
    },
  ];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full bg-[#EBF3ED] text-forest border border-[#C7DEC9] mb-4">
            <Shield className="w-3.5 h-3.5" />
            <span>Platform Architecture & Competency Lifecycle Walkthrough</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-serif font-bold text-ink tracking-tight">
            How STAT-SKILL AI Operates
          </h1>
          <p className="mt-3 text-base text-[#5C5C5C] leading-relaxed">
            The closed-loop competency intelligence engine continuously transitions learners from diagnostic evaluation
            to grounded capacity building, verifiable evidence, and measurable career advancement.
          </p>
        </div>

        {/* 9 Stages List */}
        <div className="mt-12 space-y-6">
          {stages.map((stage) => {
            const Icon = stage.icon;
            return (
              <div
                key={stage.step}
                className="card-institutional p-6 bg-paper border-[#E6E0D2] shadow-xs flex flex-col md:flex-row items-start gap-6 hover:border-forest/50 transition-all"
              >
                <div className="flex items-center gap-4 shrink-0 md:w-48">
                  <div className="w-12 h-12 rounded-lg bg-[#EBF3ED] text-forest flex items-center justify-center font-serif font-bold text-lg border border-[#C7DEC9]">
                    {stage.step}
                  </div>
                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-[#8C8275] font-bold">
                      Stage {stage.step}
                    </span>
                    <p className="text-xs font-bold text-forest">{stage.summary}</p>
                  </div>
                </div>

                <div className="flex-1">
                  <h3 className="text-base font-serif font-bold text-ink flex items-center gap-2">
                    <Icon className="w-4 h-4 text-forest" />
                    <span>{stage.title}</span>
                  </h3>
                  <p className="text-xs text-[#5C5C5C] mt-2 leading-relaxed">
                    {stage.detail}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* CTA Banner */}
        <div 
          style={{ backgroundColor: "#143326" }}
          className="mt-14 rounded-2xl p-10 sm:p-12 text-white border border-[#235841] shadow-xl text-center flex flex-col items-center relative overflow-hidden"
        >
          {/* Subtle gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-tr from-[#0F291E] via-[#143326] to-[#1E4D38] opacity-90 pointer-events-none" />

          <div className="relative z-10 max-w-2xl mx-auto flex flex-col items-center">
            <span className="inline-block text-xs uppercase font-extrabold tracking-widest text-[#7CE4B5] font-mono px-3.5 py-1 rounded-full bg-[#1B4332] border border-[#2D6A4F] mb-3">
              Closed-Loop Engine
            </span>
            <h3 className="text-2xl sm:text-3xl font-serif font-bold text-white leading-tight">
              Experience the Closed-Loop Competency Engine
            </h3>
            <p className="mt-3 text-sm text-[#E5F4ED] max-w-xl leading-relaxed">
              Register your official profile and take the calibrated baseline diagnostic assessment to evaluate your skills.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-4">
              <Link
                href="/register"
                className="px-7 py-3 rounded-lg bg-white text-[#143326] text-xs font-bold hover:bg-[#F2EDE1] transition-all flex items-center gap-2 shadow-md hover:shadow-lg hover:-translate-y-0.5"
              >
                <span>Get Started Now</span>
                <ArrowRight className="w-4 h-4 text-[#143326]" />
              </Link>
              <Link
                href="/government"
                className="px-7 py-3 rounded-lg border-2 border-white/60 text-white text-xs font-semibold hover:bg-white/10 transition-colors"
              >
                <span>Learn About Government Track</span>
              </Link>
            </div>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
