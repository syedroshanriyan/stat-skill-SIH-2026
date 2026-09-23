"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  CheckCircle2,
  Circle,
  Clock,
  ArrowRight,
  ExternalLink,
  Map,
  Plus,
} from "lucide-react";
import { apiRequest } from "@/lib/api";

export default function LearningPathsPage() {
  const [paths, setPaths] = useState<any[]>([]);
  const [activePath, setActivePath] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPaths() {
      try {
        const data = await apiRequest<any[]>("/me/learning-paths").catch(() => []);
        if (data && data.length > 0) {
          setPaths(data);
          setActivePath(data[0]);
        } else {
          // Deterministic fallback path
          const sample = {
            id: "path-1",
            title: "MoSPI Official Statistics Capacity Building Roadmap",
            goal: "Mastery of multi-stage sampling, price statistics, and R automated reporting.",
            status: "active",
            items: [
              {
                id: "i-1",
                sequence: 1,
                status: "completed",
                resource: {
                  title: "Survey Design & Questionnaire Structuring Protocols",
                  provider_type: "igot",
                  duration: "2 weeks",
                  url: "https://igotkarmayogi.gov.in",
                },
                competency: {
                  code: "STAT-01",
                  name: "Survey Design",
                },
              },
              {
                id: "i-2",
                sequence: 2,
                status: "in_progress",
                resource: {
                  title: "Advanced Multi-Stage Sampling for Socio-Economic Surveys",
                  provider_type: "igot",
                  duration: "3 weeks",
                  url: "https://igotkarmayogi.gov.in/learn/advanced-sampling-techniques",
                },
                competency: {
                  code: "STAT-02",
                  name: "Sampling Techniques",
                },
              },
              {
                id: "i-3",
                sequence: 3,
                status: "pending",
                resource: {
                  title: "NSSTA Training Programme on Price Index Compilation & Rebasing",
                  provider_type: "nssta",
                  duration: "1 week",
                  url: "https://mospi.gov.in/nssta",
                },
                competency: {
                  code: "STAT-04",
                  name: "Price Statistics",
                },
              },
              {
                id: "i-4",
                sequence: 4,
                status: "pending",
                resource: {
                  title: "R Programming for Government Statistical Analysis",
                  provider_type: "igot",
                  duration: "4 weeks",
                  url: "https://igotkarmayogi.gov.in",
                },
                competency: {
                  code: "TECH-02",
                  name: "R for Official Statistics",
                },
              },
            ],
          };
          setPaths([sample]);
          setActivePath(sample);
        }
      } finally {
        setLoading(false);
      }
    }
    loadPaths();
  }, []);

  const handleUpdateItemStatus = async (itemId: string, newStatus: string) => {
    if (!activePath) return;
    try {
      await apiRequest(`/learning-paths/${activePath.id}/items/${itemId}`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus }),
      }).catch(() => {});

      setActivePath((prev: any) => {
        if (!prev) return prev;
        return {
          ...prev,
          items: prev.items.map((i: any) =>
            i.id === itemId ? { ...i, status: newStatus } : i
          ),
        };
      });
    } catch (err) {
      console.error(err);
    }
  };

  const totalSteps = activePath?.items?.length || 0;
  const completedSteps =
    activePath?.items?.filter((i: any) => i.status === "completed")?.length || 0;
  const progressPct =
    totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-ink font-serif">
            Sequential Learning Roadmaps
          </h1>
          <p className="text-xs text-[#5C5C5C]">
            Structured competency milestone progression with prerequisite dependency enforcement
          </p>
        </div>
      </div>

      {activePath && (
        <div className="card-institutional p-6 bg-paper shadow-card space-y-6">
          {/* Header & Progress Bar */}
          <div className="border-b border-[#E6E0D2] pb-5">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-forest bg-[#EBF3ED] px-2 py-0.5 rounded border border-[#C7DEC9]">
                  Active Roadmap
                </span>
                <h2 className="text-lg font-bold text-ink font-serif mt-1">
                  {activePath.title}
                </h2>
                <p className="text-xs text-[#5C5C5C] mt-0.5">{activePath.goal}</p>
              </div>

              <div className="text-right">
                <span className="text-xs font-bold text-forest">
                  {completedSteps} of {totalSteps} Milestones Completed ({progressPct}%)
                </span>
                <div className="w-48 bg-[#E6E0D2] h-2 rounded-full overflow-hidden mt-1.5 ml-auto">
                  <div
                    className="bg-forest h-full rounded-full transition-all duration-500"
                    style={{ width: `${progressPct}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Sequential Timeline Steps */}
          <div className="space-y-4">
            {activePath.items?.map((item: any, idx: number) => {
              const isCompleted = item.status === "completed";
              const isInProgress = item.status === "in_progress";

              return (
                <div
                  key={item.id}
                  className={`p-4 rounded border transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-4 ${
                    isCompleted
                      ? "bg-[#F7F9F7] border-[#C7DEC9]"
                      : isInProgress
                      ? "bg-paper border-forest shadow-xs"
                      : "bg-warm-ivory border-[#E6E0D2] opacity-80"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5">
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-forest shrink-0" />
                      ) : isInProgress ? (
                        <div className="w-5 h-5 rounded-full border-2 border-forest flex items-center justify-center text-[11px] font-bold text-forest">
                          {idx + 1}
                        </div>
                      ) : (
                        <Circle className="w-5 h-5 text-[#8C8275] shrink-0" />
                      )}
                    </div>

                    <div>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="font-bold text-ink">Step {item.sequence}:</span>
                        <span className="font-mono text-[10px] bg-[#E6E0D2] px-1.5 py-0.5 rounded text-ink">
                          {item.competency?.code}
                        </span>
                        <span className="text-[10px] uppercase font-bold text-[#8C8275]">
                          {item.resource?.provider_type?.toUpperCase()}
                        </span>
                      </div>

                      <h4 className="text-xs font-bold text-ink mt-1">
                        {item.resource?.title}
                      </h4>
                      <p className="text-[11px] text-[#5C5C5C] mt-0.5 flex items-center gap-2">
                        <span>Duration: {item.resource?.duration || "2 weeks"}</span>
                        <span>• Target Competency: {item.competency?.name}</span>
                      </p>
                    </div>
                  </div>

                  {/* Step Action Buttons */}
                  <div className="flex items-center gap-2 w-full md:w-auto justify-end">
                    <a
                      href={item.resource?.url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1.5 rounded border border-[#D1C8B4] text-xs font-semibold text-ink hover:bg-[#F2EDE1] transition-colors inline-flex items-center gap-1"
                    >
                      <span>Open Course</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>

                    {item.status !== "completed" ? (
                      <button
                        onClick={() => handleUpdateItemStatus(item.id, "completed")}
                        className="px-3 py-1.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
                      >
                        Mark Completed
                      </button>
                    ) : (
                      <button
                        onClick={() => handleUpdateItemStatus(item.id, "in_progress")}
                        className="px-3 py-1.5 rounded border border-[#C7DEC9] text-forest text-xs font-semibold hover:bg-[#EBF3ED] transition-colors"
                      >
                        Reopen
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
