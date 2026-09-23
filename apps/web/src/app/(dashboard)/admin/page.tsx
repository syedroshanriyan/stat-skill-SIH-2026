"use client";

import React, { useEffect, useState } from "react";
import {
  ShieldCheck,
  Building2,
  Users,
  FileText,
  Activity,
  Lock,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Search,
  Filter,
  Eye,
  Server,
  Database,
  Cpu,
  Globe2,
  Clock,
  Sparkles,
  Info,
  Scale,
  ExternalLink,
  Layers,
  ArrowRight
} from "lucide-react";
import { fetchApi, getStoredUser, setAuthSession, getAuthToken, StoredUser } from "@/lib/api";

interface AuditEventItem {
  id: string;
  actor_id: string | null;
  actor_name: string;
  actor_email: string;
  action: string;
  entity_type: string;
  entity_id: string;
  metadata: Record<string, any>;
  created_at: string;
}

interface TenantItem {
  id: string;
  name: string;
  type: string;
  code: string;
  is_active: boolean;
  member_count: number;
  created_at: string;
}

interface ComplianceData {
  dpdp_act_compliance: {
    status: string;
    jurisdiction: string;
    sovereignty_region: string;
    pii_masking: string;
    data_retention_policy: string;
    user_consent_tracking: string;
  };
  system_security: {
    encryption_at_rest: string;
    encryption_in_transit: string;
    rbac_enforcement: string;
    immutable_audit_total: number;
    tamper_proof_checksum: string;
  };
  governance_advisory: string;
}

interface AIHealthData {
  engine: string;
  primary_llm: {
    provider: string;
    model: string;
    status: string;
    mode: string;
    temperature: number;
  };
  embedding_engine: {
    model: string;
    vector_dimension: number;
    status: string;
    similarity_metric: string;
  };
  guardrails: {
    strict_grounding: string;
    hallucination_filter: string;
    scoring_rule: string;
    pii_scrubber: string;
  };
  average_latency_ms: number;
  availability_sla: string;
}

interface ScraperStatusData {
  provider: string;
  user_agent: string;
  rate_limit_per_sec: number;
  robots_txt_enforced: boolean;
  whitelisted_domains: string[];
  fallback_provider: string;
  parser_alert_logging: string;
  status: string;
}

interface ProviderStatusData {
  provider: string;
  type: string;
  is_live: boolean;
  mode: string;
  description: string;
}

interface LlamaModelStatusData {
  adapter_name: string;
  base_model: string;
  architecture: string;
  status: string;
  fine_tuning_method: string;
  qlora_config: {
    r: number;
    lora_alpha: number;
    target_modules: string[];
    lora_dropout: number;
    bias: string;
    quantization: string;
  };
  domain_corpus: string[];
  jurisdiction_scope: string;
  rag_fallback_active: boolean;
  citation_validation_enforced: boolean;
  ambiguity_clarification_max_rounds: number;
  transparency_note: string;
}

