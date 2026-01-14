import { useQuery, gql } from '@apollo/client'

const GET_ANALYTICS_DATA = gql`
  query GetAnalyticsData {
    listarAnalises {
        clienteId
        idade
        genero
        regiao
        valorMensal
        tempoAssinaturaMeses
        planoAssinatura
        visualizacoesMes
        contatosSuporte
        avaliacaoPlataforma
        tipoContrato
        categoriaFavorita
        previsao
        probabilidade
        riscoAlto
        modeloUsado
    }
  }
`

// Tipos
interface ChurnData {
    clienteId: string
    idade: number
    genero: string
    regiao: string
    valorMensal: number
    tempoAssinaturaMeses: number
    planoAssinatura: string
    visualizacoesMes: number
    contatosSuporte: number
    avaliacaoPlataforma: number
    tipoContrato: string
    categoriaFavorita: string
    previsao: string
    probabilidade: number
    riscoAlto: boolean
    modeloUsado: string
}

// Processamento de dados (Power Query simulado)
const processData = (rawData: ChurnData[]) => {
    // KPIs
    const totalClientes = rawData.length
    const clientesRisco = rawData.filter(c => c.riscoAlto).length
    const taxaChurn = totalClientes > 0 ? (rawData.reduce((acc, c) => acc + c.probabilidade, 0) / totalClientes) * 100 : 0
    const ticketMedio = totalClientes > 0 ? rawData.reduce((acc, c) => acc + c.valorMensal, 0) / totalClientes : 0
    const npsMedia = totalClientes > 0 ? rawData.reduce((acc, c) => acc + c.avaliacaoPlataforma, 0) / totalClientes : 0

    // Distribuição por Região
    const porRegiao = rawData.reduce((acc, c) => {
        acc[c.regiao] = (acc[c.regiao] || 0) + 1
        return acc
    }, {} as Record<string, number>)

    // Distribuição por Plano
    const porPlano = rawData.reduce((acc, c) => {
        acc[c.planoAssinatura] = (acc[c.planoAssinatura] || 0) + 1
        return acc
    }, {} as Record<string, number>)

    // Top 10 em Risco
    const topRisco = [...rawData]
        .sort((a, b) => b.probabilidade - a.probabilidade)
        .slice(0, 10)

    // Churn por Região
    const churnPorRegiao = Object.entries(porRegiao).map(([regiao, total]) => {
        const emRisco = rawData.filter(c => c.regiao === regiao && c.riscoAlto).length
        return { regiao, total, emRisco, taxa: (emRisco / total) * 100 }
    }).sort((a, b) => b.taxa - a.taxa)

    return {
        kpis: { totalClientes, clientesRisco, taxaChurn, ticketMedio, npsMedia },
        porRegiao,
        porPlano,
        topRisco,
        churnPorRegiao
    }
}

