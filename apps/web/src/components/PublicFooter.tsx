"use client";

import React from "react";
import Link from "next/link";
import { Shield, Building2, CheckCircle2, Lock, ArrowUpRight } from "lucide-react";

export default function PublicFooter() {
  return (
    <footer className="border-t border-[#E6E0D2] bg-paper pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 text-xs text-[#5C5C5C]">
        {/* Brand & Mandate */}
        <div className="space-y-3">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded bg-forest flex items-center justify-center text-paper font-serif font-bold text-sm">
              S
            </div>
            <span className="font-serif font-bold text-base text-ink tracking-tight">
              STAT-SKILL AI
            </span>
          </div>
          <p className="text-[11px] leading-relaxed text-[#736B5E]">
            AI-Powered Competency Intelligence Platform. National capacity building framework for official statistics, iGOT Karmayogi integration, and cross-sector competency evaluation.
          </p>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#EBF3ED] text-forest border border-[#C7DEC9] text-[10px] font-semibold">
            <Shield className="w-3 h-3" />
            <span>DPDP Act 2023 & MoSPI DQAF Compliant</span>
          </div>
        </div>

        {/* The 3 Core Tracks */}
        <div className="space-y-2">
          <h4 className="font-serif font-bold text-ink text-sm uppercase tracking-wide">
            Track Pathways
          </h4>
          <ul className="space-y-1.5 text-[11px]">
            <li>
              <Link href="/government" className="hover:text-forest transition-colors flex items-center gap-1">
                <span>Government (MoSPI / NSSTA)</span>
                <ArrowUpRight className="w-3 h-3 text-[#A8A29E]" />
              </Link>
            </li>
            <li>
              <Link href="/industry" className="hover:text-gold-dark transition-colors flex items-center gap-1">
                <span>Industry (Data & AI Careers)</span>
                <ArrowUpRight className="w-3 h-3 text-[#A8A29E]" />
              </Link>
            </li>
            <li>
              <Link href="/academia" className="hover:text-terracotta transition-colors flex items-center gap-1">
                <span>Academia (OBE Curriculum Bridge)</span>
                <ArrowUpRight className="w-3 h-3 text-[#A8A29E]" />
              </Link>
            </li>
          </ul>
        </div>

        {/* Platform Architecture */}
        <div className="space-y-2">
          <h4 className="font-serif font-bold text-ink text-sm uppercase tracking-wide">
            Intelligence Engine
          </h4>
          <ul className="space-y-1.5 text-[11px]">
            <li>
              <Link href="/how-it-works" className="hover:text-ink transition-colors">
                The 9-Stage Competency Loop
              </Link>
            </li>
            <li>
              <Link href="/features" className="hover:text-ink transition-colors">
                Deterministic Psychometrics
              </Link>
            </li>
            <li>
              <Link href="/features" className="hover:text-ink transition-colors">
                Multi-Tenant Data Isolation
              </Link>
            </li>
            <li>
              <Link href="/legal-intelligence" className="hover:text-ink transition-colors">
                Legal AI & Statutory RAG
              </Link>
            </li>
            <li>
              <Link href="/faq" className="hover:text-ink transition-colors">
                Grounded Document RAG
              </Link>
            </li>
          </ul>
        </div>

        {/* Access & Verification */}
        <div className="space-y-2">
          <h4 className="font-serif font-bold text-ink text-sm uppercase tracking-wide">
            Official Access
          </h4>
          <ul className="space-y-1.5 text-[11px]">
            <li>
              <Link href="/login" className="hover:text-ink transition-colors">
                Official Sign In
              </Link>
            </li>
            <li>
              <Link href="/register" className="hover:text-ink transition-colors">
                New Officer / Learner Registration
              </Link>
            </li>
            <li>
              <Link href="/faq" className="hover:text-ink transition-colors">
                Frequently Asked Questions
              </Link>
            </li>
            <li>
              <span className="text-[10px] text-[#A8A29E]">
                Sovereign Hosting: NIC MeghRaj / India (in-mumbai-1)
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 pt-6 border-t border-[#E6E0D2] flex flex-col md:flex-row items-center justify-between gap-3 text-[11px] text-[#8C8275]">
        <p>
          © 2026 STAT-SKILL AI. Developed for Ministry of Statistics and Programme Implementation (MoSPI).
        </p>
        <p className="font-mono text-[10px]">
          ZERO_HALLUCINATED_SCORING • IMMUTABLE_DELTA_LEDGER • STRICT_SCOPE_ISOLATION
        </p>
      </div>
    </footer>
  );
}
