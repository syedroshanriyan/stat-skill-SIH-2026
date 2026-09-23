"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Building2, Shield, Bell, HelpCircle } from "lucide-react";
import { getStoredUser, StoredUser } from "@/lib/api";

export default function Header() {
  const pathname = usePathname();
  const [user, setUser] = useState<StoredUser | null>(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const getPageTitle = () => {
    if (pathname.includes("/dashboard")) return "Executive Overview";
    if (pathname.includes("/competencies")) return "Competency Framework & Hierarchy";
    if (pathname.includes("/gaps")) return "Automated Skill-Gap Analysis";
    if (pathname.includes("/recommendations")) return "Personalized Recommendations";
    if (pathname.includes("/learning-paths")) return "Learning Roadmaps & Sequencing";
    if (pathname.includes("/assessments")) return "Diagnostic Assessment Engine";
    if (pathname.includes("/documents")) return "Learning Document Processing & Indexing";
    if (pathname.includes("/quizzes")) return "AI Grounded Quiz Generator";
    if (pathname.includes("/assistant")) return "Institutional Knowledge Assistant (RAG)";
    if (pathname.includes("/evidence")) return "Evidence Portfolio & Verification";
    if (pathname.includes("/government")) return "Government & Official Capacity Building";
    if (pathname.includes("/industry")) return "Industry Competency & Opportunity Analysis";
    if (pathname.includes("/academia")) return "Academic Curriculum & Industry Crosswalk";
    if (pathname.includes("/analytics")) return "Workforce Analytics & Heatmaps";
    if (pathname.includes("/admin")) return "Administrative Oversight & Audit Log";
    return "Competency Intelligence Platform";
  };

  const trackBadge = () => {
    const track = user?.track || "GOVERNMENT";
    if (track === "GOVERNMENT") {
      return {
        label: "MoSPI Official Statistics Track",
        bg: "bg-[#EBF3ED] text-forest border-[#C7DEC9]",
      };
    } else if (track === "INDUSTRY") {
      return {
        label: "Industry & Professional Growth Track",
        bg: "bg-[#F7F1E6] text-gold-dark border-[#E2CEAB]",
      };
    } else {
      return {
        label: "Academic Bridge & Curriculum Track",
        bg: "bg-[#F9ECE7] text-terracotta border-[#E5C1B4]",
      };
    }
  };

  const badge = trackBadge();

  return (
    <header className="h-16 border-b border-[#E6E0D2] bg-paper px-8 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-4">
        <h2 className="text-base font-bold text-ink font-serif tracking-tight">
          {getPageTitle()}
        </h2>
        <span
          className={`text-[11px] px-2.5 py-0.5 rounded border font-medium ${badge.bg}`}
        >
          {badge.label}
        </span>
      </div>

      <div className="flex items-center gap-4">
        {/* Verification provenance badge */}
        <div className="flex items-center gap-1.5 text-xs text-[#5C5C5C] bg-[#F7F3EA] px-2.5 py-1 rounded border border-[#E6E0D2]">
          <Shield className="w-3.5 h-3.5 text-forest" />
          <span>Deterministic Scoring Engine</span>
        </div>

        {/* Quick links */}
        <Link
          href="/assistant"
          className="text-xs text-forest hover:text-forest-dark font-medium underline underline-offset-4"
        >
          AI Assistant
        </Link>
      </div>
    </header>
  );
}
