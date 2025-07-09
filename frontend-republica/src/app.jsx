import { useState } from 'preact/hooks';
import MensagemAlerta from './components/MensagemAlerta';
import Navbar from './components/Navbar';
import Home from './components/Home';
import ListarMembro from './components/ListarMembro';
import ListarConta from './components/ListarConta';
import ListarPagamento from './components/ListarPagamento';

export function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [message, setMessage] = useState(null);
  const [messageType, setMessageType] = useState('success');

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage(null);
    }, 5000);
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="app-container">
      <MensagemAlerta message={message} type={messageType} onClose={() => setMessage(null)} />
      <Navbar onNavigate={handleNavigate} currentPath={currentPage} />
      <main className="main-content-area">
        {currentPage === 'dashboard' && <Home />}
        {currentPage === 'membros' && <ListarMembro showMessage={showMessage} />}
        {currentPage === 'contas' && <ListarConta showMessage={showMessage} />}
        {currentPage === 'pagamentos' && <ListarPagamento showMessage={showMessage} />}
      </main>
    </div>
  );
}