"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Target, Layers, ArrowUpRight, Search, ShieldCheck } from "lucide-react";
import { apiRequest } from "@/lib/api";

export default function CompetenciesPage() {
  const [competencies, setCompetencies] = useState<any[]>([]);
  const [selectedCat, setSelectedCat] = useState<string>("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedComp, setSelectedComp] = useState<any | null>(null);

  useEffect(() => {
    async function loadCompetencies() {
      try {
        const data = await apiRequest<any[]>("/me/competencies").catch(() => []);
        if (data && data.length > 0) {
          setCompetencies(data);
          setSelectedComp(data[0]);
        } else {
          // Deterministic fallback
          const sample = [
            {
              id: "c1",
              score: 72.0,
              proficiency_level: 3,
              confidence: 0.85,
              source: "diagnostic",
              competency: {
                code: "STAT-01",
                name: "Survey Design",
                category: "Statistical",
                description: "Methodology for planning, structuring, and launching national-scale census and sample surveys.",
                level_definitions_json: {
                  "1": "Novice: Understands basic census terminology",
                  "2": "Beginner: Can design standard questionnaire modules",
                  "3": "Competent: Performs independent multi-stage survey design",
                  "4": "Proficient: Solves complex response burden & coverage issues",
                  "5": "Expert: Architects national statistical survey frameworks"
                }
              }
            },
            {
              id: "c2",
              score: 55.0,
              proficiency_level: 2,
              confidence: 0.80,
              source: "diagnostic",
              competency: {
                code: "STAT-02",
                name: "Sampling Techniques",
                category: "Statistical",
                description: "Stratified, multi-stage, cluster, and probability proportional to size (PPS) sampling.",
                level_definitions_json: {
                  "1": "Awareness of simple random sampling",
                  "2": "Calculates standard sample size",
                  "3": "Executes PPS and stratified sampling designs",
                  "4": "Applies variance estimation on complex survey weights",
                  "5": "Designs master sampling frames"
                }
              }
            },
            {
              id: "c3",
              score: 80.0,
              proficiency_level: 4,
              confidence: 0.90,
              source: "diagnostic",
              competency: {
                code: "STAT-06",
                name: "Data Quality Frameworks",
                category: "Statistical",
                description: "Statistical data quality assessment, accuracy, timeliness, and metadata documentation.",
                level_definitions_json: {
                  "1": "Basic quality checks",
                  "2": "Identifies non-sampling errors",
                  "3": "Implements validation pipelines",
                  "4": "Establishes National Data Quality Standards",
                  "5": "Directs UN NQAF implementation"
                }
              }
            },
            {
              id: "c4",
              score: 62.0,
              proficiency_level: 3,
              confidence: 0.80,
              source: "diagnostic",
              competency: {
                code: "TECH-01",
                name: "Python for Analytics",
                category: "Technical",
                description: "Data manipulation with Pandas, NumPy, statistical modeling, and automation scripting.",
                level_definitions_json: {
                  "1": "Syntax awareness",
                  "2": "Pandas dataframe cleaning",
                  "3": "Statistical modeling & scripting",
                  "4": "Pipeline engineering",
                  "5": "High-performance architecture"
                }
              }
            },
            {
              id: "c5",
              score: 35.0,
              proficiency_level: 1,
              confidence: 0.65,
              source: "diagnostic",
              competency: {
                code: "TECH-02",
                name: "R for Official Statistics",
                category: "Technical",
                description: "Statistical computing, survey weighting, econometrics, and survey package usage.",
                level_definitions_json: {
                  "1": "RStudio basics",
                  "2": "Descriptive statistics",
                  "3": "Uses 'survey' package for weights",
                  "4": "Custom econometric modeling",
                  "5": "CRAN statistical package author"
                }
              }
            },
            {
              id: "c6",
              score: 50.0,
              proficiency_level: 2,
              confidence: 0.75,
              source: "diagnostic",
              competency: {
                code: "GOV-01",
                name: "Cybersecurity & Data Privacy",
                category: "Digital Governance",
                description: "IT security policies, data classification, anonymization, and DPDP Act compliance.",
                level_definitions_json: {
                  "1": "Basic password security",
                  "2": "Awareness of DPDP Act principles",
                  "3": "Performs statistical microdata anonymization",
                  "4": "Leads organizational data audit",
                  "5": "National statistical security strategist"
                }
              }
            }
          ];
          setCompetencies(sample);
          setSelectedComp(sample[0]);
        }
      } catch (e) {
        console.error(e);
      }
    }
    loadCompetencies();
  }, []);

  const categories = ["All", "Statistical", "Technical", "Digital Governance", "Behavioural / Managerial"];

  const filtered = competencies.filter((c) => {
    const matchCat = selectedCat === "All" || c.competency?.category === selectedCat;
    const matchSearch =
      searchTerm === "" ||
      c.competency?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.competency?.code.toLowerCase().includes(searchTerm.toLowerCase());
    return matchCat && matchSearch;
  });

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-ink font-serif">
            Competency Profile & Taxonomy
          </h1>
          <p className="text-xs text-[#5C5C5C]">
            Versioned competency records with validated proficiency levels (1–5) and provenance tracking
          </p>
        </div>
        <Link
          href="/assessments"
          className="px-4 py-2 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
        >
          Take Assessment
        </Link>
      </div>

      {/* Filter and Search Bar */}
      <div className="card-institutional p-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCat(cat)}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                selectedCat === cat
                  ? "bg-forest text-paper"
                  : "bg-warm-ivory text-[#2A2A2A] hover:bg-[#EAE4D5]"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-3.5 h-3.5 text-[#8C8275] absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search competency or code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded bg-warm-ivory border border-[#D1C8B4] text-xs text-ink focus:outline-none focus:border-forest"
          />
        </div>
      </div>

      {/* 2-Column Split View: List on left, details on right */}
      <div className="grid md:grid-cols-12 gap-6">
        {/* Competencies Table/List (7 cols) */}
        <div className="md:col-span-7 space-y-3">
          {filtered.map((item) => {
            const isSelected = selectedComp?.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setSelectedComp(item)}
                className={`card-institutional p-4 cursor-pointer transition-all ${
                  isSelected
                    ? "border-forest bg-[#F7F3EA] shadow-xs"
                    : "hover:border-[#D1C8B4] bg-paper"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
                      {item.competency?.code}
                    </span>
                    <span className="text-[11px] font-medium text-[#8C8275]">
                      {item.competency?.category}
                    </span>
                  </div>
                  <span className="text-xs font-bold text-ink">
                    {item.score}% (Level {item.proficiency_level})
                  </span>
                </div>

                <h3 className="text-sm font-semibold text-ink mt-2">
                  {item.competency?.name}
                </h3>
                <p className="text-xs text-[#5C5C5C] mt-1 line-clamp-2">
                  {item.competency?.description}
                </p>

                {/* Score Bar */}
                <div className="mt-3 flex items-center gap-3">
                  <div className="flex-1 bg-[#E6E0D2] h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-forest h-full rounded-full transition-all duration-500"
                      style={{ width: `${item.score}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-[#5C5C5C] font-mono">
                    Conf: {(item.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Competency Detail Drawer (5 cols) */}
        <div className="md:col-span-5">
          {selectedComp ? (
            <div className="card-institutional p-6 bg-paper sticky top-24 space-y-5">
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
                    {selectedComp.competency?.code}
                  </span>
                  <div className="flex items-center gap-1 text-[11px] text-forest font-semibold">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span className="capitalize">Source: {selectedComp.source}</span>
                  </div>
                </div>
                <h2 className="text-base font-bold text-ink font-serif mt-2">
                  {selectedComp.competency?.name}
                </h2>
                <p className="text-xs text-[#5C5C5C] mt-1">
                  {selectedComp.competency?.description}
                </p>
              </div>

              {/* Metric Breakdown */}
              <div className="grid grid-cols-2 gap-3 p-3 rounded bg-warm-ivory border border-[#E6E0D2] text-xs">
                <div>
                  <span className="text-[#8C8275] text-[10px] uppercase font-semibold">
                    Evaluated Score
                  </span>
                  <div className="text-lg font-bold font-serif text-ink mt-0.5">
                    {selectedComp.score} / 100
                  </div>
                </div>
                <div>
                  <span className="text-[#8C8275] text-[10px] uppercase font-semibold">
                    Proficiency Level
                  </span>
                  <div className="text-lg font-bold font-serif text-forest mt-0.5">
                    Level {selectedComp.proficiency_level} of 5
                  </div>
                </div>
              </div>

              {/* Level Definitions 1 to 5 */}
              <div>
                <h4 className="text-xs font-bold text-ink font-serif mb-2">
                  Proficiency Level Definitions
                </h4>
                <div className="space-y-1.5 text-xs">
                  {[1, 2, 3, 4, 5].map((lvl) => {
                    const desc =
                      selectedComp.competency?.level_definitions_json?.[String(lvl)] ||
                      `Level ${lvl} operational capabilities`;
                    const isCurrent = selectedComp.proficiency_level === lvl;

                    return (
                      <div
                        key={lvl}
                        className={`p-2 rounded border text-[11px] ${
                          isCurrent
                            ? "bg-[#EBF3ED] border-forest text-ink font-semibold"
                            : "bg-warm-ivory border-[#E6E0D2] text-[#5C5C5C]"
                        }`}
                      >
                        <span className="font-bold mr-1.5">Level {lvl}:</span>
                        <span>{desc}</span>
                        {isCurrent && (
                          <span className="ml-2 text-[10px] uppercase font-bold text-forest">
                            (Current Status)
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Direct Remediation Link */}
              <div className="pt-3 border-t border-[#E6E0D2]">
                <Link
                  href={`/recommendations?comp=${selectedComp.competency?.id || ""}`}
                  className="w-full py-2 rounded bg-forest text-paper text-xs font-semibold flex items-center justify-center gap-1.5 hover:bg-forest-light transition-colors"
                >
                  <span>Find Targeted Courses (iGOT / NSSTA)</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ) : (
            <div className="card-institutional p-8 text-center text-xs text-[#5C5C5C]">
              Select a competency to view full level definitions and provenance details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
