import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Button, Card, ErrorNote, Loading } from '../ui';
import { abonnesIci, activer, desactiver, essai, etatGeneral } from '../../lib/notifications';

/**
 * Les rappels du soir, réglés par le parent.
 *
 * Le réglage vit ici et non dans l'espace de l'enfant : c'est le téléphone du
 * parent, et c'est lui qui décide si une application a le droit de sonner
 * chez lui. Un enfant de sept ans à qui le navigateur demande « autoriser les
 * notifications ? » répond oui sans savoir à quoi.
 *
 * L'interrupteur est par enfant et par appareil : les deux frères partagent
 * souvent le même téléphone, et chacun doit recevoir son propre message.
 */

const EXPLICATIONS: Record<string, string> = {
  impossible: 'Ce navigateur ne sait pas recevoir de rappels. Essayez depuis Chrome sur le téléphone.',
  'non-configure': 'Les rappels ne sont pas encore configurés sur ce serveur.',
  refuse:
    'Les notifications sont bloquées pour ce site. Pour les rétablir : réglages du navigateur, puis Notifications.',
};

export default function Rappels({
  parentId,
  enfants,
}: {
  parentId: string;
  enfants: Array<{ id: string; first_name: string }>;
}) {
  const qc = useQueryClient();
  const [erreur, setErreur] = useState<unknown>(null);
  const [occupe, setOccupe] = useState<string | null>(null);
  const general = etatGeneral();

  const abonnes = useQuery({
    queryKey: ['abonnements-ici'],
    queryFn: abonnesIci,
    enabled: general !== 'impossible',
  });

  async function basculer(childId: string, actif: boolean) {
    setErreur(null);
    setOccupe(childId);
    try {
      if (actif) await desactiver(childId);
      else await activer(parentId, childId);
      await qc.invalidateQueries({ queryKey: ['abonnements-ici'] });
    } catch (err) {
      setErreur(err);
    } finally {
      setOccupe(null);
    }
  }

  return (
    <Card
      titre="Rappels du soir"
      sous="Un seul message par jour, vers 18 h, et uniquement si l’enfant n’a pas encore joué."
    >
      {EXPLICATIONS[general] ? (
        <p className="rounded-2xl bg-gold/25 px-4 py-3 text-sm font-semibold text-ink-2">
          {EXPLICATIONS[general]}
        </p>
      ) : null}

      {erreur ? (
        <div className="mt-3">
          <ErrorNote error={erreur} />
        </div>
      ) : null}

      {abonnes.isLoading ? <Loading /> : null}

      <ul className="mt-3 grid gap-3 sm:grid-cols-2">
        {enfants.map((enfant) => {
          const actif = abonnes.data?.has(enfant.id) ?? false;
          return (
            <li
              key={enfant.id}
              className="flex items-center justify-between gap-3 rounded-2xl border border-line px-4 py-3"
            >
              <div className="min-w-0">
                <strong className="block truncate">{enfant.first_name}</strong>
                <small className="block text-muted">
                  {actif ? 'Rappels activés sur cet appareil' : 'Aucun rappel sur cet appareil'}
                </small>
              </div>
              <div className="flex shrink-0 gap-2">
                {actif ? (
                  <Button
                    variant="ghost"
                    onClick={() => essai(enfant.first_name)}
                    title="Afficher tout de suite un rappel d’exemple"
                  >
                    Essayer
                  </Button>
                ) : null}
                <Button
                  variant={actif ? 'ghost' : 'primary'}
                  disabled={occupe === enfant.id || general === 'impossible' || general === 'non-configure'}
                  onClick={() => basculer(enfant.id, actif)}
                >
                  {occupe === enfant.id ? '…' : actif ? 'Couper' : 'Activer'}
                </Button>
              </div>
            </li>
          );
        })}
      </ul>

      {enfants.length === 0 ? (
        <p className="mt-4 text-sm text-muted">Ajoutez d’abord un profil d’enfant.</p>
      ) : null}
    </Card>
  );
}
