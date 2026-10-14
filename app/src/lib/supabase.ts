import { createClient } from '@supabase/supabase-js';

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

if (!url || !key) {
  throw new Error(
    'VITE_SUPABASE_URL et VITE_SUPABASE_PUBLISHABLE_KEY sont absents. ' +
      'Copiez .env.example vers .env et renseignez-les.',
  );
}

/**
 * Client non typé volontairement, pour le lot 0.
 *
 * Les types de tables sont écrits à la main dans types/db.ts et appliqués au
 * cas par cas sur les retours de requête. Brancher ces types à la place des
 * génériques de supabase-js demande le schéma exact que produit la CLI :
 *
 *   npx supabase gen types typescript --project-id hhwqdvweppcosggtptvz \
 *     > src/types/db.ts
 *
 * À faire dès que la CLI est installée, puis repasser createClient<Database>.
 */
export const supabase = createClient(url, key, {
  auth: { persistSession: true, autoRefreshToken: true },
});
