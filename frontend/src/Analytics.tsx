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

// Processamento de dados (Deduplicação e Cálculos)
const processData = (rawData: ChurnData[]) => {
    // 1. Deduplicação por Cliente ID (Regra de Negócio: Visão de Clientes Únicos)
    // Utilizamos um Map para garantir que cada ID seja contado apenas uma vez.
    // Se houver duplicatas, o último registro processado prevalece.
    const uniqueClientsMap = new Map<string, ChurnData>();
    rawData.forEach(client => {
        uniqueClientsMap.set(client.clienteId, client);
    });

    // Dataset limpo apenas com clientes únicos
    const data = Array.from(uniqueClientsMap.values());

    // KPIs Baseados em Clientes Únicos
    const totalClientes = data.length
    const clientesRisco = data.filter(c => c.riscoAlto).length
    // Risco Médio: Probabilidade >= 25% mas ainda não classificado como Alto Risco pelo modelo
    const clientesRiscoMedio = data.filter(c => !c.riscoAlto && c.probabilidade >= 0.25).length
    const taxaChurn = totalClientes > 0 ? (data.reduce((acc, c) => acc + c.probabilidade, 0) / totalClientes) * 100 : 0
    const ticketMedio = totalClientes > 0 ? data.reduce((acc, c) => acc + c.valorMensal, 0) / totalClientes : 0
    const npsMedia = totalClientes > 0 ? data.reduce((acc, c) => acc + c.avaliacaoPlataforma, 0) / totalClientes : 0

    // Distribuição por Região
    const porRegiao = data.reduce((acc, c) => {
        acc[c.regiao] = (acc[c.regiao] || 0) + 1
        return acc
    }, {} as Record<string, number>)

    // Distribuição por Plano
    const porPlano = data.reduce((acc, c) => {
        acc[c.planoAssinatura] = (acc[c.planoAssinatura] || 0) + 1
        return acc
    }, {} as Record<string, number>)

    // Top 10 em Risco
    const topRisco = [...data]
        .sort((a, b) => b.probabilidade - a.probabilidade)
        .slice(0, 10)

    // Churn por Região
    const churnPorRegiao = Object.entries(porRegiao).map(([regiao, total]) => {
        const emRisco = data.filter(c => c.regiao === regiao && c.riscoAlto).length
        return { regiao, total, emRisco, taxa: (emRisco / total) * 100 }
    }).sort((a, b) => b.taxa - a.taxa)

    return {
        kpis: { totalClientes, clientesRisco, clientesRiscoMedio, taxaChurn, ticketMedio, npsMedia },
        porRegiao,
        porPlano,
        topRisco,
        churnPorRegiao
    }
}

