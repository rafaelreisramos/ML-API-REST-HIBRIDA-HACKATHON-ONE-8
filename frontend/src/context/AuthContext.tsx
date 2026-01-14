import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
    token: string | null;
    isAuthenticated: boolean;
    login: (username: string, password: string) => Promise<boolean>;
    logout: () => void;
    getToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [token, setToken] = useState<string | null>(null);

    // Carregar token do localStorage ao iniciar
    useEffect(() => {
        const savedToken = localStorage.getItem('auth_token');
        if (savedToken) {
            setToken(savedToken);
        }
    }, []);

    const login = async (username: string, password: string): Promise<boolean> => {
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ login: username, senha: password }),
            });

            if (response.ok) {
                const data = await response.json();
                const newToken = data.token;
                setToken(newToken);
                localStorage.setItem('auth_token', newToken);
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            return false;
        }
    };

    const logout = () => {
        setToken(null);
        localStorage.removeItem('auth_token');
    };

    const getToken = () => {
        return token;
    };

    return (
        <AuthContext.Provider
            value={{
                token,
                isAuthenticated: !!token,
                login,
                logout,
                getToken,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth deve ser usado dentro de um AuthProvider');
    }
    return context;
};
