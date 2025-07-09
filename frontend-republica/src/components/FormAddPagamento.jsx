import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';

// Função auxiliar para obter o CSRF token do cookie
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const FormAddPagamento = ({ showMessage, onPagamentoAdded }) => {
  const [contasNaoPagas, setContasNaoPagas] = useState([]);
  const [selectedConta, setSelectedConta] = useState('');
  const [loadingContas, setLoadingContas] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const fetchContasNaoPagas = async () => {
    setLoadingContas(true);
    try {
      const response = await fetch('/api/contas/?paga=false'); // Filtra contas não pagas
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setContasNaoPagas(data.filter(conta => !conta.paga)); // Garante que só vem não pagas
      if (data.length > 0) {
        setSelectedConta(data[0].id); // Seleciona a primeira conta por padrão
      }
    } catch (error) {
      console.error("Erro ao buscar contas não pagas:", error);
      showMessage('Erro ao carregar contas disponíveis para pagamento.', 'error');
    } finally {
      setLoadingContas(false);
    }
  };

  useEffect(() => {
    fetchContasNaoPagas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedConta) {
      showMessage('Selecione uma conta para pagar.', 'error');
      return;
    }
    setSubmitting(true);
    try {
      const response = await fetch('/api/pagamentos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ conta: selectedConta }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        let errorMessage = 'Erro ao registrar pagamento.';
        if (errorData && typeof errorData === 'object') {
          errorMessage = Object.values(errorData).flat().join(' ');
        } else if (errorData) {
          errorMessage = JSON.stringify(errorData);
        }
        throw new Error(errorMessage);
      }

      setSelectedConta(''); // Limpa a seleção
      onPagamentoAdded(); // Recarrega a lista de pagamentos e contas
      fetchContasNaoPagas(); // Recarrega a lista de contas não pagas para o formulário
    } catch (error) {
      console.error("Erro ao registrar pagamento:", error);
      showMessage(`Erro ao registrar pagamento: ${error.message}`, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingContas) return <LoadingSpinner />;

  return (
    <div className="form-container">
      <h3>Realizar Novo Pagamento</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label htmlFor="conta" className="form-label">Selecione a Conta:</label>
          {contasNaoPagas.length === 0 ? (
            <p className="mt-1" style={{ color: 'black' }}>Não há contas pendentes para pagar.</p>
          ) : (
            <select
              id="conta"
              name="conta"
              value={selectedConta}
              onChange={(e) => setSelectedConta(e.target.value)}
              className="form-control"
              required
            >
              {contasNaoPagas.map((conta) => (
                <option key={conta.id} value={conta.id}>
                  {conta.nome_conta} - R$ {parseFloat(conta.valor).toFixed(2).replace('.', ',')} (Vencimento: {new Date(conta.data_vencimento).toLocaleDateString('pt-BR')})
                </option>
              ))}
            </select>
          )}
        </div>
        <p style={{ color: 'black' }}><strong>Obs:</strong> O pagamento será sempre do valor total da conta.</p>
        <button
          type="submit"
          disabled={submitting || contasNaoPagas.length === 0}
          className="btn btn-purple"
        >
          {submitting ? 'Registrando...' : 'Registrar Pagamento'}
        </button>
      </form>
    </div>
  );
};

export default FormAddPagamento;
