"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Shield, ChevronDown, ChevronUp, ArrowRight, HelpCircle } from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";

export default function FAQPage() {
  const [openIdx, setOpenIdx] = useState<number | null>(0);

  const faqs = [
    {
      q: "How does STAT-SKILL AI address official statistical capacity building?",
      a: "The platform delivers an AI-powered competency intelligence platform for institutional statistical capacity building. It establishes a deterministic competency baseline across official statistical domains (survey design, multi-stage sampling, national accounts, CPI/WPI index compilation, SDGs, and data quality), automatically detects individual and departmental skill gaps, and integrates verified course recommendations from iGOT Karmayogi and NSSTA TPAC.",
    },
    {
      q: "How is strict role and data isolation enforced between Government, Industry, and Academia?",
      a: "Data isolation is enforced server-side within the API and database queries, not simply hidden in the frontend UI. Each protected endpoint validates the caller's JWT token, track code, and organization ID. Academic users cannot query Government microdata or Industry proprietary models; Industry users cannot query Government official records; and organization admins are strictly limited to their own affiliated users. Only the Platform Admin can access global platform analytics.",
    },
    {
      q: "Why does the platform prohibit LLM-based scoring?",
      a: "Large Language Models suffer from non-deterministic variance and hallucinations, which is unacceptable for civil service capacity benchmarking and official accreditation. In STAT-SKILL AI, all assessment answers are evaluated against validated psychometric answer keys using deterministic backend algorithms. The LLM is strictly confined to generating question prompts from verified source texts and synthesizing grounded explanations with exact citations.",
    },
    {
      q: "How was the competency radar issue resolved at the data layer?",
      a: "Previously, completing a quiz did not alter the radar because the database records remained static. We introduced the immutable `CompetencyHistory` ledger. When a quiz configured as a competency assessment is completed, the system calculates score gains, updates the `UserCompetency` table, appends a snapshot with score_before, score_after, delta, confidence, and attempt ID, recalculates skill gaps, and triggers immediate React query invalidation so the radar updates live.",
    },
    {
      q: "What is the difference between competency assessments and informational quizzes?",
      a: "Only quizzes explicitly configured as competency assessments (`is_competency_assessment = True`) alter a learner's competency scores and skill gaps. Informational quizzes test comprehension or review materials without silently modifying competency ratings or generating false progress deltas.",
    },
    {
      q: "What happens when a new user registers?",
      a: "When a new learner registers, their profile is initialized without artificial mock numbers. The dashboard displays the New-User Onboarding Roadmap clearly highlighting Stage 1: Diagnostic Baseline Assessment, with a direct call-to-action to establish their verified competency profile.",
    },
    {
      q: "How does the iGOT Karmayogi and NSSTA TPAC integration function?",
      a: "Our backend includes dedicated integration adapters for iGOT Karmayogi and the National Statistical Systems Training Academy (NSSTA). When skill gaps are identified, the recommendation engine maps specific course IDs (e.g., Advanced Multi-Stage Sampling, SDG National Indicator Framework) directly to those gaps, providing direct course enrollment links.",
    },
    {
      q: "Is the platform compliant with India's Digital Personal Data Protection (DPDP) Act 2023?",
      a: "Yes. All microdata ingestion and evidence storage follow strict Statistical Disclosure Limitation (SDL) protocols, sensitive PII is deterministically masked, audit logs are sanitized to exclude tokens and passwords, and data retention is governed under a 7-year audit preservation policy with right-to-erasure support.",
    },
  ];

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-4xl mx-auto px-6 py-12 space-y-10">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full bg-[#EBF3ED] text-forest border border-[#C7DEC9] mb-4">
            <HelpCircle className="w-3.5 h-3.5 text-forest" />
            <span>Frequently Asked Questions</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-serif font-bold text-ink tracking-tight">
            Architectural & Governance FAQ
          </h1>
          <p className="mt-3 text-base text-[#5C5C5C] leading-relaxed">
            Essential information regarding scoring integrity, multi-track isolation, MoSPI compliance, and system implementation.
          </p>
        </div>

        {/* Accordion */}
        <div className="space-y-3">
          {faqs.map((f, idx) => {
            const isOpen = openIdx === idx;
            return (
              <div
                key={idx}
                className="card-institutional border-[#E6E0D2] bg-paper shadow-xs overflow-hidden transition-all"
              >
                <button
                  onClick={() => setOpenIdx(isOpen ? null : idx)}
                  className="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-[#FAF8F5] transition-colors"
                >
                  <span className="font-serif font-bold text-sm text-ink">{f.q}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-forest shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-[#8C8275] shrink-0" />
                  )}
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 pt-1 text-xs text-[#5C5C5C] leading-relaxed border-t border-[#F2EDE1]">
                    {f.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* CTA */}
        <div className="card-institutional p-8 bg-[#FAF8F5] border border-[#E6E0D2] text-center flex flex-col items-center">
          <h3 className="text-xl font-serif font-bold text-ink">
            Still Have Questions?
          </h3>
          <p className="text-xs text-[#5C5C5C] mt-2 max-w-lg">
            Review our detailed technical specifications or sign in to experience the live platform.
          </p>
          <div className="mt-5 flex gap-3">
            <Link
              href="/register"
              className="px-6 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
            >
              Get Started Free
            </Link>
            <Link
              href="/how-it-works"
              className="px-6 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors"
            >
              Review 9-Stage Loop
            </Link>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
