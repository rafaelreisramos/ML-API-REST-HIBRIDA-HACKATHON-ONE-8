import { useState, useEffect, useRef } from 'react'
import { useQuery, gql, useMutation } from '@apollo/client'
import Analytics from './Analytics'
import { useAuth } from './context/AuthContext'
import { LoginPage } from './components/LoginPage'
import { fetchWithAuth } from './utils/api'

// Queries
const GET_STATS = gql`
  query GetStats {
    listarAnalises {
        clienteId
        riscoAlto
    }
  }
`

const ANALYZE_SCENARIO = gql`
  mutation RegistrarAnalise($input: ChurnInput!) {
    registrarAnalise(input: $input) {
      previsao
      probabilidade
      riscoAlto
      modeloUsado
    }
  }
`

function App() {
    // Auth check
    const { isAuthenticated, logout } = useAuth()

    // Se não autenticado, mostrar tela de login
    if (!isAuthenticated) {
        return <LoginPage />
    }

    // 1. Theme & Tabs State
    const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')
    const [activeTab, setActiveTab] = useState('simulador')

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme)
        localStorage.setItem('theme', theme)
    }, [theme])

    const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light')

    // 2. Stats
    const { data: statsRaw, loading: statsLoading, refetch } = useQuery(GET_STATS, { pollInterval: 0 })

    // Derived stats
    const total = statsRaw?.listarAnalises?.length || 0
    const risk = statsRaw?.listarAnalises?.filter((a: any) => a.riscoAlto).length || 0
    const riskRate = total > 0 ? ((risk / total) * 100).toFixed(1) : "0.0"

    // 3. Simulator State
    const [formData, setFormData] = useState({
        clienteId: "APPLE-USER-01", idade: 30, genero: "Masculino", regiao: "Sudeste",
        tempoAssinaturaMeses: 12, planoAssinatura: "padrao", valorMensal: 29.90,
        visualizacoesMes: 20, tempoMedioSessaoMin: 45, contatosSuporte: 0,
        avaliacaoConteudoMedia: 4.0, avaliacaoConteudoUltimoMes: 4.0, avaliacaoPlataforma: 4.0,
        diasUltimoAcesso: 1, metodoPagamento: "credito", dispositivoPrincipal: "mobile",
        tipoContrato: "MENSAL", categoriaFavorita: "FILMES", acessibilidade: 0
    })

    // Campos derivados calculados automaticamente (features importantes do modelo)
    const engajamentoScore = Math.min(100, Math.round(
        (formData.visualizacoesMes * 2) +
        (formData.tempoMedioSessaoMin * 0.5) +
        (formData.avaliacaoConteudoMedia * 10) -
        (formData.diasUltimoAcesso * 3)
    ))
    const visualizacoesPorDia = (formData.visualizacoesMes / 30).toFixed(1)

    const [analyze, { data: simData, loading: simLoading }] = useMutation(ANALYZE_SCENARIO, {
        update(cache, { data: { registrarAnalise } }) {
            // Atualizar Cache de Estatísticas Gerais (GET_STATS)
            try {
                const existingStats: any = cache.readQuery({ query: GET_STATS });
                if (existingStats && existingStats.listarAnalises) {
                    cache.writeQuery({
                        query: GET_STATS,
                        data: {
                            listarAnalises: [...existingStats.listarAnalises, registrarAnalise]
                        },
                    });
                }
            } catch (e) {
                // Ignore cache errors if query hasn't run yet
            }

            // Atualizar Cache Detalhado (GET_ANALYTICS_DATA) - Usado pelo Analytics Component
            // Precisamos reconstruir o objeto completo pois a mutation retorna apenas alguns campos
            // Mas para o monitoramento rápido, o update acima já ajuda. O ideal é refetch ou update completo.
            // Para garantir consistência total "instantânea":
            refetch(); // Força update da query principal em background
        }
    })

    // 4. Batch Upload State
    const [uploading, setUploading] = useState(false)
    const [uploadStatus, setUploadStatus] = useState("")
    const [batchProgress, setBatchProgress] = useState({ initial: 0, current: 0, isMonitoring: false })

    // Refs para controle de cancelamento
    const abortControllerRef = useRef<AbortController | null>(null)
    const progressIntervalRef = useRef<any>(null)

    const cancelUpload = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort()
        }
        if (progressIntervalRef.current) {
            clearInterval(progressIntervalRef.current)
        }
        setUploading(false)
        setUploadStatus("⚠️ Upload cancelado pelo usuário.")
        setBatchProgress({ initial: 0, current: 0, isMonitoring: false })
    }

    const handleBatchUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files?.length) return
        const file = e.target.files[0]

        const data = new FormData()
        data.append('file', file)

        setUploading(true)
        setUploadStatus("Iniciando upload de alta performance...")

        // Capturar contagem inicial para monitorar progresso
        const initialCount = statsRaw?.listarAnalises?.length || 0
        setBatchProgress({ initial: initialCount, current: 0, isMonitoring: true })

        // Iniciar polling para monitorar progresso
        // Configurar AbortController
        abortControllerRef.current = new AbortController()

        // Iniciar polling para monitorar progresso
        progressIntervalRef.current = setInterval(() => {
            refetch().then((result) => {
                const newCount = result.data?.listarAnalises?.length || 0
                const processed = newCount - initialCount
                setBatchProgress(prev => ({ ...prev, current: processed }))
                setUploadStatus(`Processando: ${processed} registros...`)
            })
        }, 2000) // Poll a cada 2 segundos

        try {
            // USANDO ENDPOINT OTIMIZADO PARA 50K LINHAS com autenticação do contexto
            const res = await fetchWithAuth('/api/churn/batch/optimized', {
                method: 'POST',
                body: data,
                signal: abortControllerRef.current.signal
            })

            if (progressIntervalRef.current) clearInterval(progressIntervalRef.current)

            if (res.ok) {
                const blob = await res.blob()
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `resultado_batch_${file.name}`
                a.click()

                // Atualizar contagem final
                await refetch()
                const finalCount = statsRaw?.listarAnalises?.length || 0
                const totalProcessed = finalCount - initialCount
                setUploadStatus(`✅ Processamento concluído! ${totalProcessed} registros analisados.`)
            } else {
                setUploadStatus("Erro no servidor. Verifique o formato do CSV.")
            }
        } catch (err: any) {
            if (progressIntervalRef.current) clearInterval(progressIntervalRef.current)
            if (err.name === 'AbortError') {
                console.log('Upload aborted');
            } else {
                setUploadStatus("Erro de conexão ou timeout.")
            }
        } finally {
            setUploading(false)
            setBatchProgress({ initial: 0, current: 0, isMonitoring: false })
            abortControllerRef.current = null
        }
    }

    return (
        <div className="container">
            {/* Header */}
            <header>
                <div className="logo" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ background: 'var(--accent)', color: 'white', width: 36, height: 36, borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem' }}>C</div>
                    ChurnInsight <span style={{ fontSize: '0.7rem', opacity: 0.6, border: '1px solid currentColor', padding: '2px 6px', borderRadius: 4 }}>V8 PRO</span>
                </div>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <button onClick={toggleTheme} className="theme-toggle">
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>
                    <button className="theme-toggle" style={{ color: 'var(--error)', borderColor: 'var(--error)' }}
                        onClick={async () => {
                            if (confirm("ATENÇÃO: Isso apagará TODOS os dados do banco de dados.\n\nDeseja continuar?")) {
                                try {
                                    const res = await fetchWithAuth('/api/churn/reset', { method: 'DELETE' });
                                    if (res.ok) {
                                        localStorage.removeItem('apollo-cache-persist');
                                        alert("Sistema resetado com sucesso!");
                                        window.location.reload();
                                    } else if (res.status === 403) {
                                        alert("⚠️ Acesso Negado (403)\\n\\nO endpoint /reset está bloqueado.\\nContate o administrador do backend.");
                                        console.error("Reset endpoint forbidden (403). Check SecurityConfig.java");
                                    } else {
                                        alert("Erro ao resetar: " + res.statusText);
                                        console.error("Reset failed", res);
                                    }
                                } catch (e) {
                                    alert("Erro de conexão ao tentar resetar.");
                                    console.error(e);
                                }
                            }
                        }}>
                        Reset
                    </button>
                    {isAuthenticated && (
                        <button className="theme-toggle" onClick={logout} style={{ color: 'var(--text-secondary)' }}>
                            Sair
                        </button>
                    )}
                </div>
            </header>

            {/* Global Statistics Panel */}
            <section style={{
                background: 'linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%)',
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '20px',
                color: 'white',
                boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: '600', color: 'white' }}>📊 Estatísticas Globais da API</h3>
                    <span style={{
                        background: 'rgba(255,255,255,0.2)',
                        padding: '4px 12px',
                        borderRadius: '20px',
                        fontSize: '0.75rem',
                        fontWeight: '600'
                    }}>LIVE</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
                    <div style={{ background: 'rgba(255,255,255,0.15)', padding: '15px', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '5px' }}>TOTAL PROCESSADO</div>
                        <div style={{ fontSize: '2rem', fontWeight: '800' }}>{total.toLocaleString()}</div>
                        <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>registros analisados</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.15)', padding: '15px', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '5px' }}>CLIENTES ÚNICOS</div>
                        <div style={{ fontSize: '2rem', fontWeight: '800' }}>
                            {new Set(statsRaw?.listarAnalises?.map((a: any) => a.clienteId) || []).size}
                        </div>
                        <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>IDs distintos</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.15)', padding: '15px', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '5px' }}>EM RISCO ALTO</div>
                        <div style={{ fontSize: '2rem', fontWeight: '800', color: '#fbbf24' }}>{risk}</div>
                        <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>{riskRate}% da base</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.15)', padding: '15px', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.75rem', opacity: 0.9, marginBottom: '5px' }}>ÚLTIMA ATUALIZAÇÃO</div>
                        <div style={{ fontSize: '1.2rem', fontWeight: '700' }}>{new Date().toLocaleTimeString('pt-BR')}</div>
                        <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>{new Date().toLocaleDateString('pt-BR')}</div>
                    </div>
                </div>
            </section>

            {/* Layout Principal - Condicional baseado na aba */}
            {activeTab === 'dashboard' ? (
                // Layout Full-Screen para Dashboard
                <div style={{ marginTop: '20px' }}>
                    <div className="tabs" style={{ marginBottom: '20px' }}>
                        <button className={`tab-btn ${activeTab === 'simulador' ? 'active' : ''}`} onClick={() => setActiveTab('simulador')}>Simulador Individual</button>
                        <button className={`tab-btn ${activeTab === 'batch' ? 'active' : ''}`} onClick={() => setActiveTab('batch')}>Processamento Batch</button>
                        <button className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>📊 Dashboard Analytics</button>
                    </div>
                    <Analytics />
                </div>
            ) : (
                // Layout Lovable Structure: Sidebar Fixed (w-80) + Content Liquid (flex-1)
                <div className="flex gap-6 items-start">

                    {/* Coluna Esquerda: Abas + Conteúdo (W-80 Fixed) */}
                    <div className="w-80 flex-shrink-0 flex flex-col gap-4">
                        <div className="tabs">
                            <button className={`tab-btn ${activeTab === 'simulador' ? 'active' : ''}`} onClick={() => setActiveTab('simulador')}>Simulador</button>
                            <button className={`tab-btn ${activeTab === 'batch' ? 'active' : ''}`} onClick={() => setActiveTab('batch')}>Batch</button>
                            <button className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>📊 Dash</button>
                        </div>

                        {activeTab === 'simulador' && (
                            <div className="card" style={{ padding: '20px' }}>
                                <h3 style={{ fontSize: '1rem', marginTop: 0 }}>Simulador Real-Time</h3>
                                <form onSubmit={e => { e.preventDefault(); analyze({ variables: { input: formData } }) }}>
                                    {/* Form Grid Compacto - 2 Colunas mas labels menores */}
                                    {/* Form Grid Compacto - 2 Colunas mas labels menores */}
                                    {/* SEÇÃO 1: FATORES CRÍTICOS (ALTO PESO NA IA) */}
                                    <div className="bg-accent/5 p-4 rounded-lg border border-accent/20 mb-4">
                                        <div className="text-xs font-bold text-accent uppercase tracking-wider mb-4 flex items-center gap-2">
                                            <span>🔥 Fatores de Comportamento (Alto Impacto)</span>
                                        </div>
                                        <div className="grid grid-cols-2 gap-x-4 gap-y-3">
                                            {/* Linha 1 */}
                                            <div className="flex flex-col">
                                                <label className="label-field font-semibold text-accent-foreground text-xs whitespace-nowrap mb-1">T. Sessão (min)</label>
                                                <input className="input-field border-accent/30 w-full" type="number"
                                                    value={formData.tempoMedioSessaoMin}
                                                    onChange={e => setFormData({ ...formData, tempoMedioSessaoMin: +e.target.value })}
                                                />
                                            </div>
                                            <div className="flex flex-col">
                                                <label className="label-field font-semibold text-accent-foreground text-xs whitespace-nowrap mb-1">Dias Inativo</label>
                                                <input className="input-field border-accent/30 w-full" type="number"
                                                    value={formData.diasUltimoAcesso}
                                                    onChange={e => setFormData({ ...formData, diasUltimoAcesso: +e.target.value })}
                                                />
                                            </div>

                                            {/* Linha 2 */}
                                            <div className="flex flex-col">
                                                <label className="label-field font-semibold text-accent-foreground text-xs whitespace-nowrap mb-1">Aval. Conteúdo</label>
                                                <select className="input-field w-full" value={formData.avaliacaoConteudoUltimoMes}
                                                    onChange={e => setFormData({ ...formData, avaliacaoConteudoUltimoMes: +e.target.value, avaliacaoConteudoMedia: +e.target.value })}>
                                                    <option value="1">1 ⭐ (Crítico)</option>
                                                    <option value="2">2 ⭐ (Ruim)</option>
                                                    <option value="3">3 ⭐ (Médio)</option>
                                                    <option value="4">4 ⭐ (Bom)</option>
                                                    <option value="5">5 ⭐ (Excelente)</option>
                                                </select>
                                            </div>
                                            <div className="flex flex-col">
                                                <label className="label-field font-semibold text-accent-foreground text-xs whitespace-nowrap mb-1">Views / Mês</label>
                                                <input className="input-field w-full" type="number"
                                                    value={formData.visualizacoesMes}
                                                    onChange={e => setFormData({ ...formData, visualizacoesMes: +e.target.value })}
                                                />
                                            </div>
                                        </div>

                                        {/* Métricas Calculadas (Auto) */}
                                        <div className="mt-4 pt-3 border-t border-accent/20">
                                            <div className="text-[10px] font-bold text-accent uppercase tracking-wider mb-2">📊 Métricas Calculadas (IA)</div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <div className="bg-accent/10 rounded px-2 py-1.5">
                                                    <div className="text-[9px] text-muted-foreground uppercase tracking-wide">Engajamento</div>
                                                    <div className="text-sm font-bold text-accent">{engajamentoScore}/100</div>
                                                </div>
                                                <div className="bg-accent/10 rounded px-2 py-1.5">
                                                    <div className="text-[9px] text-muted-foreground uppercase tracking-wide">Views/Dia</div>
                                                    <div className="text-sm font-bold text-accent">{visualizacoesPorDia}</div>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Legenda */}
                                        <div className="mt-3 pt-2 border-t border-accent/10 text-[10px] text-muted-foreground grid grid-cols-2 gap-x-2 gap-y-0.5 mb-4">
                                            <span>• T. Sessão: Média min/uso (28%)</span>
                                            <span>• Engajamento: Score IA (26%)</span>
                                            <span>• Aval. Conteúdo: Último mês (9%)</span>
                                            <span>• Views/Mês: Total assistido (8%)</span>
                                            <span>• Views/Dia: Frequência (7%)</span>
                                            <span>• Dias Inativo: Recência (4%)</span>
                                        </div>
                                    </div>

                                    {/* SEÇÃO 2: DADOS CADASTRAIS (BAIXO PESO) */}
                                    <div className="opacity-80">
                                        <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Dados Cadastrais (Secundário)</div>
                                        <div className="grid grid-cols-3 gap-2 text-sm">
                                            <div className="col-span-3">
                                                <label className="label-field text-xs">ID Cliente</label>
                                                <input className="input-field py-1 text-xs" value={formData.clienteId} onChange={e => setFormData({ ...formData, clienteId: e.target.value })} />
                                            </div>

                                            <div>
                                                <label className="label-field text-xs">Plano</label>
                                                <select className="input-field py-1 text-xs" value={formData.planoAssinatura} onChange={e => setFormData({ ...formData, planoAssinatura: e.target.value })}>
                                                    <option value="basico">Básico</option><option value="padrao">Padrão</option><option value="premium">Premium</option>
                                                </select>
                                            </div>
                                            <div>
                                                <label className="label-field text-xs">Valor</label>
                                                <input className="input-field py-1 text-xs" type="number" value={formData.valorMensal} onChange={e => setFormData({ ...formData, valorMensal: +e.target.value })} />
                                            </div>
                                            <div>
                                                <label className="label-field text-xs">Contrato</label>
                                                <select className="input-field py-1 text-xs" value={formData.tipoContrato} onChange={e => setFormData({ ...formData, tipoContrato: e.target.value })}>
                                                    <option>MENSAL</option><option>ANUAL</option>
                                                </select>
                                            </div>

                                            {/* Campos Ocultáveis/Menores */}
                                            <div>
                                                <label className="label-field text-xs">Idade</label>
                                                <input className="input-field py-1 text-xs" type="number" value={formData.idade} onChange={e => setFormData({ ...formData, idade: +e.target.value })} />
                                            </div>
                                            <div>
                                                <label className="label-field text-xs">Gênero</label>
                                                <select className="input-field py-1 text-xs" value={formData.genero} onChange={e => setFormData({ ...formData, genero: e.target.value })}>
                                                    <option>Masculino</option><option>Feminino</option>
                                                </select>
                                            </div>
                                            <div>
                                                <label className="label-field text-xs">Região</label>
                                                <div className="text-xs font-mono p-2 bg-input-bg rounded border border-border text-muted-foreground truncate">{formData.regiao}</div>
                                            </div>
                                        </div>
                                    </div>

                                    <button type="submit" disabled={simLoading} className="w-full bg-primary hover:bg-primary/90 text-white font-semibold py-3 px-4 rounded-xl mt-4 transition-colors">
                                        {simLoading ? "Calculando..." : "Analisar Risco"}
                                    </button>
                                </form>

                                {simData?.registrarAnalise && (
                                    <div className={`result-box ${simData.registrarAnalise.riscoAlto ? 'result-risk' : 'result-safe'}`} style={{ marginTop: '15px', padding: '15px' }}>
                                        <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>{(simData.registrarAnalise.probabilidade * 100).toFixed(1)}%</div>
                                        <div style={{ fontSize: '0.9rem' }}>{simData.registrarAnalise.previsao}</div>
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'batch' && (
                            <div className="card">
                                <h3>Processamento em Lote (High Performance)</h3>
                                <p style={{ marginBottom: '20px', color: 'var(--text-secondary)' }}>
                                    Utilize este módulo para processar arquivos CSV grandes (até 50.000 linhas).
                                    O sistema utiliza paralelismo para inferência rápida.
                                </p>

                                {!uploading ? (
                                    <label className="upload-area" style={{ height: '220px', cursor: 'pointer' }}>
                                        <input type="file" accept=".csv" hidden onChange={handleBatchUpload} disabled={uploading} />
                                        <div style={{ textAlign: 'center', width: '100%' }}>
                                            <div style={{ fontSize: '3rem', marginBottom: '10px' }}>📂</div>
                                            <div style={{ fontWeight: '600', fontSize: '1.1rem' }}>
                                                Carregar CSV (Drag & Drop)
                                            </div>
                                            <div style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
                                                {uploadStatus || "Suporta arquivos padrão V8 (até 50k linhas)"}
                                            </div>
                                        </div>
                                    </label>
                                ) : (
                                    <div className="upload-area" style={{ height: '220px', cursor: 'default', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                                        <div className="loading-spinner" style={{ margin: '0 auto 15px' }}></div>
                                        <div style={{ fontWeight: '600', fontSize: '1.2rem', marginBottom: '5px' }}>
                                            Processando Lote...
                                        </div>
                                        <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--accent)' }}>
                                            {batchProgress.current.toLocaleString()}
                                        </div>
                                        <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
                                            registros analisados em tempo real
                                        </div>
                                        {/* Visual Progress Bar (Indeterminate) */}
                                        <div style={{
                                            width: '200px',
                                            height: '6px',
                                            background: 'rgba(255,255,255,0.1)',
                                            borderRadius: '3px',
                                            margin: '15px auto 0',
                                            overflow: 'hidden',
                                            position: 'relative'
                                        }}>
                                            <div style={{
                                                position: 'absolute',
                                                left: 0,
                                                top: 0,
                                                height: '100%',
                                                width: '50%',
                                                background: 'var(--accent)',
                                                borderRadius: '3px',
                                                animation: 'indeterminate 1.5s infinite linear'
                                            }}></div>
                                        </div>
                                        <style>{`
                                            @keyframes indeterminate {
                                                0% { left: -50%; }
                                                100% { left: 100%; }
                                            }
                                        `}</style>

                                        <button
                                            onClick={(e) => {
                                                e.preventDefault();
                                                e.stopPropagation();
                                                cancelUpload();
                                            }}
                                            style={{
                                                marginTop: '20px',
                                                padding: '8px 16px',
                                                background: 'rgba(239, 68, 68, 0.15)',
                                                color: '#ef4444',
                                                border: '1px solid rgba(239, 68, 68, 0.3)',
                                                borderRadius: '6px',
                                                cursor: 'pointer',
                                                fontSize: '0.9rem',
                                                fontWeight: '600',
                                                transition: 'all 0.2s',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '6px'
                                            }}
                                            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.25)'}
                                            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.15)'}
                                        >
                                            🛑 Cancelar Operação
                                        </button>
                                    </div>
                                )}

                                <div style={{ marginTop: '20px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                    * O endpoint <code>/batch/optimized</code> será usado.
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Coluna Direita: Conteúdo Principal (Liquid) Container */}
                    <div className="flex-1 min-w-0">
                        {activeTab === 'dashboard' ? (
                            <Analytics />
                        ) : (
                            // Modo "Slim" / Resumo quando usando outra ferramenta
                            <div className="card p-6 h-full border-border">
                                <div className="flex justify-between items-center mb-6">
                                    <div>
                                        <h3 className="m-0 text-lg font-semibold">Monitoramento</h3>
                                        <p className="text-sm text-muted-foreground">Acompanhe os resultados em tempo real.</p>
                                    </div>
                                    <button className="text-sm text-accent hover:underline cursor-pointer bg-transparent border-0" onClick={() => setActiveTab('dashboard')}>
                                        Expandir 📊
                                    </button>
                                </div>
                                <Analytics slim={true} />
                            </div>
                        )}
                    </div>

                </div>
            )}
        </div>
    )
}

export default App
