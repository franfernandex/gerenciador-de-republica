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

const FormAddMembro = ({ showMessage, onPessoaAdded }) => {
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    idade: '',
    telefone: '',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const response = await fetch('/api/pessoas/', {
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

      setFormData({ nome: '', cpf: '', idade: '', telefone: '' });
      onPessoaAdded(); // Chama a função para recarregar a lista e fechar o formulário
    } catch (error) {
      console.error("Erro ao cadastrar membro:", error);
      showMessage(`Erro ao cadastrar membro: ${error.message}`, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <h3>Cadastrar Novo Membro</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label htmlFor="nome" className="form-label">Nome</label>
          <input
            type="text"
            id="nome"
            name="nome"
            value={formData.nome}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="cpf" className="form-label">CPF</label>
          <input
            type="text"
            id="cpf"
            name="cpf"
            value={formData.cpf}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="idade" className="form-label">Idade</label>
          <input
            type="number"
            id="idade"
            name="idade"
            value={formData.idade}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="telefone" className="form-label">Telefone</label>
          <input
            type="text"
            id="telefone"
            name="telefone"
            value={formData.telefone}
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
          {submitting ? 'Cadastrando...' : 'Cadastrar Membro'}
        </button>
      </form>
    </div>
  );
};

export default FormAddMembro;
