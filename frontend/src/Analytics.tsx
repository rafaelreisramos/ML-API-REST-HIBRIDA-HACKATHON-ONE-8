import { useQuery, gql } from '@apollo/client'

const GET_LATEST = gql`
  query GetLatest {
    listarAnalises {
        clienteId
        previsao
        probabilidade
        riscoAlto
        modeloUsado
    }
  }
`

export default function Analytics() {
    const { data, loading } = useQuery(GET_LATEST, { pollInterval: 15000 })

    if (loading) return <div className="card"><h3>Analytics</h3><p>Sincronizando...</p></div>
    if (!data?.listarAnalises) return <div className="card"><h3>Analytics</h3><p>Sem dados.</p></div>

    const analises = [...data.listarAnalises].reverse().slice(0, 5) // Últimas 5
    const total = data.listarAnalises.length
    const riscoCount = data.listarAnalises.filter((a: any) => a.riscoAlto).length
    const safeCount = total - riscoCount

    // Percentagens para barra visual
    const pRisk = total > 0 ? (riscoCount / total) * 100 : 0
    const pSafe = total > 0 ? (safeCount / total) * 100 : 0

    return (
        <div className="card">
            <h3>Monitoramento em Tempo Real</h3>

            {/* Barra de Distribuição de Risco */}
            <div style={{ marginBottom: '32px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem', fontWeight: '500', color: 'var(--text-secondary)' }}>
                    <span>Clientes Baixo Risco</span>
                    <span>Alto Risco Trend</span>
                </div>
                <div style={{ height: '16px', background: 'var(--input-bg)', borderRadius: '8px', overflow: 'hidden', display: 'flex' }}>
                    <div style={{ width: `${pSafe}%`, background: 'var(--success)', transition: 'width 1s ease-out' }}></div>
                    <div style={{ width: `${pRisk}%`, background: 'var(--error)', transition: 'width 1s ease-out' }}></div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    <span>{safeCount}</span>
                    <span>{riscoCount}</span>
                </div>
            </div>

            {/* Lista Recente Estilo iOS */}
            <div>
                <h4 style={{ fontSize: '0.8rem', marginBottom: '16px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    FEED DE ANÁLISES (LIVE)
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {analises.length === 0 && <div style={{ opacity: 0.5, fontStyle: 'italic' }}>Nenhuma análise registrada hoje.</div>}

                    {analises.map((item: any, i: number) => (
                        <div key={i} style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            padding: '12px 16px',
                            background: 'var(--bg-app)',
                            borderRadius: '12px',
                            fontSize: '0.9rem'
                        }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                <div style={{
                                    width: 8, height: 8, borderRadius: '50%',
                                    background: item.riscoAlto ? 'var(--error)' : 'var(--success)'
                                }}></div>
                                <div>
                                    <div style={{ fontWeight: '600', color: 'var(--text-primary)' }}>
                                        {item.clienteId?.substring(0, 15) || 'Cliente'}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                        {item.modeloUsado}
                                    </div>
                                </div>
                            </div>

                            <div style={{ textAlign: 'right' }}>
                                <div style={{
                                    fontSize: '0.9rem',
                                    fontWeight: '700',
                                    color: item.riscoAlto ? 'var(--error)' : 'var(--success)'
                                }}>
                                    {(item.probabilidade * 100).toFixed(0)}%
                                </div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>chance</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
