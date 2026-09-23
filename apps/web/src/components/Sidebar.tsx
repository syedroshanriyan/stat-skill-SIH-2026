"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  Target,
  AlertTriangle,
  Compass,
  Map,
  FileCheck2,
  FileText,
  HelpCircle,
  MessageSquare,
  Award,
  BarChart3,
  ShieldCheck,
  Building2,
  GraduationCap,
  Briefcase,
  LogOut,
  ChevronRight,
} from "lucide-react";
import { getStoredUser, clearAuthSession, StoredUser } from "@/lib/api";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<StoredUser | null>(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const handleLogout = () => {
    clearAuthSession();
    router.push("/login");
  };

  const handleSwitchTrack = (newTrack: "GOVERNMENT" | "INDUSTRY" | "ACADEMIA") => {
    if (!user) return;
    const updated = { ...user, track: newTrack };
    localStorage.setItem("statskill_user", JSON.stringify(updated));
    setUser(updated);
    if (newTrack === "GOVERNMENT") router.push("/government");
    else if (newTrack === "INDUSTRY") router.push("/industry");
    else router.push("/academia");
  };

  const currentTrack = user?.track || "GOVERNMENT";

  const navGroups = [
    {
      title: "Core Intelligence",
      items: [
        { label: "Overview", href: "/dashboard", icon: LayoutDashboard },
        { label: "Competencies", href: "/competencies", icon: Target },
        { label: "Skill Gaps", href: "/gaps", icon: AlertTriangle },
        { label: "Recommendations", href: "/recommendations", icon: Compass },
        { label: "Learning Paths", href: "/learning-paths", icon: Map },
        { label: "Assessments", href: "/assessments", icon: FileCheck2 },
      ],
    },
    {
      title: "Knowledge & Evidence",
      items: [
        { label: "Document Hub", href: "/documents", icon: FileText },
        { label: "AI Grounded Quizzes", href: "/quizzes", icon: HelpCircle },
        { label: "RAG Assistant", href: "/assistant", icon: MessageSquare },
        { label: "Evidence & Portfolio", href: "/evidence", icon: Award },
      ],
    },
    {
      title: "Specialized Track",
      items: [
        {
          label: "Government (MoSPI)",
          href: "/government",
          icon: Building2,
          active: currentTrack === "GOVERNMENT",
        },
        {
          label: "Industry Careers",
          href: "/industry",
          icon: Briefcase,
          active: currentTrack === "INDUSTRY",
        },
        {
          label: "Academic Bridge",
          href: "/academia",
          icon: GraduationCap,
          active: currentTrack === "ACADEMIA",
        },
      ],
    },
    {
      title: "Analytics & Oversight",
      items: [
        { label: "Workforce Analytics", href: "/analytics", icon: BarChart3 },
        { label: "Administration", href: "/admin", icon: ShieldCheck },
      ],
    },
  ];

  return (
    <aside className="w-72 bg-paper border-r border-[#E6E0D2] flex flex-col h-screen sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-[#E6E0D2]">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded bg-forest flex items-center justify-center text-paper font-serif font-bold text-lg">
            S
          </div>
          <div>
            <h1 className="text-base font-bold text-ink tracking-tight font-serif">
              STAT-SKILL AI
            </h1>
            <p className="text-[11px] text-[#5C5C5C] tracking-wide uppercase font-medium">
              Competency Intelligence
            </p>
          </div>
        </Link>

        {/* Track Switcher */}
        <div className="mt-4 bg-[#F2EDE1] p-1 rounded-md flex gap-1 text-[11px] font-medium text-ink">
          {(["GOVERNMENT", "INDUSTRY", "ACADEMIA"] as const).map((t) => (
            <button
              key={t}
              onClick={() => handleSwitchTrack(t)}
              className={`flex-1 py-1 rounded transition-colors text-center ${
                currentTrack === t
                  ? "bg-forest text-paper font-semibold shadow-xs"
                  : "text-[#5C5C5C] hover:text-ink"
              }`}
            >
              {t === "GOVERNMENT" ? "Gov" : t === "INDUSTRY" ? "Ind" : "Acad"}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation Groups */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {navGroups.map((grp) => (
          <div key={grp.title}>
            <p className="px-3 text-[10px] uppercase font-semibold text-[#8C8275] tracking-wider mb-1.5">
              {grp.title}
            </p>
            <nav className="space-y-0.5">
              {grp.items.map((item) => {
                const Icon = item.icon;
                const isActive =
                  pathname === item.href ||
                  (item.href !== "/dashboard" && pathname.startsWith(item.href));

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-all ${
                      isActive
                        ? "bg-forest text-paper shadow-xs"
                        : "text-[#2A2A2A] hover:bg-[#F2EDE1] hover:text-ink"
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon className={`w-4 h-4 ${isActive ? "text-paper" : "text-[#5C5C5C]"}`} />
                      <span>{item.label}</span>
                    </div>
                    {isActive && <ChevronRight className="w-3.5 h-3.5 opacity-80" />}
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-[#E6E0D2] bg-[#F7F3EA] flex items-center justify-between">
        <div className="flex items-center gap-2.5 overflow-hidden">
          <div className="w-8 h-8 rounded-full bg-forest text-paper font-bold text-xs flex items-center justify-center shrink-0">
            {user?.display_name?.charAt(0) || "U"}
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-semibold text-ink truncate">
              {user?.display_name || "Official User"}
            </p>
            <p className="text-[10px] text-[#5C5C5C] truncate uppercase tracking-wider">
              {user?.role || "Statistical Officer"}
            </p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          title="Sign Out"
          className="p-1.5 rounded text-[#5C5C5C] hover:text-terracotta hover:bg-[#EAE4D5] transition-colors"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
}
