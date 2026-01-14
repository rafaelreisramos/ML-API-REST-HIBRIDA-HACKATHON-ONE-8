# Implementation Plan - Fix GraphQL Security

This plan addresses the `403 Forbidden` error when accessing the GraphQL API with a valid JWT token.

## Proposed Changes

### 1. Backend Security Configuration

**File:** `src/main/java/com/hackathon/churn/security/SecurityConfiguration.java`

- **Current State:** The `/graphql` endpoint is not explicitly defined, falling into `anyRequest().authenticated()`. For reasons likely related to dispatcher types or path matching precedence, this is resulting in 403.
- **Change:** Explicitly add `req.requestMatchers("/graphql").authenticated()` to the security chain.
- **Why:** Ensures Spring Security recognizes the GraphQL endpoint as a valid secured resource accessible to authenticated users (`ROLE_USER`).

```java
// Snippet of proposed change
.authorizeHttpRequests(req -> {
    req.requestMatchers("/login").permitAll();
    req.requestMatchers("/usuarios").permitAll();
    req.requestMatchers("/actuator/health").permitAll();
    req.requestMatchers("/graphiql").permitAll();
    
    // NEW LINE: Explicitly allow authenticated access to GraphQL
    req.requestMatchers("/graphql").authenticated(); 
    
    req.anyRequest().authenticated();
})
```

### 2. Validation

- Run `verify_security.py` script locally to confirm:
  - Login returns token (Status 200)
  - GraphQL Query with token returns Data (Status 200) - **Success Criteria**
- Check Docker Health via `docker ps` (Backend should be healthy).

### 3. Deployment

- Rebuild backend container to apply Java changes.
- Command: `docker-compose up -d --build backend`

## Verification Steps

1. User approves this plan.
2. Agent applies code change.
3. Agent triggers rebuild (approx 2 mins).
4. Agent runs `verify_security.py`.
