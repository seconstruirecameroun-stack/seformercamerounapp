/**
 * Types de la base, écrits à la main pour le lot 0.
 *
 * À remplacer par la génération automatique dès que la CLI Supabase est
 * installée :
 *   npx supabase gen types typescript --project-id hhwqdvweppcosggtptvz > src/types/db.ts
 */

export type Json = string | number | boolean | null | { [k: string]: Json } | Json[];

export type Subsystem = 'francophone' | 'anglophone';
export type ContentStatus = 'pending' | 'approved' | 'rejected';
export type MediaStatus =
  | 'queued'
  | 'script_ready'
  | 'rendering'
  | 'ready'
  | 'published'
  | 'failed';
export type NotionKind = 'definition' | 'date' | 'liste' | 'relation';
export type ExplainRegister = 'simple' | 'analogie' | 'histoire' | 'visuel' | 'pas_a_pas';
export type ItemKind =
  | 'qcm'
  | 'association'
  | 'chronologie'
  | 'texte_a_trous'
  | 'vrai_faux'
  | 'restitution_audio'
  | 'defi_chrono';

export interface ClassRow {
  id: string;
  subsystem: Subsystem;
  code: string;
  rank: number;
}

export interface ChildRow {
  id: string;
  parent_id: string;
  first_name: string;
  class_id: string | null;
  avatar: string | null;
  created_at: string;
}

export interface SubjectRow {
  id: string;
  parent_id: string;
  label: string;
  color: string | null;
  created_at: string;
}

export interface LessonRow {
  id: string;
  parent_id: string;
  document_id: string | null;
  subject_id: string | null;
  class_id: string | null;
  title: string;
  summary: string | null;
  lang: string;
  chapter: string | null;
  sort_order: number;
  status: ContentStatus;
  created_at: string;
}

export interface NotionRow {
  id: string;
  parent_id: string;
  lesson_id: string;
  kind: NotionKind;
  statement: string;
  sort_order: number;
  status: ContentStatus;
  created_at: string;
}

export interface ExplanationRow {
  id: string;
  parent_id: string;
  notion_id: string;
  register: ExplainRegister;
  body: string;
  status: ContentStatus;
  created_at: string;
}

/** payload et answer dépendent de kind : voir les gardes dans lib/items.ts */
export interface ItemRow {
  id: string;
  parent_id: string;
  notion_id: string;
  kind: ItemKind;
  level: number;
  payload: Json;
  answer: Json;
  explain: string | null;
  status: ContentStatus;
  created_at: string;
}

export interface VideoRow {
  id: string;
  parent_id: string;
  lesson_id: string;
  manifest: Json;
  voice_preset: string | null;
  storage_path: string | null;
  external_url: string | null;
  poster_url: string | null;
  duration_s: number | null;
  status: MediaStatus;
  created_at: string;
}

export interface LessonProgressRow {
  child_id: string;
  lesson_id: string;
  parent_id: string;
  seen_at: string | null;
  completed_at: string | null;
}

export interface MasteryRow {
  child_id: string;
  notion_id: string;
  parent_id: string;
  level: number;
  score: number;
  streak: number;
  next_review: string | null;
  updated_at: string;
}

export interface AttemptRow {
  id: number;
  parent_id: string;
  child_id: string;
  item_id: string;
  answer: Json;
  correct: boolean;
  duration_ms: number | null;
  created_at: string;
}

export interface RewardRow {
  id: string;
  parent_id: string;
  child_id: string;
  kind: string;
  value: number;
  created_at: string;
}

export interface ParentSettingsRow {
  parent_id: string;
  interface_lang: string;
  generation_quota: number;
  video_quota: number;
  created_at: string;
}

type Table<Row> = {
  Row: Row;
  Insert: Partial<Row>;
  Update: Partial<Row>;
  Relationships: [];
};

export interface Database {
  public: {
    Tables: {
      classes: Table<ClassRow>;
      children: Table<ChildRow>;
      subjects: Table<SubjectRow>;
      lessons: Table<LessonRow>;
      notions: Table<NotionRow>;
      explanations: Table<ExplanationRow>;
      items: Table<ItemRow>;
      videos: Table<VideoRow>;
      lesson_progress: Table<LessonProgressRow>;
      mastery: Table<MasteryRow>;
      attempts: Table<AttemptRow>;
      rewards: Table<RewardRow>;
      parent_settings: Table<ParentSettingsRow>;
    };
    Views: Record<string, never>;
    Functions: {
      seed_demo_prehistoire: { Args: Record<string, never>; Returns: string };
      set_parent_pin: { Args: { new_pin: string }; Returns: undefined };
      verify_parent_pin: { Args: { candidate: string }; Returns: boolean };
      parent_pin_is_set: { Args: Record<string, never>; Returns: boolean };
    };
    Enums: {
      subsystem: Subsystem;
      content_status: ContentStatus;
      media_status: MediaStatus;
      notion_kind: NotionKind;
      explain_register: ExplainRegister;
      item_kind: ItemKind;
    };
    CompositeTypes: Record<string, never>;
  };
}