export default function Analytics({ slim = false }: { slim?: boolean }) {
    const { data, loading } = useQuery(GET_ANALYTICS_DATA, { pollInterval: 0 })

    if (loading) return (
        <div className="flex flex-col items-center justify-center p-6 min-h-[400px]">
            <div className="loading-spinner"></div>
            <p className="mt-4 text-muted-foreground animate-pulse">Carregando dashboard...</p>
        </div>
    )

    if (!data?.listarAnalises || data.listarAnalises.length === 0) {
        return <div className="card p-6"><h3>📊 Dashboard Analytics</h3><p className="text-muted-foreground">Sem dados para análise. Execute algumas previsões primeiro.</p></div>
    }

    const analytics = processData(data.listarAnalises)
    const { kpis, porPlano, topRisco, churnPorRegiao } = analytics

    // Cores (CSS Variables controlam agora, mas mantemos refs para gráficos JS)
    const chartColors = ['#34c759', '#5ac8fa', '#ff9500', '#ff3b30']

    // Se estiver em modo slim (sidebar), mostramo apenas KPIs resumidos empilhados ou grid menor
    if (slim) {
        return (
            <div className="flex flex-col gap-4 h-full overflow-y-auto">
                {/* KPIs Compactos */}
                <div className="grid grid-cols-2 gap-3">
                    <div className="card p-4 bg-accent/10 border-accent/20">
                        <div className="text-xs font-semibold text-accent uppercase">Total</div>
                        <div className="text-xl font-bold">{kpis.totalClientes}</div>
                    </div>
                    <div className="card p-4 bg-warning/10 border-warning/20">
                        <div className="text-xs font-semibold text-warning uppercase">Churn</div>
                        <div className="text-xl font-bold">{kpis.taxaChurn.toFixed(1)}%</div>
                    </div>
                </div>

                {/* Lista Simplificada de Risco */}
                <div className="flex-1">
                    <h4 className="text-sm font-semibold mb-3">Top Risco</h4>
                    <div className="flex flex-col gap-2">
                        {topRisco.slice(0, 5).map((c, i) => {
                            let riskLabel = "Baixo";
                            let riskColor = "text-success";
                            if (c.probabilidade > 0.6) { riskLabel = "CRÍTICO"; riskColor = "text-danger"; }
                            else if (c.probabilidade > 0.42) { riskLabel = "ALTO"; riskColor = "text-warning"; }

                            return (
                                <div key={i} className="flex justify-between items-center text-sm p-3 bg-input-bg rounded-lg border-l-4 mb-2"
                                    style={{ borderLeftColor: c.probabilidade > 0.42 ? (c.probabilidade > 0.6 ? '#ff3b30' : '#ff9500') : '#34c759' }}>
                                    <div className="flex flex-col overflow-hidden mr-3">
                                        <span className="font-mono text-xs font-bold truncate pr-2">{c.clienteId}</span>
                                        <span className="text-[10px] text-muted-foreground uppercase truncate phone:hidden">{c.regiao} • {c.planoAssinatura}</span>
                                    </div>
                                    <div className="text-right flex-shrink-0 flex flex-col items-end min-w-[60px]">
                                        <span className={`font-bold ${riskColor} text-[10px] uppercase tracking-wide mb-0.5 block`}>{riskLabel}</span>
                                        <span className="font-bold text-sm">{(c.probabilidade * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>

                {/* Mini Churn por Região */}
                <div className="flex-1 mt-6 border-t border-border pt-4">
                    <h4 className="text-sm font-semibold mb-4 flex items-center gap-2">
                        <span>🌍 Risco Região</span>
                    </h4>
                    <div className="flex flex-col gap-4 pr-1">
                        {churnPorRegiao.map((r, i) => (
                            <div key={i} className="text-xs">
                                <div className="flex justify-between items-center mb-1.5 ">
                                    <span className="font-medium text-muted-foreground">{r.regiao}</span>
                                    <span className={`font-bold ${r.taxa > 42 ? 'text-danger' : 'text-success'}`}>
                                        {r.taxa.toFixed(0)}%
                                    </span>
                                </div>
                                <div className="h-2 w-full bg-input-bg rounded-full overflow-hidden border border-border/50">
                                    <div
                                        className="h-full rounded-full transition-all duration-500 shadow-sm"
                                        style={{ width: `${r.taxa}%`, background: r.taxa > 42 ? '#ff3b30' : '#34c759' }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        )
    }

    // Modo Full Dashboard (Grid Lovable)
    return (
        <div className="flex flex-col gap-6 h-full">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <span className="text-lg font-semibold">📊 Dashboard Analytics</span>
                </div>
                <span className="bg-success/10 text-success border border-success/20 px-3 py-1 rounded-full text-xs font-bold animate-pulse">
                    LIVE
                </span>
            </div>

            {/* KPI Cards Grid (6 colunas) */}
            <div className="grid-cols-6">
                {/* Total */}
                <div className="card p-4 border-l-4 border-l-accent">
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Total Analisados</div>
                    <div className="text-2xl font-bold">{kpis.totalClientes.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground mt-1">clientes</div>
                </div>

                {/* Churn */}
                <div className="card p-4 border-l-4 border-l-warning">
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Taxa de Churn</div>
                    <div className="text-2xl font-bold text-warning">{kpis.taxaChurn.toFixed(1)}%</div>
                    <div className="text-xs text-muted-foreground mt-1">média geral</div>
                </div>

                {/* Risco Médio */}
                <div className="card p-4 border-l-4 border-l-warning" style={{ borderLeftColor: '#ff9500' }}>
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Risco Médio</div>
                    <div className="text-2xl font-bold" style={{ color: '#ff9500' }}>{kpis.clientesRiscoMedio.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground mt-1">atenção necessária</div>
                </div>

                {/* Risco */}
                <div className="card p-4 border-l-4 border-l-danger">
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Alto Risco</div>
                    <div className="text-2xl font-bold text-danger">{kpis.clientesRisco.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground mt-1">clientes críticos</div>
                </div>

                {/* Ticket */}
                <div className="card p-4 border-l-4 border-l-success">
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Ticket Médio</div>
                    <div className="text-2xl font-bold text-success">R$ {kpis.ticketMedio.toFixed(0)}</div>
                    <div className="text-xs text-muted-foreground mt-1">por cliente</div>
                </div>

                {/* NPS */}
                <div className="card p-4 border-l-4 border-l-dark">
                    <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">NPS Médio</div>
                    <div className="text-2xl font-bold text-foreground">{kpis.npsMedia.toFixed(1)}</div>
                    <div className="text-xs text-muted-foreground mt-1">satisfação</div>
                </div>
            </div>

            {/* Charts Row (2 colunas) */}
            <div className="grid-cols-2 gap-6 flex-1 min-h-0">
                {/* Pizza */}
                <div className="card p-6 flex flex-col items-center justify-center">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-6 uppercase tracking-wider self-start">Distribuição por Plano</h4>
                    {Object.keys(porPlano).length > 0 ? (
                        <PieChart data={porPlano} colors={chartColors} />
                    ) : (
                        <p className="text-muted-foreground">Sem dados</p>
                    )}
                </div>

                {/* Lista de Risco */}
                <div className="card p-6 flex flex-col overflow-hidden">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-4 uppercase tracking-wider">Top 10 Clientes em Risco</h4>
                    <div className="flex-col gap-2 overflow-y-auto pr-2">
                        {topRisco.map((cliente, i) => (
                            <div key={i} className="flex justify-between items-center p-3 bg-bg-app rounded-lg border-l-4"
                                style={{ borderLeftColor: cliente.probabilidade > 0.7 ? '#ff3b30' : '#ff9500' }}>
                                <div>
                                    <div className="text-sm font-semibold flex items-center gap-2">
                                        {cliente.clienteId}
                                        <span className="text-[10px] bg-input-bg border border-border px-1.5 py-0.5 rounded text-muted-foreground uppercase tracking-wider">
                                            {cliente.modeloUsado || 'AI'}
                                        </span>
                                    </div>
                                    <div className="text-xs text-muted-foreground uppercase">{cliente.planoAssinatura}</div>
                                </div>
                                <div className="text-right">
                                    <div className="font-bold text-danger">
                                        {(cliente.probabilidade * 100).toFixed(1)}%
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                        R$ {cliente.valorMensal.toFixed(0)}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Tabela Região (Full Width) */}
            <div className="card p-6">
                <h4 className="text-sm font-semibold text-muted-foreground mb-4 uppercase tracking-wider">Churn por Região</h4>
                <div className="flex flex-col gap-3">
                    {churnPorRegiao.map((item, i) => (
                        <div key={i}>
                            <div className="flex justify-between mb-1">
                                <span className="text-sm font-medium">{item.regiao}</span>
                                <span className="text-sm font-bold text-muted-foreground">
                                    {item.emRisco} / {item.total} <span className={item.taxa > 0 ? 'text-danger' : 'text-success'}>({item.taxa.toFixed(1)}%)</span>
                                </span>
                            </div>
                            <div className="h-2 w-full bg-input-bg rounded-full overflow-hidden">
                                <div className="h-full rounded-full transition-all duration-1000 ease-out"
                                    style={{
                                        width: `${item.taxa}%`,
                                        background: 'linear-gradient(90deg, #ff9500, #ff3b30)'
                                    }}>
                                </div>
                            </div>
                        </div>
                    ))}
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
