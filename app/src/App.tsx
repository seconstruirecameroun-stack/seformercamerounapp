import { Navigate, Route, Routes } from 'react-router-dom';
import { SessionProvider, useSession } from './lib/auth';
import { Loading } from './components/ui';
import LoginPage from './pages/Login';
import ProfilePicker from './pages/ProfilePicker';
import Landing from './pages/Landing';
import ParentSpace from './pages/parent/ParentSpace';
import PinGate from './components/PinGate';
import ChildSpace from './pages/child/ChildSpace';
import ChildHome from './pages/child/ChildHome';
import Matiere from './pages/child/Matiere';

/**
 * La racine a deux visages.
 *
 * Un parent déjà connecté veut ses enfants, tout de suite ; un visiteur veut
 * comprendre ce que fait l'app. Rediriger ce dernier vers un formulaire de
 * connexion, comme avant, lui demandait de s'engager avant d'avoir rien vu.
 */
function Accueil() {
  const { session, ready } = useSession();
  if (!ready) return <Loading label="Ouverture de la session…" />;
  return session ? <ProfilePicker /> : <Landing />;
}

function RequireParent({ children }: { children: React.ReactNode }) {
  const { session, ready } = useSession();
  if (!ready) return <Loading label="Ouverture de la session…" />;
  if (!session) return <Navigate to="/connexion" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <SessionProvider>
      <Routes>
        <Route path="/connexion" element={<LoginPage />} />
        <Route path="/" element={<Accueil />} />
        <Route
          path="/parent"
          element={
            <RequireParent>
              <PinGate>
                <ParentSpace />
              </PinGate>
            </RequireParent>
          }
        />
        <Route
          path="/enfant/:childId"
          element={
            <RequireParent>
              <ChildHome />
            </RequireParent>
          }
        />
        <Route
          path="/enfant/:childId/matiere/:subjectId"
          element={
            <RequireParent>
              <Matiere />
            </RequireParent>
          }
        />
        <Route
          path="/enfant/:childId/lecon/:lessonId"
          element={
            <RequireParent>
              <ChildSpace />
            </RequireParent>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </SessionProvider>
  );
}
