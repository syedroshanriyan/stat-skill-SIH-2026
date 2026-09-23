// Core Track Types
export type TrackCode = 'GOVERNMENT' | 'INDUSTRY' | 'ACADEMIA';

export type UserRole =
  | 'learner'
  | 'official'
  | 'student'
  | 'professional'
  | 'org_admin'
  | 'institution_admin'
  | 'platform_admin';

export type OrganizationType = 'GOVERNMENT' | 'INDUSTRY' | 'ACADEMIA';

export interface User {
  id: string;
  email: string;
  display_name: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Profile {
  id: string;
  user_id: string;
  track_id: string;
  designation?: string;
  department?: string;
  education_json?: Record<string, unknown>;
  experience_json?: Record<string, unknown>;
  career_goal?: string;
  target_role_id?: string;
  metadata_json?: Record<string, unknown>;
}

export interface CompetencyFramework {
  id: string;
  track_id: string;
  name: string;
  version: string;
  status: string;
}

export interface Competency {
  id: string;
  framework_id: string;
  parent_id?: string | null;
  code: string;
  name: string;
  category: string;
  description: string;
  level_definitions_json?: Record<string, string>;
}

export interface UserCompetency {
  id?: string;
  user_id: string;
  competency_id: string;
  competency?: Competency;
  score: number; // 0 - 100
  proficiency_level: number; // 1 - 5
  confidence: number; // 0.0 - 1.0
  source: 'diagnostic' | 'quiz' | 'evidence' | 'manual';
  assessed_at: string;
  version: number;
}

export type GapPriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface SkillGap {
  id: string;
  user_id: string;
  competency_id: string;
  competency?: Competency;
  required_level: number;
  current_score: number;
  gap_value: number;
  priority: GapPriority;
  status: 'OPEN' | 'IN_PROGRESS' | 'RESOLVED';
  explanation?: string;
}

export interface LearningResource {
  id: string;
  provider_type: 'igot' | 'nssta' | 'industry' | 'academia';
  provider_external_id: string;
  title: string;
  description: string;
  url: string;
  level: string;
  duration: string;
  metadata_json?: Record<string, unknown>;
  is_demo?: boolean;
}

export interface Recommendation {
  id: string;
  user_id: string;
  resource_id: string;
  resource?: LearningResource;
  competency_id: string;
  competency?: Competency;
  rank: number;
  score: number;
  explanation: string;
  status: 'suggested' | 'saved' | 'started' | 'completed' | 'dismissed';
  generated_at: string;
}

export interface LearningPathItem {
  id: string;
  learning_path_id: string;
  resource_id: string;
  resource?: LearningResource;
  competency_id: string;
  competency?: Competency;
  sequence: number;
  status: 'pending' | 'in_progress' | 'completed' | 'skipped';
}

export interface LearningPath {
  id: string;
  user_id: string;
  title: string;
  goal: string;
  status: 'active' | 'completed' | 'archived';
  items: LearningPathItem[];
}

export interface AssessmentQuestion {
  id: string;
  assessment_id: string;
  competency_id: string;
  competency?: Competency;
  question_type: string;
  difficulty: 'easy' | 'medium' | 'hard';
  prompt: string;
  options_json: string[];
  answer_json: number;
  source_ref?: string;
}

export interface AssessmentAttempt {
  id: string;
  assessment_id: string;
  user_id: string;
  score: number;
  started_at: string;
  completed_at?: string;
}

export interface QuizQuestion {
  id: string;
  quiz_id: string;
  prompt: string;
  options_json: [string, string, string, string];
  correct_option: number;
  explanation: string;
  competency_id: string;
  difficulty: 'easy' | 'medium' | 'hard';
  source_ref: string;
}

export interface Quiz {
  id: string;
  owner_id: string;
  title: string;
  source_document_id?: string;
  competency_id?: string;
  status: 'draft' | 'ready' | 'archived';
  questions?: QuizQuestion[];
}

export interface DocumentRecord {
  id: string;
  user_id: string;
  organization_id?: string;
  filename: string;
  mime_type: string;
  storage_key: string;
  sha256: string;
  status: 'uploaded' | 'processing' | 'indexed' | 'failed';
  chunk_count?: number;
  created_at: string;
}

export type EvidenceStatus =
  | 'submitted'
  | 'ai_analyzed'
  | 'pending_verification'
  | 'verified'
  | 'rejected';

export interface EvidenceRecord {
  id: string;
  user_id: string;
  type: 'project' | 'github' | 'certificate' | 'internship';
  title: string;
  description: string;
  url?: string;
  storage_key?: string;
  status: EvidenceStatus;
  ai_analysis_json?: {
    classification: 'demonstrated' | 'partially demonstrated' | 'not demonstrated' | 'insufficient evidence';
    summary: string;
    detected_competencies: Array<{ code: string; confidence: number; rationale: string }>;
  };
  created_at: string;
}
