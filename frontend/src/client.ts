import { ApolloClient, InMemoryCache } from '@apollo/client';

export const client = new ApolloClient({
    uri: '/graphql', // Proxy Vite redirecionará para http://localhost:9999/graphql
    cache: new InMemoryCache(),
});
