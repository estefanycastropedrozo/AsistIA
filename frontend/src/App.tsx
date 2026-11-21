import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ChatView } from './components/ChatView';
import { AdminDashboard } from './components/AdminDashboard';
import { PrivacyModal } from './components/PrivacyModal';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'admin'>('chat');
  const [userRole, setUserRole] = useState<string>('estudiante');
  const [isPrivacyOpen, setIsPrivacyOpen] = useState(false);
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);

  // Comprobar salud del backend periódicamente
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/health');
        if (res.ok) {
          setIsBackendHealthy(true);
        } else {
          setIsBackendHealthy(false);
        }
      } catch {
        setIsBackendHealthy(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen teinco-bg flex flex-col text-slate-800">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenPrivacy={() => setIsPrivacyOpen(true)}
        isBackendHealthy={isBackendHealthy}
        userRole={userRole}
        setUserRole={setUserRole}
      />

      <main className="flex-1">
        {activeTab === 'chat' ? (
          <ChatView userRole={userRole} setUserRole={setUserRole} />
        ) : (
          <AdminDashboard />
        )}
      </main>

      <PrivacyModal isOpen={isPrivacyOpen} onClose={() => setIsPrivacyOpen(false)} />
    </div>
  );
};

export default App;
