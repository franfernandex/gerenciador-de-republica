import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import FormAddPagamento from './FormAddPagamento';

const ListarPagamento = ({ showMessage }) => {
  const [pagamentos, setPagamentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchPagamentos = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/pagamentos/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPagamentos(data);
    } catch (error) {
      console.error("Erro ao buscar pagamentos:", error);
      showMessage('Erro ao carregar a lista de pagamentos.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPagamentos();
  }, []);

  const handlePagamentoAdded = () => {
    fetchPagamentos();
    setShowAddForm(false);
    showMessage('Pagamento registrado com sucesso!', 'success');
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="mycard">
      <h2>Pagamentos Realizados</h2>
      <button
        onClick={() => setShowAddForm(!showAddForm)}
        className="btn btn-primary"
        style={{ marginBottom: '1.5rem' }} /* Adiciona margem inferior */
      >
        {showAddForm ? 'Ocultar Formulário' : 'Realizar Novo Pagamento'}
      </button>

      {showAddForm && (
        <FormAddPagamento showMessage={showMessage} onPagamentoAdded={handlePagamentoAdded} />
      )}

      {pagamentos.length === 0 ? (
        <p style={{ color: 'black' }}>Nenhum pagamento registrado ainda.</p>
      ) : (
        <div className="table-container">
          <table className="table-striped">
            <thead>
              <tr>
                <th>Conta</th>
                <th>Valor Pago</th>
                <th>Data do Pagamento</th>
                <th>Pago por</th>
              </tr>
            </thead>
            <tbody>
              {pagamentos.map((pagamento) => (
                <tr key={pagamento.id}>
                  <td>{pagamento.conta_nome}</td>
                  <td>R$ {parseFloat(pagamento.valor_pago).toFixed(2).replace('.', ',')}</td>
                  <td>{new Date(pagamento.data_pagamento).toLocaleDateString('pt-BR')}</td>
                  <td>{pagamento.pessoa_nome}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ListarPagamento;