export default function Analytics() {
    const { data, loading } = useQuery(GET_ANALYTICS_DATA, { pollInterval: 0 })

    if (loading) return (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
            <div className="loading-spinner"></div>
            <p style={{ marginTop: '15px', color: 'var(--text-secondary)' }}>Carregando dashboard...</p>
        </div>
    )

    if (!data?.listarAnalises || data.listarAnalises.length === 0) {
        return <div className="card"><h3>📊 Dashboard Analytics</h3><p>Sem dados para análise. Execute algumas previsões primeiro.</p></div>
    }

    const analytics = processData(data.listarAnalises)
    const { kpis, porPlano, topRisco, churnPorRegiao } = analytics

    // Cores do tema
    const colors = {
        primary: '#10b981',
        danger: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6',
        dark: '#1f2937',
        darker: '#111827'
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', height: '100%' }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ margin: 0 }}>📊 Dashboard Analytics</h3>
                <span style={{
                    background: colors.primary,
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '6px',
                    fontSize: '0.75rem',
                    fontWeight: '700'
                }}>LIVE</span>
            </div>

            {/* KPI Cards Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '15px' }}>
                {/* Total Clientes */}
                <div className="card" style={{ background: `linear-gradient(135deg, ${colors.info} 0%, ${colors.info}dd 100%)`, color: 'white', padding: '20px' }}>
                    <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '8px' }}>TOTAL ANALISADOS</div>
                    <div style={{ fontSize: '2rem', fontWeight: '800' }}>{kpis.totalClientes.toLocaleString()}</div>
                    <div style={{ fontSize: '0.7rem', opacity: 0.8, marginTop: '4px' }}>clientes</div>
                </div>

                {/* Taxa de Churn */}
                <div className="card" style={{ background: `linear-gradient(135deg, ${colors.warning} 0%, ${colors.warning}dd 100%)`, color: 'white', padding: '20px' }}>
                    <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '8px' }}>TAXA DE CHURN</div>
                    <div style={{ fontSize: '2rem', fontWeight: '800' }}>{kpis.taxaChurn.toFixed(1)}%</div>
                    <div style={{ fontSize: '0.7rem', opacity: 0.8, marginTop: '4px' }}>média geral</div>
                </div>

                {/* Clientes em Risco */}
                <div className="card" style={{ background: `linear-gradient(135deg, ${colors.danger} 0%, ${colors.danger}dd 100%)`, color: 'white', padding: '20px' }}>
                    <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '8px' }}>ALTO RISCO</div>
                    <div style={{ fontSize: '2rem', fontWeight: '800' }}>{kpis.clientesRisco.toLocaleString()}</div>
                    <div style={{ fontSize: '0.7rem', opacity: 0.8, marginTop: '4px' }}>clientes críticos</div>
                </div>

                {/* Ticket Médio */}
                <div className="card" style={{ background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primary}dd 100%)`, color: 'white', padding: '20px' }}>
                    <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '8px' }}>TICKET MÉDIO</div>
                    <div style={{ fontSize: '2rem', fontWeight: '800' }}>R$ {kpis.ticketMedio.toFixed(0)}</div>
                    <div style={{ fontSize: '0.7rem', opacity: 0.8, marginTop: '4px' }}>por cliente</div>
                </div>

                {/* NPS Médio */}
                <div className="card" style={{ background: `linear-gradient(135deg, ${colors.dark} 0%, ${colors.darker} 100%)`, color: 'white', padding: '20px' }}>
                    <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '8px' }}>NPS MÉDIO</div>
                    <div style={{ fontSize: '2rem', fontWeight: '800' }}>{kpis.npsMedia.toFixed(1)}</div>
                    <div style={{ fontSize: '0.7rem', opacity: 0.8, marginTop: '4px' }}>satisfação</div>
                </div>
            </div>

            {/* Charts Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', flex: 1 }}>
                {/* Gráfico de Pizza - Distribuição por Plano */}
                <div className="card" style={{ padding: '20px' }}>
                    <h4 style={{ margin: '0 0 20px 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>DISTRIBUIÇÃO POR PLANO</h4>
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
                        {Object.keys(porPlano).length > 0 ? (
                            <PieChart data={porPlano} colors={[colors.primary, colors.info, colors.warning]} />
                        ) : (
                            <p style={{ color: 'var(--text-secondary)' }}>Sem dados</p>
                        )}
                    </div>
                </div>

                {/* Ranking de Risco */}
                <div className="card" style={{ padding: '20px', maxHeight: '300px', overflowY: 'auto' }}>
                    <h4 style={{ margin: '0 0 15px 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>TOP 10 CLIENTES EM RISCO</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {topRisco.map((cliente, i) => (
                            <div key={i} style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '10px',
                                background: 'var(--bg-app)',
                                borderRadius: '8px',
                                borderLeft: `3px solid ${cliente.probabilidade > 0.7 ? colors.danger : colors.warning}`
                            }}>
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontSize: '0.85rem', fontWeight: '600' }}>{cliente.clienteId}</div>
                                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{cliente.planoAssinatura}</div>
                                </div>
                                <div style={{ textAlign: 'right' }}>
                                    <div style={{ fontSize: '0.9rem', fontWeight: '700', color: colors.danger }}>
                                        {(cliente.probabilidade * 100).toFixed(1)}%
                                    </div>
                                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                                        R$ {cliente.valorMensal.toFixed(0)}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Churn por Região - Barras Horizontais */}
                <div className="card" style={{ padding: '20px', gridColumn: '1 / -1' }}>
                    <h4 style={{ margin: '0 0 20px 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>CHURN POR REGIÃO</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {churnPorRegiao.map((item, i) => (
                            <div key={i}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                                    <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>{item.regiao}</span>
                                    <span style={{ fontSize: '0.85rem', color: colors.danger, fontWeight: '700' }}>
                                        {item.emRisco} / {item.total} ({item.taxa.toFixed(1)}%)
                                    </span>
                                </div>
                                <div style={{
                                    height: '8px',
                                    background: 'var(--input-bg)',
                                    borderRadius: '4px',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        height: '100%',
                                        width: `${item.taxa}%`,
                                        background: `linear-gradient(90deg, ${colors.warning}, ${colors.danger})`,
                                        transition: 'width 1s ease-out'
                                    }}></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

// Componente auxiliar: Gráfico de Pizza CSS Puro
function PieChart({ data, colors }: { data: Record<string, number>, colors: string[] }) {
    const total = Object.values(data).reduce((a, b) => a + b, 0)
    const entries = Object.entries(data)

    let cumulativePercent = 0

    return (
        <div style={{ position: 'relative', width: '180px', height: '180px' }}>
            <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)' }}>
                {entries.map(([key, value], i) => {
                    const percent = (value / total) * 100
                    const offset = cumulativePercent
                    cumulativePercent += percent

                    return (
                        <circle
                            key={key}
                            cx="50"
                            cy="50"
                            r="40"
                            fill="none"
                            stroke={colors[i % colors.length]}
                            strokeWidth="20"
                            strokeDasharray={`${percent * 2.51} ${251 - percent * 2.51}`}
                            strokeDashoffset={-offset * 2.51}
                            style={{ transition: 'all 0.5s ease' }}
                        />
                    )
                })}
            </svg>
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center'
            }}>
                <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>{total}</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>total</div>
            </div>
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {entries.map(([key, value], i) => (
                    <div key={key} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
                        <div style={{ width: '12px', height: '12px', borderRadius: '2px', background: colors[i % colors.length] }}></div>
                        <span>{key}: {value} ({((value / total) * 100).toFixed(0)}%)</span>
                    </div>
                ))}
            </div>
        </div>
    )
}
