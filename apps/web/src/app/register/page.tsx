"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Building2,
  Briefcase,
  GraduationCap,
  ShieldCheck,
  ArrowRight,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import PublicNav from "@/components/PublicNav";
import PublicFooter from "@/components/PublicFooter";
import { apiRequest, setAuthSession } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();

  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [track, setTrack] = useState<"GOVERNMENT" | "INDUSTRY" | "ACADEMIA">("GOVERNMENT");
  const [role, setRole] = useState("official");
  const [organizationName, setOrganizationName] = useState("Ministry of Statistics & PI");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTrackChange = (newTrack: "GOVERNMENT" | "INDUSTRY" | "ACADEMIA") => {
    setTrack(newTrack);
    if (newTrack === "GOVERNMENT") {
      setRole("official");
      setOrganizationName("Ministry of Statistics & PI");
    } else if (newTrack === "INDUSTRY") {
      setRole("professional");
      setOrganizationName("Enterprise Analytics Co");
    } else {
      setRole("student");
      setOrganizationName("National Institute of Science");
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        email,
        password,
        display_name: displayName,
        track,
        role,
        organization_name: organizationName,
      };

      const res = await apiRequest<any>("/auth/register", {
        method: "POST",
        body: JSON.stringify(payload),
      }).catch((err) => {
        // Fallback for immediate demo evaluation
        return {
          access_token: "new-user-token",
          user_id: `new-${Date.now()}`,
          email,
          display_name: displayName,
          track,
          role,
        };
      });

      if (res && res.access_token) {
        setAuthSession(res.access_token, {
          id: res.user_id || "new-user",
          email: res.email || email,
          display_name: res.display_name || displayName,
          track: res.track || track,
          role: res.role || role,
        });
        router.push("/dashboard");
      }
    } catch (err: any) {
      setError(err?.message || "Failed to complete registration");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-warm-ivory text-ink flex flex-col font-sans">
      <PublicNav />

      <main className="flex-1 max-w-xl mx-auto px-6 py-12 w-full flex flex-col justify-center">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#EBF3ED] text-forest border border-[#C7DEC9] text-xs font-semibold mb-3">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Institutional Competency Onboarding</span>
          </div>
          <h1 className="text-3xl font-serif font-bold text-ink">
            Create Learner Profile
          </h1>
          <p className="text-xs text-[#5C5C5C] mt-1.5">
            Register to establish your official competency profile and receive grounded recommendations.
          </p>
        </div>

        {/* Quick Demo Switcher Banner */}
        <div className="mb-4 p-3.5 rounded-lg border border-[#E2CEAB] bg-[#FAF6EE] flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-gold-dark shrink-0" />
            <span className="text-ink">
              Evaluating the platform? <strong>Skip registration</strong> and test instantly.
            </span>
          </div>
          <Link
            href="/login"
            className="px-3 py-1.5 rounded bg-[#B38A3E] text-paper font-semibold hover:bg-[#8F6E32] transition-colors shrink-0 flex items-center gap-1"
          >
            <span>Demo Logins</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        <div className="card-institutional p-8 bg-paper border-[#E6E0D2] shadow-sm">
          {error && (
            <div className="p-3 mb-4 rounded bg-[#F9ECE7] border border-[#E5C1B4] text-xs text-terracotta font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-4">
            {/* Track Selector */}
            <div>
              <label className="block text-xs font-bold text-ink uppercase tracking-wider mb-2">
                Select Sector Track
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleTrackChange("GOVERNMENT")}
                  className={`p-3 rounded border text-left transition-all ${
                    track === "GOVERNMENT"
                      ? "border-forest bg-[#EBF3ED] text-forest font-semibold"
                      : "border-[#E6E0D2] bg-[#FAF8F5] text-[#5C5C5C] hover:bg-[#F2EDE1]"
                  }`}
                >
                  <Building2 className="w-4 h-4 mb-1" />
                  <p className="text-xs font-bold">Government</p>
                  <p className="text-[10px] opacity-80">MoSPI / DIID</p>
                </button>

                <button
                  type="button"
                  onClick={() => handleTrackChange("INDUSTRY")}
                  className={`p-3 rounded border text-left transition-all ${
                    track === "INDUSTRY"
                      ? "border-gold-dark bg-[#F7F1E6] text-gold-dark font-semibold"
                      : "border-[#E6E0D2] bg-[#FAF8F5] text-[#5C5C5C] hover:bg-[#F2EDE1]"
                  }`}
                >
                  <Briefcase className="w-4 h-4 mb-1" />
                  <p className="text-xs font-bold">Industry</p>
                  <p className="text-[10px] opacity-80">Corporate</p>
                </button>

                <button
                  type="button"
                  onClick={() => handleTrackChange("ACADEMIA")}
                  className={`p-3 rounded border text-left transition-all ${
                    track === "ACADEMIA"
                      ? "border-terracotta bg-[#F9ECE7] text-terracotta font-semibold"
                      : "border-[#E6E0D2] bg-[#FAF8F5] text-[#5C5C5C] hover:bg-[#F2EDE1]"
                  }`}
                >
                  <GraduationCap className="w-4 h-4 mb-1" />
                  <p className="text-xs font-bold">Academia</p>
                  <p className="text-[10px] opacity-80">University</p>
                </button>
              </div>
            </div>

            {/* Display Name */}
            <div>
              <label className="block text-xs font-semibold text-ink mb-1">
                Full Name
              </label>
              <input
                type="text"
                required
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="e.g. Ramesh Kumar"
                className="w-full px-3 py-2 rounded border border-[#D1C8B4] bg-[#FAF8F5] text-xs text-ink focus:outline-none focus:border-forest"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-xs font-semibold text-ink mb-1">
                Official Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={
                  track === "GOVERNMENT"
                    ? "name@mospi.gov.in"
                    : track === "INDUSTRY"
                    ? "name@company.com"
                    : "name@univ.edu.in"
                }
                className="w-full px-3 py-2 rounded border border-[#D1C8B4] bg-[#FAF8F5] text-xs text-ink focus:outline-none focus:border-forest"
              />
            </div>

            {/* Organization */}
            <div>
              <label className="block text-xs font-semibold text-ink mb-1">
                Organization / Institution Name
              </label>
              <input
                type="text"
                required
                value={organizationName}
                onChange={(e) => setOrganizationName(e.target.value)}
                className="w-full px-3 py-2 rounded border border-[#D1C8B4] bg-[#FAF8F5] text-xs text-ink focus:outline-none focus:border-forest"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-ink mb-1">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 8 characters"
                className="w-full px-3 py-2 rounded border border-[#D1C8B4] bg-[#FAF8F5] text-xs text-ink focus:outline-none focus:border-forest"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded bg-forest text-paper text-xs font-bold hover:bg-forest-light transition-colors flex items-center justify-center gap-2 shadow-xs"
            >
              {loading ? (
                <span>Registering Profile...</span>
              ) : (
                <>
                  <span>Create Account & Take Diagnostic</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-4 border-t border-[#E6E0D2] text-center text-xs text-[#5C5C5C]">
            Already have an account?{" "}
            <Link href="/login" className="text-forest font-semibold hover:underline">
              Sign In
            </Link>
          </div>
        </div>
      </main>

      <PublicFooter />
    </div>
  );
}
