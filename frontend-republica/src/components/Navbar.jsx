import { h } from 'preact';

const Navbar = ({ onNavigate, currentPath }) => (
  <header className="topnav">
    <ul>
      <li>
        <button
          onClick={() => onNavigate('dashboard')}
          className={currentPath === 'dashboard' ? 'active-nav-item' : ''}
        >
          Início
        </button>
      </li>
      <li>
        <button
          onClick={() => onNavigate('contas')}
          className={currentPath === 'contas' ? 'active-nav-item' : ''}
        >
          Contas
        </button>
      </li>
      <li>
        <button
          onClick={() => onNavigate('pagamentos')}
          className={currentPath === 'pagamentos' ? 'active-nav-item' : ''}
        >
          Pagamentos
        </button>
      </li>
      <li>
        <button
          onClick={() => onNavigate('membros')}
          className={currentPath === 'membros' ? 'active-nav-item' : ''}
        >
          Membros
        </button>
      </li>
      <li>
        {/* O logout ainda será via Django, então redirecionamos */}
        <a href="/auth/logout" className="btn-red">
          Sair
        </a>
      </li>
    </ul>
  </header>
);

export default Navbar;
