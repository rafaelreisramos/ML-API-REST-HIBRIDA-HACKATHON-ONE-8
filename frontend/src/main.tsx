import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { ApolloProvider } from '@apollo/client'
import { client } from './client.ts'
import { AuthProvider } from './context/AuthContext.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AuthProvider>
            <ApolloProvider client={client}>
                <App />
            </ApolloProvider>
        </AuthProvider>
    </React.StrictMode>,
)
