import { h } from 'preact';
import { useState } from 'preact/hooks';

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

const FormAddConta = ({ showMessage, onContaAdded }) => {
  const [formData, setFormData] = useState({
    nome_conta: '',
    valor: '',
    data_vencimento: '',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const response = await fetch('/api/contas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData ? JSON.stringify(errorData) : `HTTP error! status: ${response.status}`);
      }

      setFormData({ nome_conta: '', valor: '', data_vencimento: '' });
      onContaAdded();
    } catch (error) {
      console.error("Erro ao cadastrar conta:", error);
      showMessage(`Erro ao cadastrar conta: ${error.message}`, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <h3>Cadastrar Nova Conta</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label htmlFor="nome_conta" className="form-label">Nome da Conta:</label>
          <input
            type="text"
            id="nome_conta"
            name="nome_conta"
            value={formData.nome_conta}
            onChange={handleChange}
            className="form-control"
            placeholder="Ex: Conta de Luz"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="valor" className="form-label">Valor:</label>
          <input
            type="number"
            id="valor"
            name="valor"
            value={formData.valor}
            onChange={handleChange}
            className="form-control"
            step="0.01"
            placeholder="0.00"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="data_vencimento" className="form-label">Data de Vencimento:</label>
          <input
            type="date"
            id="data_vencimento"
            name="data_vencimento"
            value={formData.data_vencimento}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="btn btn-success"
        >
          {submitting ? 'Cadastrando...' : 'Cadastrar Conta'}
        </button>
      </form>
    </div>
  );
};

export default FormAddConta;
