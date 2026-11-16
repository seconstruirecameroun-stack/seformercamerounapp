/**
 * L'allure du personnage : sa peau, son haut, son pantalon.
 *
 * À part du dessin 3D, exprès : la page d'accueil et les réglages en ont
 * besoin sans charger le moteur 3D, qui ne vient qu'avec le personnage
 * lui-même.
 */
export type Apparence = { peau: string; haut: string; bas: string };

export const PEAUX = ['#8d5524', '#6b3e1e', '#c68642', '#e0ac69'];
export const HAUTS = ['#2f7d32', '#d7443a', '#2f6db5', '#f5b335', '#7a4fc4', '#1f2937'];
export const APPARENCE_DEFAUT: Apparence = { peau: '#8d5524', haut: '#2f7d32', bas: '#1f3a5f' };
