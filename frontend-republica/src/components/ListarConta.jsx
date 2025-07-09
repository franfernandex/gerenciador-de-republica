import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import FormAddConta from './FormAddConta';

const ListarConta = ({ showMessage }) => {
  const [contas, setContas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchContas = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/contas/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setContas(data);
    } catch (error) {
      console.error("Erro ao buscar contas:", error);
      showMessage('Erro ao carregar a lista de contas.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContas();
  }, []);

  const handleContaAdded = () => {
    fetchContas();
    setShowAddForm(false);
    showMessage('Conta cadastrada com sucesso!', 'success');
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="mycard">
      <h2>Contas da República</h2>
      <button
        onClick={() => setShowAddForm(!showAddForm)}
        className="btn btn-primary"
        style={{ marginBottom: '1.5rem' }} /* Adiciona margem inferior */
      >
        {showAddForm ? 'Ocultar Formulário' : 'Cadastrar Nova Conta'}
      </button>

      {showAddForm && (
        <FormAddConta showMessage={showMessage} onContaAdded={handleContaAdded} />
      )}

      {contas.length === 0 ? (
        <p style={{ color: 'black' }}>Nenhuma conta cadastrada ainda.</p>
      ) : (
        <div className="table-container">
          <table className="table-striped">
            <thead>
              <tr>
                <th>Nome da Conta</th>
                <th>Valor</th>
                <th>Data de Vencimento</th>
                <th>Status</th>
                <th>República</th>
              </tr>
            </thead>
            <tbody>
              {contas.map((conta) => (
                <tr key={conta.id}>
                  <td>{conta.nome_conta}</td>
                  <td>R$ {parseFloat(conta.valor).toFixed(2).replace('.', ',')}</td>
                  <td>{new Date(conta.data_vencimento).toLocaleDateString('pt-BR')}</td>
                  <td>
                    <span className={`status-badge ${conta.paga ? 'success' : 'warning'}`}>
                      {conta.paga ? 'Paga' : 'Pendente'}
                    </span>
                  </td>
                  <td>{conta.republica_nome}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ListarConta;
