import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import FormAddMembro from './FormAddMembro';

const ListarMembro = ({ showMessage }) => {
  const [pessoas, setPessoas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchPessoas = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/pessoas/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPessoas(data);
    } catch (error) {
      console.error("Erro ao buscar membros:", error);
      showMessage('Erro ao carregar a lista de membros.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPessoas();
  }, []);

  const handlePessoaAdded = () => {
    fetchPessoas();
    setShowAddForm(false);
    showMessage('Membro cadastrado com sucesso!', 'success');
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="mycard">
      <h2>Membros da República</h2>
      <button
        onClick={() => setShowAddForm(!showAddForm)}
        className="btn btn-primary"
        style={{ marginBottom: '1.5rem' }} /* Adiciona margem inferior */
      >
        {showAddForm ? 'Ocultar Formulário' : 'Cadastrar Novo Membro'}
      </button>

      {showAddForm && (
        <FormAddMembro showMessage={showMessage} onPessoaAdded={handlePessoaAdded} />
      )}

      {pessoas.length === 0 ? (
        <p style={{ color: 'black' }}>Nenhum membro cadastrado ainda.</p>
      ) : (
        <div className="table-container">
          <table className="table-striped">
            <thead>
              <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Idade</th>
                <th>Telefone</th>
                <th>República</th>
              </tr>
            </thead>
            <tbody>
              {pessoas.map((pessoa) => (
                <tr key={pessoa.id}>
                  <td>{pessoa.nome}</td>
                  <td>{pessoa.cpf}</td>
                  <td>{pessoa.idade}</td>
                  <td>{pessoa.telefone}</td>
                  <td>{pessoa.republica_nome}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ListarMembro;
