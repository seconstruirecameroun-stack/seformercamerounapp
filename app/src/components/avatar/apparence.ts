/**
 * L'allure du personnage : ce que l'enfant choisit par goût, et qui ne se
 * gagne pas — sa peau, ses cheveux, ses habits de base, son expression, le
 * fond de son studio.
 *
 * À part du dessin 3D, exprès : la page d'accueil et les réglages en ont
 * besoin sans charger le moteur 3D, qui ne vient qu'avec le personnage
 * lui-même.
 */
export type Coiffure = 'meches' | 'boucles' | 'court';
export type Expression = 'sourire' | 'cool';
export type Fond = 'gris' | 'sombre' | 'clair';

export type Apparence = {
  peau: string;
  haut: string;
  bas: string;
  coiffure: Coiffure;
  cheveux: string;
  expression: Expression;
  fond: Fond;
};

export const PEAUX = ['#8d5524', '#6b3e1e', '#c68642', '#e0ac69'];
export const HAUTS = ['#f8fafc', '#2f7d32', '#d7443a', '#2f6db5', '#f5b335', '#1f2937'];
export const BAS = ['#111827', '#1f3a5f', '#4b5563', '#6b4f33'];
export const CHEVEUX = ['#14100d', '#3b2314', '#7a4a21', '#c9962b'];
export const COIFFURES: Array<{ cle: Coiffure; nom: string }> = [
  { cle: 'meches', nom: 'Mèches' },
  { cle: 'boucles', nom: 'Boucles' },
  { cle: 'court', nom: 'Court' },
];
export const EXPRESSIONS: Array<{ cle: Expression; nom: string }> = [
  { cle: 'sourire', nom: 'Souriant' },
  { cle: 'cool', nom: 'Cool' },
];
export const FONDS: Array<{ cle: Fond; nom: string }> = [
  { cle: 'gris', nom: 'Studio gris' },
  { cle: 'sombre', nom: 'Studio sombre' },
  { cle: 'clair', nom: 'Studio clair' },
];

export const APPARENCE_DEFAUT: Apparence = {
  peau: '#8d5524',
  haut: '#f8fafc',
  bas: '#111827',
  coiffure: 'meches',
  cheveux: '#14100d',
  expression: 'sourire',
  fond: 'gris',
};

/** Le fond du studio, derrière le personnage. */
export function fondDuStudio(f: Fond): string {
  if (f === 'gris') return 'radial-gradient(circle at 50% 35%, #6a6d73 0%, #4f5258 55%, #3a3c41 100%)';
  return f === 'sombre'
    ? 'radial-gradient(circle at 50% 30%, #4a4e57 0%, #2b2d33 55%, #17181c 100%)'
    : 'radial-gradient(circle at 50% 30%, #fff8e6 0%, #ffe2b0 55%, #f6c27a 100%)';
}
