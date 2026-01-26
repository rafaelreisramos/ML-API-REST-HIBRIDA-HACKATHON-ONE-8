/**
 * Utilitário para fazer requisições HTTP autenticadas
 */

export const fetchWithAuth = async (
    url: string,
    options: RequestInit = {}
): Promise<Response> => {
    const token = localStorage.getItem('auth_token');

    const headers = {
        ...options.headers,
        ...(token && { 'Authorization': `Bearer ${token}` }),
    };

    const response = await fetch(url, {
        ...options,
        headers,
    });

    // Se receber 401 ou 403, limpar token e redirecionar para login
    if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }

    return response;
};
