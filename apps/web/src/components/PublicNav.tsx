"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, ArrowRight, Menu, X, Building2, Briefcase, GraduationCap } from "lucide-react";
import { getStoredUser, StoredUser } from "@/lib/api";

export default function PublicNav() {
  const pathname = usePathname();
  const [user, setUser] = useState<StoredUser | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const navLinks = [
    { label: "Overview", href: "/" },
    { label: "How It Works", href: "/how-it-works" },
    { label: "Government", href: "/government" },
    { label: "Industry", href: "/industry" },
    { label: "Academia", href: "/academia" },
    { label: "Features", href: "/features" },
    { label: "Legal AI", href: "/legal-intelligence" },
    { label: "FAQ", href: "/faq" },
  ];

  return (
    <nav className="glass-nav sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-3.5 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded bg-forest flex items-center justify-center text-paper font-serif font-bold text-lg shadow-xs group-hover:bg-forest-light transition-colors">
            S
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-serif font-bold text-lg text-ink tracking-tight">
                STAT-SKILL AI
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#EBF3ED] text-forest border border-[#C7DEC9]">
                Enterprise Edition
              </span>
            </div>
            <p className="text-[10px] text-[#8C8275] tracking-wide font-sans">
              Ministry of Statistics & Programme Implementation (MoSPI / DIID)
            </p>
          </div>
        </Link>

        {/* Desktop Links */}
        <div className="hidden lg:flex items-center gap-1">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`text-xs font-medium px-3 py-1.5 rounded transition-colors ${
                  isActive
                    ? "bg-[#EBF3ED] text-forest font-semibold border border-[#C7DEC9]"
                    : "text-[#4A4A4A] hover:text-ink hover:bg-[#F2EDE1]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Right CTA / Auth Status */}
        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <Link
              href="/dashboard"
              className="text-xs font-semibold px-4 py-2 rounded bg-forest text-paper hover:bg-forest-light transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <span>Go to Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          ) : (
            <>
              <Link
                href="/login"
                className="text-xs font-semibold px-4 py-2 rounded border border-[#D1C8B4] text-ink hover:bg-[#F2EDE1] transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="text-xs font-semibold px-4 py-2 rounded bg-forest text-paper hover:bg-forest-light transition-colors flex items-center gap-1.5 shadow-xs"
              >
                <span>Get Started</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </>
          )}
        </div>

        {/* Mobile menu toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-2 rounded text-ink hover:bg-[#F2EDE1]"
          aria-label="Toggle Menu"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-[#E6E0D2] bg-paper px-6 py-4 space-y-3">
          <div className="space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`block text-xs font-medium px-3 py-2 rounded ${
                  pathname === link.href
                    ? "bg-[#EBF3ED] text-forest font-semibold"
                    : "text-[#4A4A4A] hover:bg-[#F2EDE1]"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="pt-3 border-t border-[#E6E0D2] flex flex-col gap-2">
            {user ? (
              <Link
                href="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full text-center text-xs font-semibold py-2.5 rounded bg-forest text-paper"
              >
                Go to Workspace
              </Link>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center text-xs font-semibold py-2 rounded border border-[#D1C8B4] text-ink"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center text-xs font-semibold py-2 rounded bg-forest text-paper"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
