import { useState, useEffect } from 'react'
import { useQuery, gql, useMutation } from '@apollo/client'
import Analytics from './Analytics'

// Queries
const GET_STATS = gql`
  query GetStats {
    listarAnalises {
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

    const [analyze, { data: simData, loading: simLoading }] = useMutation(ANALYZE_SCENARIO)

    // 4. Batch Upload State
    const [uploading, setUploading] = useState(false)
    const [uploadStatus, setUploadStatus] = useState("")

    const handleBatchUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files?.length) return
        const file = e.target.files[0]

        const data = new FormData()
        data.append('file', file)

        setUploading(true)
        setUploadStatus("Iniciando upload de alta performance...")

        try {
            // USANDO ENDPOINT OTIMIZADO PARA 50K LINHAS
            const res = await fetch('/api/churn/batch/optimized', {
                method: 'POST',
                body: data
            })

            if (res.ok) {
                const blob = await res.blob()
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `resultado_batch_${file.name}`
                a.click()
                setUploadStatus("Processamento concluído! Download iniciado.")
                refetch()
            } else {
                setUploadStatus("Erro no servidor. Verifique o formato do CSV.")
            }
        } catch (err) {
            setUploadStatus("Erro de conexão ou timeout.")
        } finally {
            setUploading(false)
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
                            if (confirm("Limpar TUDO?")) {
                                await fetch('/api/churn/reset', { method: 'DELETE' });
                                window.location.href = window.location.origin;
                            }
                        }}>
                        Reset
                    </button>
                </div>
            </header>

            {/* KPI Cards */}
            <section className="grid">
                <div className="card">
                    <div className="stat-label">Total Analisado</div>
                    <div className="stat-value">{statsLoading ? "-" : total}</div>
                </div>
                <div className="card">
                    <div className="stat-label">Alto Risco</div>
                    <div className="stat-value high-risk">{statsLoading ? "-" : risk}</div>
                </div>
                <div className="card">
                    <div className="stat-label">Taxa de Churn</div>
                    <div className="stat-value">{statsLoading ? "-" : riskRate}%</div>
                </div>
            </section>

            {/* Layout Principal */}
            <div className="grid" style={{ gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)', alignItems: 'start' }}>

                {/* Coluna Esquerda: Abas + Conteúdo */}
                <div>
                    <div className="tabs">
                        <button className={`tab-btn ${activeTab === 'simulador' ? 'active' : ''}`} onClick={() => setActiveTab('simulador')}>Simulador Individual</button>
                        <button className={`tab-btn ${activeTab === 'batch' ? 'active' : ''}`} onClick={() => setActiveTab('batch')}>Processamento Batch (Massivo)</button>
                    </div>

                    {activeTab === 'simulador' && (
                        <div className="card">
                            <h3>Simulador Real-Time</h3>
                            <form onSubmit={e => { e.preventDefault(); analyze({ variables: { input: formData } }) }}>
                                {/* Form Grid Compacto */}
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                                    <div><label>ID Cliente</label><input value={formData.clienteId} onChange={e => setFormData({ ...formData, clienteId: e.target.value })} /></div>
                                    <div><label>Idade</label><input type="number" value={formData.idade} onChange={e => setFormData({ ...formData, idade: +e.target.value })} /></div>

                                    <div><label>Gênero</label>
                                        <select value={formData.genero} onChange={e => setFormData({ ...formData, genero: e.target.value })}>
                                            <option>Masculino</option><option>Feminino</option>
                                        </select>
                                    </div>
                                    <div><label>Plano</label>
                                        <select value={formData.planoAssinatura} onChange={e => setFormData({ ...formData, planoAssinatura: e.target.value })}>
                                            <option value="basico">Básico</option><option value="padrao">Padrão</option><option value="premium">Premium</option>
                                        </select>
                                    </div>

                                    <div><label>Valor Mensal (R$)</label><input type="number" value={formData.valorMensal} onChange={e => setFormData({ ...formData, valorMensal: +e.target.value })} /></div>
                                    <div><label>Meses Assinatura</label><input type="number" value={formData.tempoAssinaturaMeses} onChange={e => setFormData({ ...formData, tempoAssinaturaMeses: +e.target.value })} /></div>

                                    {/* V8 Fields */}
                                    <div style={{ gridColumn: '1/-1', background: 'var(--input-bg)', padding: '10px', borderRadius: '8px', marginTop: '10px' }}>
                                        <div style={{ fontSize: '0.8rem', fontWeight: '600', marginBottom: '8px', opacity: 0.7 }}>PARÂMETROS V8</div>
                                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
                                            <div><label>Contrato</label>
                                                <select value={formData.tipoContrato} onChange={e => setFormData({ ...formData, tipoContrato: e.target.value })}>
                                                    <option>MENSAL</option><option>ANUAL</option>
                                                </select>
                                            </div>
                                            <div><label>Categoria</label>
                                                <select value={formData.categoriaFavorita} onChange={e => setFormData({ ...formData, categoriaFavorita: e.target.value })}>
                                                    <option>FILMES</option><option>SERIES</option><option>DOCUMENTARIOS</option>
                                                </select>
                                            </div>
                                            <div><label>Acessibilidade</label>
                                                <select value={formData.acessibilidade} onChange={e => setFormData({ ...formData, acessibilidade: +e.target.value })}>
                                                    <option value={0}>Não</option><option value={1}>Sim</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <button type="submit" disabled={simLoading} style={{ marginTop: '20px', width: '100%' }}>
                                    {simLoading ? "Calculando..." : "Analisar Risco de Churn"}
                                </button>
                            </form>

                            {simData?.registrarAnalise && (
                                <div className={`result-box ${simData.registrarAnalise.riscoAlto ? 'result-risk' : 'result-safe'}`}>
                                    <div style={{ fontSize: '2rem', fontWeight: '700' }}>{(simData.registrarAnalise.probabilidade * 100).toFixed(1)}%</div>
                                    <div>{simData.registrarAnalise.previsao}</div>
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

                            <label className="upload-area" style={{ height: '200px' }}>
                                <input type="file" accept=".csv" hidden onChange={handleBatchUpload} disabled={uploading} />
                                <div style={{ textAlign: 'center' }}>
                                    <div style={{ fontSize: '3rem', marginBottom: '10px' }}>📂</div>
                                    <div style={{ fontWeight: '600', fontSize: '1.1rem' }}>
                                        {uploading ? "Processando Lote..." : "Carregar CSV (Drag & Drop)"}
                                    </div>
                                    <div style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
                                        {uploadStatus || "Suporta arquivos padrão V8"}
                                    </div>
                                    {uploading && <div className="loading-spinner" style={{ margin: '20px auto' }}></div>}
                                </div>
                            </label>

                            <div style={{ marginTop: '20px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                * O endpoint <code>/batch/optimized</code> será usado.
                            </div>
                        </div>
                    )}
                </div>

                {/* Coluna Direita: Analytics */}
                <div>
                    <Analytics />
                </div>

            </div>
        </div>
    )
}

export default App
