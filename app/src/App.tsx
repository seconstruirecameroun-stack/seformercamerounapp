import { Navigate, Route, Routes } from 'react-router-dom';
import { SessionProvider, useSession } from './lib/auth';
import { Loading } from './components/ui';
import LoginPage from './pages/Login';
import ProfilePicker from './pages/ProfilePicker';
import ParentSpace from './pages/parent/ParentSpace';
import ChildSpace from './pages/child/ChildSpace';

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
        <Route
          path="/"
          element={
            <RequireParent>
              <ProfilePicker />
            </RequireParent>
          }
        />
        <Route
          path="/parent"
          element={
            <RequireParent>
              <ParentSpace />
            </RequireParent>
          }
        />
        <Route
          path="/enfant/:childId"
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
