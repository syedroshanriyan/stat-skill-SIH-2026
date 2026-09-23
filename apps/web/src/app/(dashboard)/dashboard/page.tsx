"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import {
  Target,
  AlertTriangle,
  Compass,
  ArrowRight,
  TrendingUp,
  FileCheck2,
  CheckCircle2,
  HelpCircle,
  Upload,
  Sparkles,
  Layers,
  Award,
  Clock,
} from "lucide-react";
import { apiRequest, getStoredUser, StoredUser } from "@/lib/api";

export default function DashboardOverviewPage() {
  const [user, setUser] = useState<StoredUser | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [gaps, setGaps] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const u = getStoredUser();
    setUser(u);

    async function loadData() {
      try {
        const [anData, gapData, recData] = await Promise.all([
          apiRequest<any>("/analytics/me").catch(() => null),
          apiRequest<any[]>("/me/gaps").catch(() => []),
          apiRequest<any[]>("/me/recommendations").catch(() => []),
        ]);

        if (anData) {
          setAnalytics(anData);
        } else {
          // Unestablished state (no fake data)
          setAnalytics({
            has_completed_diagnostic: false,
            total_competencies_tracked: 0,
            overall_score: 0,
            radar_data: [],
            open_gaps_count: 0,
            critical_gaps_count: 0,
            learning_progress_pct: 0,
          });
        }

        if (gapData && Array.isArray(gapData)) {
          setGaps(gapData.slice(0, 4));
        }

        if (recData && Array.isArray(recData)) {
          setRecommendations(recData.slice(0, 3));
        }
      } catch (err) {
        console.error("Error loading analytics data:", err);
      } finally {
        setLoading(false);
      }
    }

    loadData();

    // Live Event Invalidation: Automatically re-query backend when competency state mutates
    const handleCompetencyUpdate = () => {
      loadData();
    };

    window.addEventListener("statskill:competency-updated", handleCompetencyUpdate);
    return () => {
      window.removeEventListener("statskill:competency-updated", handleCompetencyUpdate);
    };
  }, []);

  const hasBaseline = Boolean(
    analytics?.has_completed_diagnostic &&
    (analytics?.total_competencies_tracked || 0) > 0
  );

  const radarData = analytics?.radar_data || [];

  return (
    <div className="space-y-8 font-sans">
      {/* Top Welcome Banner */}
      <div className="card-institutional p-6 bg-paper flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm border-[#E6E0D2]">
        <div>
          <span className="text-[10px] uppercase font-bold text-forest tracking-wider bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
            {user?.track || "GOVERNMENT"} TRACK
          </span>
          <h1 className="text-2xl font-bold text-ink font-serif mt-1.5">
            Welcome back, {user?.display_name || "Official"}
          </h1>
          <p className="text-xs text-[#5C5C5C] mt-1">
            Designation: <span className="font-semibold text-ink">{user?.role || "Statistical Officer"}</span> • Organization Scope:{" "}
            <span className="font-semibold text-ink">Authorized MoSPI Scope</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/assessments"
            className="px-4 py-2 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors flex items-center gap-2 shadow-xs"
          >
            <FileCheck2 className="w-4 h-4" />
            <span>Official Diagnostic</span>
          </Link>
          <Link
            href="/documents"
            className="px-4 py-2 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors flex items-center gap-2"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Document</span>
          </Link>
        </div>
      </div>

      {/* Conditional Rendering: New-User Onboarding Roadmap vs Active Radar Dashboard */}
      {!hasBaseline ? (
        /* New-User Onboarding Roadmap */
        <div className="space-y-6">
          <div className="card-institutional p-8 bg-paper border-[#E6E0D2] shadow-sm">
            <div className="max-w-3xl">
              <span className="text-[10px] uppercase font-bold tracking-widest text-[#8C8275]">
                New-User Onboarding Roadmap
              </span>
              <h2 className="text-2xl font-bold text-ink font-serif mt-1">
                Establish Your Calibrated Competency Baseline
              </h2>
              <p className="text-xs text-[#5C5C5C] mt-2 leading-relaxed">
                Welcome to STAT-SKILL AI. Zero uncalibrated metrics or arbitrary mock data are shown
                before your initial evaluation. Complete the official baseline diagnostic assessment
                to establish your dynamic competency profile, calculate priority skill gaps, and activate personalized iGOT / NSSTA learning paths.
              </p>
            </div>

            {/* Stepper Progress */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Stage 0 */}
              <div className="p-4 rounded-lg bg-[#EBF3ED] border border-[#C7DEC9]">
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="font-mono text-[10px] font-bold text-forest">STAGE 0</span>
                  <CheckCircle2 className="w-4 h-4 text-forest" />
                </div>
                <h4 className="text-xs font-bold text-forest">Profile Created</h4>
                <p className="text-[11px] text-[#5C5C5C] mt-1">
                  Track: {user?.track || "Government"}
                </p>
                <span className="mt-3 inline-block text-[10px] font-bold text-forest uppercase">
                  Completed
                </span>
              </div>

              {/* Stage 1 - Active Next Action */}
              <div className="p-4 rounded-lg bg-[#FAF8F5] border-2 border-forest shadow-xs">
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="font-mono text-[10px] font-bold text-forest">STAGE 1</span>
                  <Sparkles className="w-4 h-4 text-forest" />
                </div>
                <h4 className="text-xs font-bold text-ink">Diagnostic Assessment</h4>
                <p className="text-[11px] text-[#5C5C5C] mt-1">
                  Psychometric baseline test across key competencies
                </p>
                <span className="mt-3 inline-block text-[10px] font-bold text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9] uppercase">
                  Current Action
                </span>
              </div>

              {/* Stage 2 */}
              <div className="p-4 rounded-lg bg-[#FAF8F5] border border-[#E6E0D2] opacity-70">
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="font-mono text-[10px] font-bold text-[#8C8275]">STAGE 2</span>
                  <Clock className="w-4 h-4 text-[#8C8275]" />
                </div>
                <h4 className="text-xs font-bold text-ink">Radar Spectrum</h4>
                <p className="text-[11px] text-[#5C5C5C] mt-1">
                  Automated radar mapping based on verified scores
                </p>
                <span className="mt-3 inline-block text-[10px] text-[#8C8275] uppercase">
                  Pending Stage 1
                </span>
              </div>

              {/* Stage 3 */}
              <div className="p-4 rounded-lg bg-[#FAF8F5] border border-[#E6E0D2] opacity-70">
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="font-mono text-[10px] font-bold text-[#8C8275]">STAGE 3</span>
                  <Clock className="w-4 h-4 text-[#8C8275]" />
                </div>
                <h4 className="text-xs font-bold text-ink">Capacity Building</h4>
                <p className="text-[11px] text-[#5C5C5C] mt-1">
                  Personalized iGOT / NSSTA learning roadmap
                </p>
                <span className="mt-3 inline-block text-[10px] text-[#8C8275] uppercase">
                  Pending Stage 1
                </span>
              </div>
            </div>

            {/* Direct Call to Action */}
            <div className="mt-8 pt-6 border-t border-[#E6E0D2] flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="text-left">
                <h4 className="text-sm font-bold text-ink font-serif">
                  Ready to complete your diagnostic assessment?
                </h4>
                <p className="text-xs text-[#5C5C5C]">
                  Takes approximately 15 minutes • Calibrated psychometric questions • Instant radar update
                </p>
              </div>

              <Link
                href="/assessments"
                className="px-6 py-3 rounded bg-forest text-paper text-xs font-bold hover:bg-forest-light transition-all flex items-center gap-2 shadow-xs shrink-0"
              >
                <FileCheck2 className="w-4 h-4" />
                <span>Complete Diagnostic Assessment Now</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      ) : (
        /* Active Competency Intelligence Dashboard */
        <div className="space-y-8">
          {/* KPI Metric Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="card-institutional p-5 bg-paper shadow-xs">
              <div className="flex items-center justify-between text-[#8C8275] mb-2">
                <span className="text-xs font-medium">Overall Score</span>
                <Target className="w-4 h-4 text-forest" />
              </div>
              <div className="text-2xl font-bold font-serif text-ink">
                {analytics?.overall_score || 0}%
              </div>
              <p className="text-[11px] text-[#5C5C5C] mt-1">
                Across {analytics?.total_competencies_tracked || 0} tracked competencies
              </p>
            </div>

            <div className="card-institutional p-5 bg-paper shadow-xs">
              <div className="flex items-center justify-between text-[#8C8275] mb-2">
                <span className="text-xs font-medium">Critical Gaps</span>
                <AlertTriangle className="w-4 h-4 text-terracotta" />
              </div>
              <div className="text-2xl font-bold font-serif text-terracotta">
                {analytics?.critical_gaps_count || 0}
              </div>
              <p className="text-[11px] text-[#5C5C5C] mt-1">
                Require priority capacity building
              </p>
            </div>

            <div className="card-institutional p-5 bg-paper shadow-xs">
              <div className="flex items-center justify-between text-[#8C8275] mb-2">
                <span className="text-xs font-medium">Roadmap Progress</span>
                <TrendingUp className="w-4 h-4 text-gold-dark" />
              </div>
              <div className="text-2xl font-bold font-serif text-ink">
                {analytics?.learning_progress_pct || 0}%
              </div>
              <p className="text-[11px] text-[#5C5C5C] mt-1">
                {analytics?.completed_learning_steps || 0} of {analytics?.total_learning_steps || 0} items completed
              </p>
            </div>

            <div className="card-institutional p-5 bg-paper shadow-xs">
              <div className="flex items-center justify-between text-[#8C8275] mb-2">
                <span className="text-xs font-medium">Assessment Status</span>
                <CheckCircle2 className="w-4 h-4 text-forest" />
              </div>
              <div className="text-2xl font-bold font-serif text-forest">
                Validated
              </div>
              <p className="text-[11px] text-[#5C5C5C] mt-1">
                Avg: {analytics?.average_assessment_score || 0}% ({analytics?.assessment_attempts_count || 0} attempts)
              </p>
            </div>
          </div>

          {/* Main Visuals: Competency Radar & Top Skill Gaps */}
          <div className="grid md:grid-cols-12 gap-8">
            {/* Radar Chart (7 cols) */}
            <div className="md:col-span-7 card-institutional p-6 bg-paper shadow-xs flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-sm font-bold text-ink font-serif">
                    Competency Radar Spectrum
                  </h3>
                  <p className="text-xs text-[#5C5C5C]">
                    Reading live database records • Compared against Level 3 proficiency benchmark
                  </p>
                </div>
                <Link
                  href="/competencies"
                  className="text-xs text-forest hover:underline font-semibold"
                >
                  View Full Framework
                </Link>
              </div>

              <div className="h-72 w-full">
                {radarData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="#E6E0D2" />
                      <PolarAngleAxis
                        dataKey="name"
                        tick={{ fill: "#2A2A2A", fontSize: 10, fontWeight: 500 }}
                      />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#D1C8B4" />
                      <Radar
                        name="Benchmark"
                        dataKey="required_level"
                        stroke="#D1C8B4"
                        strokeDasharray="3 3"
                        fill="transparent"
                      />
                      <Radar
                        name="Current Score"
                        dataKey="score"
                        stroke="#1F4D3A"
                        fill="#A7B9A7"
                        fillOpacity={0.4}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex items-center justify-center text-xs text-[#5C5C5C]">
                    No competency data available. Complete diagnostic assessment.
                  </div>
                )}
              </div>
            </div>

            {/* Priority Skill Gaps (5 cols) */}
            <div className="md:col-span-5 card-institutional p-6 bg-paper shadow-xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-ink font-serif">
                    Priority Skill Shortfalls
                  </h3>
                  <Link href="/gaps" className="text-xs text-forest hover:underline font-semibold">
                    Full Report
                  </Link>
                </div>

                <div className="space-y-3">
                  {gaps.length > 0 ? (
                    gaps.map((gap) => (
                      <div
                        key={gap.id}
                        className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory flex items-start justify-between"
                      >
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[10px] bg-[#E6E0D2] text-ink px-1.5 py-0.5 rounded font-bold">
                              {gap.competency?.code}
                            </span>
                            <span
                              className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                                gap.priority === "CRITICAL"
                                  ? "bg-[#F9ECE7] text-terracotta border border-[#E5C1B4]"
                                  : "bg-[#F7F1E6] text-gold-dark border border-[#E2CEAB]"
                              }`}
                            >
                              {gap.priority}
                            </span>
                          </div>
                          <p className="text-xs font-semibold text-ink mt-1">
                            {gap.competency?.name}
                          </p>
                          <p className="text-[11px] text-[#5C5C5C]">
                            Current: {gap.current_score} pts • Gap: -{gap.gap_value} pts
                          </p>
                        </div>
                        <Link
                          href={`/recommendations?comp=${gap.competency?.id || ""}`}
                          className="text-xs text-forest hover:text-forest-dark font-medium underline"
                        >
                          Remediate
                        </Link>
                      </div>
                    ))
                  ) : (
                    <div className="p-4 text-center text-xs text-[#5C5C5C]">
                      No active skill gaps identified. Benchmark standards met.
                    </div>
                  )}
                </div>
              </div>

              <Link
                href="/gaps"
                className="mt-4 w-full py-2 rounded border border-[#D1C8B4] text-xs font-semibold text-center hover:bg-[#F2EDE1] transition-colors"
              >
                Review Gap Analysis
              </Link>
            </div>
          </div>

          {/* Recommended Learning Programs (iGOT / NSSTA) */}
          <div className="card-institutional p-6 bg-paper shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-ink font-serif">
                  Curated Training Programs (iGOT & NSSTA)
                </h3>
                <p className="text-xs text-[#5C5C5C]">
                  Ranked through hybrid recommendation engine targeting identified priority shortfalls
                </p>
              </div>
              <Link
                href="/recommendations"
                className="text-xs text-forest hover:underline font-semibold"
              >
                Explore Catalog
              </Link>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {recommendations.map((rec) => (
                <div
                  key={rec.id}
                  className="p-4 rounded border border-[#E6E0D2] bg-warm-ivory flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span
                        className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                          rec.resource?.provider_type === "igot"
                            ? "bg-[#EBF3ED] text-forest border border-[#C7DEC9]"
                            : "bg-[#F7F1E6] text-gold-dark border border-[#E2CEAB]"
                        }`}
                      >
                        {rec.resource?.provider_type === "igot"
                          ? "iGOT Karmayogi"
                          : "NSSTA TPAC Programme"}
                      </span>
                      <span className="text-[11px] font-semibold text-[#8C8275]">
                        Score: {rec.score}
                      </span>
                    </div>
                    <h4 className="text-xs font-bold text-ink">{rec.resource?.title}</h4>
                    <p className="text-[11px] text-[#5C5C5C] mt-1 line-clamp-2">
                      {rec.explanation}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-[#E6E0D2] flex items-center justify-between text-xs">
                    <span className="text-[#8C8275] text-[11px]">
                      Duration: {rec.resource?.duration || "Self-paced"}
                    </span>
                    <Link
                      href="/learning-paths"
                      className="text-forest hover:text-forest-dark font-semibold flex items-center gap-1"
                    >
                      <span>Add to Roadmap</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