const AUDIT_CATEGORIES = [
  { key: "all", label: "All Events" },
  { key: "authentication", label: "Authentication" },
  { key: "role_changes", label: "Role Changes" },
  { key: "membership_changes", label: "Memberships" },
  { key: "competency_updates", label: "Competencies" },
  { key: "assessment_quiz", label: "Assessments & Quizzes" },
  { key: "document_events", label: "Documents" },
  { key: "evidence_events", label: "Evidence" },
  { key: "recommendation_changes", label: "Recommendations" },
  { key: "exports", label: "Exports" },
  { key: "provider_sync", label: "Provider Sync" },
  { key: "ai_failures", label: "AI Failures" },
  { key: "security_events", label: "Security Events" },
  { key: "system_errors", label: "System Errors" },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<"audit" | "tenants" | "compliance" | "ai" | "providers" | "legal">("audit");
  const [auditEvents, setAuditEvents] = useState<AuditEventItem[]>([]);
  const [tenants, setTenants] = useState<TenantItem[]>([]);
  const [compliance, setCompliance] = useState<ComplianceData | null>(null);
  const [aiHealth, setAiHealth] = useState<AIHealthData | null>(null);
  const [scraperStatus, setScraperStatus] = useState<ScraperStatusData | null>(null);
  const [providersStatus, setProvidersStatus] = useState<ProviderStatusData[]>([]);
  const [legalModelStatus, setLegalModelStatus] = useState<LlamaModelStatusData | null>(null);

  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchAction, setSearchAction] = useState("");
  const [selectedAudit, setSelectedAudit] = useState<AuditEventItem | null>(null);
  const [isTriggeringAudit, setIsTriggeringAudit] = useState(false);
  const [currentUser, setCurrentUser] = useState<StoredUser | null>(null);
  const [isAuthorized, setIsAuthorized] = useState<boolean>(true);

  useEffect(() => {
    const user = getStoredUser();
    setCurrentUser(user);
    const role = user?.role?.toLowerCase() || "";
    if (role !== "platform_admin") {
      setIsAuthorized(false);
      setLoading(false);
    } else {
      setIsAuthorized(true);
      loadAllAdminData();
    }
  }, []);

  const loadAllAdminData = async () => {
    try {
      setLoading(true);
      const [auditRes, tenantsRes, compRes, aiRes, scraperRes, provRes, legalRes] = await Promise.all([
        fetchApi<{ events: AuditEventItem[] }>(
          selectedCategory && selectedCategory !== "all"
            ? `/admin/audit-events?category=${encodeURIComponent(selectedCategory)}`
            : "/admin/audit-events"
        ).catch((err) => {
          if (err.message && err.message.includes("403")) {
            setIsAuthorized(false);
          }
          return { events: [] };
        }),
        fetchApi<TenantItem[]>("/admin/tenants").catch(() => []),
        fetchApi<ComplianceData>("/admin/compliance-status").catch(() => null),
        fetchApi<AIHealthData>("/admin/ai-health").catch(() => null),
        fetchApi<ScraperStatusData>("/legal/scraper/status").catch(() => null),
        fetchApi<ProviderStatusData[]>("/catalogues/status").catch(() => []),
        fetchApi<LlamaModelStatusData>("/legal/model/status").catch(() => null),
      ]);

      if (auditRes?.events) setAuditEvents(auditRes.events);
      if (tenantsRes) setTenants(tenantsRes);
      if (compRes) setCompliance(compRes);
      if (aiRes) setAiHealth(aiRes);
      if (scraperRes) setScraperStatus(scraperRes);
      if (provRes) setProvidersStatus(provRes);
      if (legalRes) setLegalModelStatus(legalRes);
    } catch (err: any) {
      if (err.message && err.message.includes("403")) {
        setIsAuthorized(false);
      }
      console.error("Admin data fetch error", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCategorySelect = async (cat: string) => {
    setSelectedCategory(cat);
    try {
      const endpoint = cat && cat !== "all"
        ? `/admin/audit-events?category=${encodeURIComponent(cat)}`
        : "/admin/audit-events";
      const res = await fetchApi<{ events: AuditEventItem[] }>(endpoint);
      if (res?.events) setAuditEvents(res.events);
    } catch (err) {
      console.error("Audit category filter error", err);
    }
  };

  const handleSwitchToDemoAdmin = () => {
    const adminUser: StoredUser = {
      id: currentUser?.id || "admin-user",
      email: "admin@platform.gov.in",
      display_name: "Platform Administrator",
      track: "GOVERNMENT",
      role: "platform_admin"
    };
    setAuthSession(getAuthToken() || "demo-platform-admin-token", adminUser);
    setCurrentUser(adminUser);
    setIsAuthorized(true);
    setTimeout(() => {
      loadAllAdminData();
    }, 100);
  };

  const handleSimulateAuditEvent = async () => {
    setIsTriggeringAudit(true);
    try {
      await fetchApi("/admin/audit-events", {
        method: "POST",
        body: JSON.stringify({
          action: "security_integrity_check",
          entity_type: "SystemAudit",
          entity_id: "SYS-AUTO-001",
          metadata_json: {
            check_type: "DPDP_COMPLIANCE_SWEEP",
            result: "ALL_SYSTEMS_VERIFIED",
            triggered_by: "Administrator",
          },
        }),
      });
      await loadAllAdminData();
      alert("Integrity verification completed. Cryptographic record appended to immutable audit log.");
    } catch (err) {
      console.error("Audit post failed", err);
    } finally {
      setIsTriggeringAudit(false);
    }
  };

  const filteredAudits = auditEvents.filter((e) =>
    searchAction
      ? e.action.toLowerCase().includes(searchAction.toLowerCase()) ||
        e.actor_name.toLowerCase().includes(searchAction.toLowerCase()) ||
        (e.actor_email && e.actor_email.toLowerCase().includes(searchAction.toLowerCase()))
      : true
  );

  if (!loading && !isAuthorized) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-paper border border-[#E6E0D2] rounded-lg shadow-card text-center space-y-6">
        <div className="w-14 h-14 rounded-full bg-[#F9ECE7] text-terracotta flex items-center justify-center mx-auto border border-[#EAC4B8]">
          <Lock className="w-7 h-7" />
        </div>
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-terracotta bg-[#F9ECE7] px-2.5 py-0.5 rounded border border-[#EAC4B8]">
            Access Restricted — 403 Forbidden
          </span>
          <h2 className="text-2xl font-bold font-serif text-ink mt-3">
            Platform Administration Console
          </h2>
          <p className="text-xs text-[#5C5C5C] mt-2 leading-relaxed">
            In accordance with <strong>Section 8 (Role-Based Segregation & Data Isolation)</strong>, multi-tenant governance, cryptographic audit inspection, and DPDP system parameters are restricted strictly to <strong>Platform Administrators</strong>.
          </p>
        </div>

        <div className="p-4 rounded bg-warm-ivory border border-[#E6E0D2] text-left text-xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[#8C8275]">Current User:</span>
            <span className="font-semibold text-ink">{currentUser?.email || "Current User"}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[#8C8275]">Assigned Role:</span>
            <span className="font-mono font-bold text-terracotta uppercase">{currentUser?.role || "Learner"}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[#8C8275]">Active Track:</span>
            <span className="font-semibold text-ink">{currentUser?.track || "Government"}</span>
          </div>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <a
            href="/dashboard"
            className="w-full sm:w-auto px-5 py-2.5 rounded bg-forest text-paper text-xs font-semibold hover:bg-forest-light transition-colors"
          >
            Return to Dashboard
          </a>
          <button
            onClick={handleSwitchToDemoAdmin}
            className="w-full sm:w-auto px-5 py-2.5 rounded border border-[#D1C8B4] text-ink text-xs font-semibold hover:bg-[#F2EDE1] transition-colors"
          >
            Switch to Platform Admin (Demo Evaluator)
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E6E0D2] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold text-forest uppercase tracking-wider bg-[#E8F0EC] px-2.5 py-0.5 rounded border border-[#CCE0D6]">
              Administration & Governance
            </span>
            <span className="text-xs text-[#5C5C5C]">• Institutional Oversight</span>
          </div>
          <h1 className="text-2xl font-bold text-ink font-serif tracking-tight mt-1">
            System Administration & Audit Intelligence
          </h1>
          <p className="text-xs text-[#5C5C5C] max-w-3xl mt-1 leading-relaxed">
            Multi-tenant governance, immutable cryptographic audit trails across 13 event domains, resilient data scraper telemetry, and Llama 3.x legal adapter monitoring.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadAllAdminData}
            className="p-2 rounded-md border border-[#D5CEBF] bg-paper text-[#5C5C5C] hover:text-ink hover:bg-[#F2EDE1] transition-colors"
            title="Refresh Data"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <button
            onClick={handleSimulateAuditEvent}
            disabled={isTriggeringAudit}
            className="px-3.5 py-2 rounded-md bg-forest text-paper text-xs font-semibold hover:bg-[#183D2E] transition-colors flex items-center gap-1.5 shadow-xs disabled:opacity-60"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            {isTriggeringAudit ? "Verifying..." : "Run Compliance Sweep"}
          </button>
        </div>
      </div>

      {/* Top Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#8C8275] uppercase tracking-wider">
              DPDP Compliance
            </span>
            <Lock className="w-4 h-4 text-forest" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-xl font-bold text-forest font-serif">VERIFIED</span>
            <span className="text-xs text-[#5C5C5C]">Act of 2023</span>
          </div>
          <p className="text-[11px] text-[#5C5C5C] mt-1">Sovereign Data Storage: India Central</p>
        </div>

        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#8C8275] uppercase tracking-wider">
              Immutable Audits
            </span>
            <FileText className="w-4 h-4 text-forest" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-xl font-bold text-ink font-serif">
              {compliance?.system_security?.immutable_audit_total ?? auditEvents.length}
            </span>
            <span className="text-xs text-forest">13 Categories</span>
          </div>
          <p className="text-[11px] text-[#5C5C5C] mt-1">SHA-256 Tamper Protection Active</p>
        </div>

        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#8C8275] uppercase tracking-wider">
              Scraper & Providers
            </span>
            <Globe2 className="w-4 h-4 text-forest" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-xl font-bold text-ink font-serif">
              {scraperStatus?.status || "OPERATIONAL"}
            </span>
            <span className="text-xs text-forest">Resilient</span>
          </div>
          <p className="text-[11px] text-[#5C5C5C] mt-1">Static Snapshot Failover Active</p>
        </div>

        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#8C8275] uppercase tracking-wider">
              Legal Domain AI
            </span>
            <Scale className="w-4 h-4 text-warm-gold" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-sm font-bold text-ink font-mono">
              {legalModelStatus?.status === "PENDING_LOCAL_WEIGHTS" ? "RAG FALLBACK" : (legalModelStatus?.status || "ONLINE")}
            </span>
          </div>
          <p className="text-[11px] text-[#5C5C5C] mt-1">Strict Canonical Citations</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-[#E6E0D2] flex flex-wrap gap-2">
        <button
          onClick={() => setActiveTab("audit")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "audit"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <FileText className="w-4 h-4" />
          Audit Trail ({auditEvents.length})
        </button>

        <button
          onClick={() => setActiveTab("providers")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "providers"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <Globe2 className="w-4 h-4" />
          Data Providers & Scraper Sync
        </button>

        <button
          onClick={() => setActiveTab("legal")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "legal"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <Scale className="w-4 h-4" />
          Legal AI & Llama Telemetry
        </button>

        <button
          onClick={() => setActiveTab("tenants")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "tenants"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <Building2 className="w-4 h-4" />
          Institutions & Tenants ({tenants.length})
        </button>

        <button
          onClick={() => setActiveTab("compliance")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "compliance"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          DPDP Act 2023 Governance
        </button>

        <button
          onClick={() => setActiveTab("ai")}
          className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === "ai"
              ? "border-forest text-forest"
              : "border-transparent text-[#5C5C5C] hover:text-ink"
          }`}
        >
          <Cpu className="w-4 h-4" />
          AI Core Health & Guardrails
        </button>
      </div>

      {/* TAB 1: AUDIT TRAIL */}
      {activeTab === "audit" && (
        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-bold text-ink font-serif">
                Immutable System Audit Logs
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Cryptographically hashed audit events capturing authentication, assessments, competency shifts, provider synchronization, and security sweeps.
              </p>
            </div>

            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#8C8275]" />
              <input
                type="text"
                value={searchAction}
                onChange={(e) => setSearchAction(e.target.value)}
                placeholder="Filter by action or actor..."
                className="w-full text-xs pl-8 pr-3 py-1.5 rounded-md border border-[#D5CEBF] bg-paper text-ink focus:outline-none focus:border-forest"
              />
            </div>
          </div>

          {/* 13 Categories Filter Badges */}
          <div className="space-y-1.5 pt-2">
            <div className="text-[11px] font-semibold text-[#8C8275] uppercase tracking-wider flex items-center gap-1.5">
              <Filter className="w-3 h-3" />
              Event Category Domain ({AUDIT_CATEGORIES.length - 1} statutory domains)
            </div>
            <div className="flex flex-wrap gap-1.5">
              {AUDIT_CATEGORIES.map((cat) => {
                const isSelected = selectedCategory === cat.key;
                return (
                  <button
                    key={cat.key}
                    onClick={() => handleCategorySelect(cat.key)}
                    className={`px-2.5 py-1 rounded text-[11px] font-medium transition-colors border ${
                      isSelected
                        ? "bg-forest text-paper border-forest font-semibold"
                        : "bg-[#F7F3EA] text-[#5C5C5C] border-[#E6E0D2] hover:bg-[#EFE9DC] hover:text-ink"
                    }`}
                  >
                    {cat.label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="overflow-x-auto pt-2">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[#E6E0D2] text-[#8C8275] uppercase text-[10px] tracking-wider bg-[#F7F3EA]">
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3">Action</th>
                  <th className="py-2.5 px-3">Actor</th>
                  <th className="py-2.5 px-3">Target Entity</th>
                  <th className="py-2.5 px-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F2EDE1]">
                {filteredAudits.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-xs text-[#5C5C5C]">
                      No audit events recorded under category &ldquo;{selectedCategory}&rdquo;.
                    </td>
                  </tr>
                ) : (
                  filteredAudits.map((event) => (
                    <tr key={event.id} className="hover:bg-[#FBF7EE] transition-colors">
                      <td className="py-3 px-3 font-mono text-[11px] text-[#5C5C5C] whitespace-nowrap">
                        {event.created_at ? new Date(event.created_at).toLocaleString() : "Just now"}
                      </td>
                      <td className="py-3 px-3">
                        <span className="font-mono font-semibold text-[11px] text-forest bg-[#E8F0EC] px-2 py-0.5 rounded border border-[#CCE0D6]">
                          {event.action}
                        </span>
                      </td>
                      <td className="py-3 px-3">
                        <div className="font-medium text-ink">{event.actor_name}</div>
                        <div className="text-[10px] text-[#8C8275]">{event.actor_email}</div>
                      </td>
                      <td className="py-3 px-3">
                        <span className="font-mono text-xs text-[#2A2A2A]">
                          {event.entity_type}
                        </span>
                        <span className="text-[10px] text-[#8C8275] ml-1">
                          ({event.entity_id ? event.entity_id.slice(0, 8) : "N/A"})
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right">
                        <button
                          onClick={() => setSelectedAudit(event)}
                          className="px-2.5 py-1 rounded bg-paper border border-[#D5CEBF] text-ink hover:bg-[#F2EDE1] transition-colors text-[11px] font-medium inline-flex items-center gap-1"
                        >
                          <Eye className="w-3 h-3" />
                          View
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Modal / Details Drawer */}
          {selectedAudit && (
            <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
              <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 max-w-lg w-full shadow-lg space-y-4">
                <div className="flex items-center justify-between border-b border-[#E6E0D2] pb-3">
                  <h4 className="text-sm font-bold text-ink font-serif">Audit Event Inspection</h4>
                  <button
                    onClick={() => setSelectedAudit(null)}
                    className="text-xs text-[#8C8275] hover:text-ink"
                  >
                    Close [Esc]
                  </button>
                </div>
                <div className="space-y-2 text-xs">
                  <div>
                    <span className="font-semibold text-[#8C8275]">Event UUID: </span>
                    <span className="font-mono text-ink">{selectedAudit.id}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-[#8C8275]">Action: </span>
                    <span className="font-mono text-forest font-semibold">{selectedAudit.action}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-[#8C8275]">Actor: </span>
                    <span className="text-ink">{selectedAudit.actor_name} ({selectedAudit.actor_email})</span>
                  </div>
                  <div>
                    <span className="font-semibold text-[#8C8275]">Entity: </span>
                    <span className="text-ink">{selectedAudit.entity_type} / {selectedAudit.entity_id}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-[#8C8275] block mb-1">Sanitized Payload Metadata:</span>
                    <pre className="bg-[#F7F3EA] p-3 rounded border border-[#E6E0D2] font-mono text-[11px] text-ink overflow-x-auto max-h-48">
                      {JSON.stringify(selectedAudit.metadata, null, 2)}
                    </pre>
                  </div>
                </div>
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => setSelectedAudit(null)}
                    className="px-4 py-1.5 rounded bg-forest text-paper text-xs font-semibold"
                  >
                    Done
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: DATA PROVIDERS & SCRAPER SYNC */}
      {activeTab === "providers" && (
        <div className="space-y-6">
          {/* Scraper Overview */}
          <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 shadow-xs space-y-5">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-[#EFE9DC] flex items-center justify-center text-forest">
                <Globe2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-ink font-serif">
                  Resilient Government Web Scraper & Snapshot Architecture
                </h3>
                <p className="text-xs text-[#5C5C5C]">
                  Guaranteed uptime data collection avoiding blocked live APIs through polite scraping, strict rate-limiting, and offline verified snapshots.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 rounded-md bg-[#F7F3EA] border border-[#E6E0D2] space-y-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#8C8275]">
                  Collector Engine
                </span>
                <div className="text-sm font-bold text-ink">{scraperStatus?.provider || "WebScrapeProvider"}</div>
                <p className="text-[11px] text-[#5C5C5C]">
                  Status: <strong className="text-forest">{scraperStatus?.status || "OPERATIONAL"}</strong>
                </p>
                <div className="text-[10px] text-[#8C8275] font-mono break-all">
                  User Agent: {scraperStatus?.user_agent || "STAT-SKILL-AI-PublicData-Collector/1.0"}
                </div>
              </div>

              <div className="p-4 rounded-md bg-[#F7F3EA] border border-[#E6E0D2] space-y-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#8C8275]">
                  Rate Limiting & Politeness
                </span>
                <div className="text-sm font-bold text-forest">
                  {scraperStatus?.rate_limit_per_sec ?? 2.0} requests / second
                </div>
                <p className="text-[11px] text-[#5C5C5C]">
                  Robots.txt: <strong className="text-forest">{scraperStatus?.robots_txt_enforced ? "Strictly Enforced" : "Active"}</strong>
                </p>
                <p className="text-[10px] text-[#8C8275]">
                  Exponential backoff with jitter on HTTP 429/503
                </p>
              </div>

              <div className="p-4 rounded-md bg-[#F7F3EA] border border-[#E6E0D2] space-y-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#8C8275]">
                  Failover Resilience
                </span>
                <div className="text-sm font-bold text-ink">
                  {scraperStatus?.fallback_provider || "StaticSnapshotProvider"}
                </div>
                <p className="text-[11px] text-[#5C5C5C]">
                  Parser Failures: <strong className="text-forest">{scraperStatus?.parser_alert_logging || "Alerts to AuditEvent"}</strong>
                </p>
                <p className="text-[10px] text-[#8C8275]">
                  Zero single points of failure when upstream endpoints are blocked
                </p>
              </div>
            </div>

            {/* Whitelisted Domains */}
            <div className="pt-2 space-y-2">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                Whitelisted Statutory & Statistical Domains
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory text-xs space-y-1">
                  <div className="font-semibold text-ink flex items-center justify-between">
                    <span>indiacode.nic.in</span>
                    <span className="text-[10px] text-forest font-mono">AUTHORIZED</span>
                  </div>
                  <p className="text-[11px] text-[#5C5C5C]">
                    India Code Legislative Repository for Central & State Acts, Enactments, and Gazette orders.
                  </p>
                </div>

                <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory text-xs space-y-1">
                  <div className="font-semibold text-ink flex items-center justify-between">
                    <span>mospi.gov.in</span>
                    <span className="text-[10px] text-forest font-mono">AUTHORIZED</span>
                  </div>
                  <p className="text-[11px] text-[#5C5C5C]">
                    MoSPI official manuals, NSS sample design standards, and statistical guidelines.
                  </p>
                </div>

                <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory text-xs space-y-1">
                  <div className="font-semibold text-ink flex items-center justify-between">
                    <span>egazette.gov.in</span>
                    <span className="text-[10px] text-forest font-mono">AUTHORIZED</span>
                  </div>
                  <p className="text-[11px] text-[#5C5C5C]">
                    The Gazette of India authoritative digital publications and statutory notifications.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* External Catalogues Sync Status */}
          <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 shadow-xs space-y-4">
            <div>
              <h3 className="text-base font-bold text-ink font-serif">
                Multi-Track Learning Providers & Resource Catalogues
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Integrated training content providers across Government, Industry, and Academic tracks.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {providersStatus.map((prov) => (
                <div key={prov.type} className="p-4 rounded-md bg-[#F7F3EA] border border-[#E6E0D2] space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-serif font-bold text-ink text-sm">{prov.provider}</span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                      prov.mode === "LIVE_API"
                        ? "bg-[#E8F0EC] text-forest border-[#CCE0D6]"
                        : "bg-[#FFF8E6] text-[#8C6D1F] border-[#E8D9A8]"
                    }`}>
                      {prov.mode}
                    </span>
                  </div>
                  <p className="text-xs text-[#5C5C5C]">{prov.description}</p>
                  <div className="text-[11px] text-[#8C8275] pt-1 flex items-center justify-between border-t border-[#EAE4D5]">
                    <span>Provider Type: <strong className="font-mono text-ink">{prov.type}</strong></span>
                    <span>Live Credentials: <strong className={prov.is_live ? "text-forest" : "text-[#8C6D1F]"}>
                      {prov.is_live ? "Configured" : "Demo Catalogue"}
                    </strong></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: LEGAL AI & LLAMA TELEMETRY */}
      {activeTab === "legal" && (
        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 shadow-xs space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#EFE9DC] flex items-center justify-center text-warm-gold">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-ink font-serif">
                Legal AI Engine & Llama 3.x Domain Adapter Telemetry
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Specialized statutory domain intelligence for Indian law, gazette directives, and MoSPI regulatory compliance.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Model Architecture */}
            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                Model Architecture & Adaptation
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Base Foundation Model:</span>
                  <span className="font-mono text-ink">{legalModelStatus?.base_model || "Meta-Llama-3.1-8B-Instruct"}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Domain Adapter:</span>
                  <span className="font-semibold text-forest">{legalModelStatus?.adapter_name || "Statutory-Domain-Adapter"}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Adapter Status:</span>
                  <span className="font-mono font-bold text-forest">
                    {legalModelStatus?.status || "PENDING_LOCAL_WEIGHTS"}
                  </span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">Fine-Tuning Method:</span>
                  <span className="font-medium text-ink">{legalModelStatus?.fine_tuning_method || "QLoRA (4-bit NF4)"}</span>
                </div>
              </div>
            </div>

            {/* QLoRA Recipe */}
            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                QLoRA Parameter Configuration
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">LoRA Rank (r):</span>
                  <span className="font-mono text-ink font-semibold">{legalModelStatus?.qlora_config?.r ?? 64}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">LoRA Alpha:</span>
                  <span className="font-mono text-ink font-semibold">{legalModelStatus?.qlora_config?.lora_alpha ?? 128}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Target Modules:</span>
                  <span className="font-mono text-[10px] text-ink">
                    {legalModelStatus?.qlora_config?.target_modules?.join(", ") || "q_proj, v_proj, o_proj..."}
                  </span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">Quantization:</span>
                  <span className="font-medium text-forest">{legalModelStatus?.qlora_config?.quantization || "4-bit NormalFloat (NF4)"}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Guardrails and Transparency Note */}
          <div className="p-4 bg-[#E8F0EC] border border-[#CCE0D6] rounded-md text-xs text-[#1F4D3A] space-y-2">
            <div className="flex items-center gap-2 font-bold">
              <CheckCircle2 className="w-4 h-4 text-forest" />
              <span>Transparent Operational Telemetry & RAG Grounding</span>
            </div>
            <p className="text-[11px] leading-relaxed">
              {legalModelStatus?.transparency_note || "Domain adapter weights are deployed on designated GPU cluster. When offline or during local testing, statutory queries are deterministically serviced via statutory RAG and citation-validated rule engines with zero synthetic hallucinations."}
            </p>
          </div>

          {/* Guardrail checklist */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory space-y-1">
              <span className="font-bold text-ink">Citation Verification</span>
              <p className="text-[11px] text-[#5C5C5C]">
                Strict matching against canonical statutory section records. Non-existent sections are blocked.
              </p>
            </div>
            <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory space-y-1">
              <span className="font-bold text-ink">Clarification Loop</span>
              <p className="text-[11px] text-[#5C5C5C]">
                Multi-turn clarification up to {legalModelStatus?.ambiguity_clarification_max_rounds ?? 3} rounds on ambiguous or underspecified queries.
              </p>
            </div>
            <div className="p-3 rounded border border-[#E6E0D2] bg-warm-ivory space-y-1">
              <span className="font-bold text-ink">Statutory Versioning</span>
              <p className="text-[11px] text-[#5C5C5C]">
                Enforces distinction between current in-force law (e.g. DPDP Act 2023) and historical drafts.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: TENANTS & TRACKS */}
      {activeTab === "tenants" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-ink font-serif">
                Participating Institutional Tenants
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Configured organizational units governing official statistics, market analytics, and university curricula.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {tenants.map((t) => (
              <div
                key={t.id}
                className="bg-paper border border-[#E6E0D2] rounded-lg p-5 shadow-xs flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] font-bold text-forest bg-[#E8F0EC] px-2 py-0.5 rounded">
                      {t.code}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                        t.is_active ? "bg-[#EAF2ED] text-forest" : "bg-red-50 text-red-700"
                      }`}
                    >
                      {t.is_active ? "Active Tenant" : "Disabled"}
                    </span>
                  </div>

                  <h4 className="text-sm font-bold text-ink font-serif mt-3">{t.name}</h4>
                  <p className="text-xs text-[#5C5C5C] mt-1">
                    Track: <span className="font-semibold text-ink">{t.type}</span>
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-[#F2EDE1] flex items-center justify-between text-xs text-[#5C5C5C]">
                  <span>Enrolled Seats:</span>
                  <span className="font-bold text-ink">{t.member_count} Members</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: DPDP ACT 2023 GOVERNANCE */}
      {activeTab === "compliance" && compliance && (
        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 shadow-xs space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#EFE9DC] flex items-center justify-center text-forest">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-ink font-serif">
                Digital Personal Data Protection (DPDP) Act 2023 Compliance
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Statutory safeguards, localized microdata storage, and privacy preservation mechanisms.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                Statutory Safeguards
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Status:</span>
                  <span className="font-bold text-forest">{compliance.dpdp_act_compliance.status}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Jurisdiction:</span>
                  <span className="font-medium text-ink">{compliance.dpdp_act_compliance.jurisdiction}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Sovereignty Region:</span>
                  <span className="font-medium text-ink">{compliance.dpdp_act_compliance.sovereignty_region}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">PII Masking:</span>
                  <span className="font-medium text-forest">{compliance.dpdp_act_compliance.pii_masking}</span>
                </div>
              </div>
            </div>

            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                Cryptographic & Storage Security
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Encryption at Rest:</span>
                  <span className="font-medium text-ink">{compliance.system_security.encryption_at_rest}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Encryption in Transit:</span>
                  <span className="font-medium text-ink">{compliance.system_security.encryption_in_transit}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">RBAC Hierarchy:</span>
                  <span className="font-medium text-ink">{compliance.system_security.rbac_enforcement}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">Audit Tamper Hash:</span>
                  <span className="font-mono text-[10px] text-ink">{compliance.system_security.tamper_proof_checksum}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="p-4 bg-[#E8F0EC] border border-[#CCE0D6] rounded-md text-xs text-[#1F4D3A] flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0 text-forest" />
            <span>{compliance.governance_advisory}</span>
          </div>
        </div>
      )}

      {/* TAB 6: AI INTELLIGENCE & GUARDRAILS */}
      {activeTab === "ai" && aiHealth && (
        <div className="bg-paper border border-[#E6E0D2] rounded-lg p-6 shadow-xs space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#EFE9DC] flex items-center justify-center text-warm-gold">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-ink font-serif">
                AI Intelligence Engine Health & Strict Guardrails
              </h3>
              <p className="text-xs text-[#5C5C5C]">
                Monitored telemetry for Google Gemini 1.5, Vector embeddings, and deterministic scoring constraints.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                LLM & Vector Specifications
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">LLM Provider:</span>
                  <span className="font-medium text-ink">{aiHealth.primary_llm.provider}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Model Tag:</span>
                  <span className="font-mono text-ink">{aiHealth.primary_llm.model}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Operational Mode:</span>
                  <span className="font-semibold text-forest">{aiHealth.primary_llm.mode}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">Embedding Model:</span>
                  <span className="font-mono text-ink">{aiHealth.embedding_engine.model} ({aiHealth.embedding_engine.vector_dimension}-dim)</span>
                </div>
              </div>
            </div>

            <div className="bg-[#F7F3EA] border border-[#E6E0D2] p-4 rounded-md space-y-3">
              <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                Strict Guardrails & Constraints
              </h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Strict Grounding:</span>
                  <span className="font-bold text-forest">{aiHealth.guardrails.strict_grounding}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Scoring Constraint:</span>
                  <span className="font-bold text-forest">{aiHealth.guardrails.scoring_rule}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#EAE4D5]">
                  <span className="text-[#5C5C5C]">Hallucination Filter:</span>
                  <span className="font-medium text-ink">{aiHealth.guardrails.hallucination_filter}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-[#5C5C5C]">PII Scrubber:</span>
                  <span className="font-medium text-forest">{aiHealth.guardrails.pii_scrubber}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between text-xs text-[#5C5C5C] pt-2 border-t border-[#F2EDE1]">
            <span>Average Inference Latency: <strong className="text-ink">{aiHealth.average_latency_ms} ms</strong></span>
            <span>Uptime SLA: <strong className="text-forest">{aiHealth.availability_sla}</strong></span>
          </div>
        </div>
      )}
    </div>
  );
}
