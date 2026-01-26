import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export const LoginPage: React.FC = () => {
    const [isRegistering, setIsRegistering] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const success = await login(username, password);

        if (!success) {
            setError('Usuário ou senha inválidos');
        }
        setLoading(false);
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccessMsg('');

        if (password !== confirmPassword) {
            setError('As senhas não coincidem');
            return;
        }

        if (password.length < 6) {
            setError('A senha deve ter pelo menos 6 caracteres');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('/usuarios', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ login: username, senha: password }),
            });

            if (response.ok) {
                setSuccessMsg('Conta criada com sucesso! Fazendo login...');
                // Tentar login automático após registro
                const loginSuccess = await login(username, password);
                if (!loginSuccess) {
                    setIsRegistering(false); // Voltar para tela de login se falhar o auto-login
                    setSuccessMsg('Conta criada! Faça login para continuar.');
                }
            } else {
                const text = await response.text();
                if (response.status === 400) {
                    setError('Usuário já existe ou dados inválidos.');
                } else {
                    setError('Erro ao criar conta. Tente novamente.');
                }
                console.error('Erro registro:', text);
            }
        } catch (err) {
            setError('Erro de conexão. Verifique sua rede.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}>
            <div style={{
                background: 'white',
                padding: '2.5rem',
                borderRadius: '16px',
                boxShadow: '0 20px 60px rgba(0,0,0,0.2)',
                width: '100%',
                maxWidth: '420px',
                transition: 'all 0.3s ease'
            }}>
                <h1 style={{
                    textAlign: 'center',
                    marginBottom: '0.5rem',
                    color: '#333',
                    fontSize: '2rem',
                    fontWeight: 700
                }}>
                    {isRegistering ? 'Criar Conta' : 'ChurnInsight'}
                </h1>
                <p style={{
                    textAlign: 'center',
                    color: '#666',
                    marginBottom: '2rem',
                    fontSize: '0.95rem'
                }}>
                    {isRegistering ? 'Entre com seus dados para começar' : 'Faça login para acessar o dashboard'}
                </p>

                <form onSubmit={isRegistering ? handleRegister : handleLogin}>
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            color: '#444',
                            fontWeight: '600',
                            fontSize: '0.9rem'
                        }}>
                            Usuário
                        </label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            placeholder="Ex: analista_01"
                            style={{
                                width: '100%',
                                padding: '0.9rem',
                                border: '2px solid #e0e0e0',
                                borderRadius: '8px',
                                fontSize: '1rem',
                                outline: 'none',
                                transition: 'border-color 0.2s',
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                        />
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            color: '#444',
                            fontWeight: '600',
                            fontSize: '0.9rem'
                        }}>
                            Senha
                        </label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="******"
                            style={{
                                width: '100%',
                                padding: '0.9rem',
                                border: '2px solid #e0e0e0',
                                borderRadius: '8px',
                                fontSize: '1rem',
                                outline: 'none',
                                transition: 'border-color 0.2s',
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                        />
                    </div>

                    {isRegistering && (
                        <div style={{ marginBottom: '1.5rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                color: '#444',
                                fontWeight: '600',
                                fontSize: '0.9rem'
                            }}>
                                Confirmar Senha
                            </label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                placeholder="******"
                                style={{
                                    width: '100%',
                                    padding: '0.9rem',
                                    border: '2px solid #e0e0e0',
                                    borderRadius: '8px',
                                    fontSize: '1rem',
                                    outline: 'none',
                                    transition: 'border-color 0.2s',
                                }}
                                onFocus={(e) => e.target.style.borderColor = '#667eea'}
                                onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                            />
                        </div>
                    )}

                    {error && (
                        <div style={{
                            padding: '0.8rem',
                            marginBottom: '1rem',
                            background: '#fee2e2',
                            color: '#dc2626',
                            borderRadius: '8px',
                            fontSize: '0.9rem',
                            textAlign: 'center',
                            border: '1px solid #fecaca'
                        }}>
                            {error}
                        </div>
                    )}

                    {successMsg && (
                        <div style={{
                            padding: '0.8rem',
                            marginBottom: '1rem',
                            background: '#dcfce7',
                            color: '#16a34a',
                            borderRadius: '8px',
                            fontSize: '0.9rem',
                            textAlign: 'center',
                            border: '1px solid #bbf7d0'
                        }}>
                            {successMsg}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '1rem',
                            background: loading ? '#9ca3af' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            fontSize: '1rem',
                            fontWeight: '600',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            transition: 'all 0.2s',
                            boxShadow: loading ? 'none' : '0 4px 6px rgba(102, 126, 234, 0.25)'
                        }}
                        onMouseEnter={(e) => !loading && (e.currentTarget.style.transform = 'translateY(-2px)')}
                        onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                    >
                        {loading ? 'Processando...' : (isRegistering ? 'Cadastrar' : 'Entrar')}
                    </button>
                </form>

                <div style={{
                    marginTop: '2rem',
                    textAlign: 'center',
                    borderTop: '1px solid #f3f4f6',
                    paddingTop: '1.5rem'
                }}>
                    <span style={{ color: '#666', fontSize: '0.95rem' }}>
                        {isRegistering ? 'Já tem uma conta?' : 'Não tem conta?'}
                    </span>
                    <button
                        onClick={() => {
                            setIsRegistering(!isRegistering);
                            setError('');
                            setSuccessMsg('');
                        }}
                        style={{
                            background: 'none',
                            border: 'none',
                            color: '#667eea',
                            fontWeight: '700',
                            cursor: 'pointer',
                            marginLeft: '0.5rem',
                            fontSize: '0.95rem',
                            textDecoration: 'none'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.textDecoration = 'underline'}
                        onMouseLeave={(e) => e.currentTarget.style.textDecoration = 'none'}
                    >
                        {isRegistering ? 'Fazer Login' : 'Cadastre-se agora'}
                    </button>
                </div>
            </div>
        </div>
    );
};
