import { useState } from 'react'
import { useQuery, gql, useMutation } from '@apollo/client'
import Sandbox from './Sandbox'

// Queries GraphQL adaptadas para Spring Boot schema
const GET_STATS = gql`
  query GetStats {
    listarAnalises {
      riscoAlto
    }
  }
`

// Nota: O Spring Boot não tem a query "analiseChurn" do Python
// Vamos usar uma mutation para criar análise e retornar resultado
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
    // Estado para Stats
    const { data: statsRaw, loading: statsLoading, refetch } = useQuery(GET_STATS, {
        pollInterval: 5000 // Atualiza a cada 5s
    })

    // Calcular stats manualmente
    const statsData = statsRaw?.listarAnalises ? {
        stats: {
            totalAnalisados: statsRaw.listarAnalises.length,
            totalChurnPrevisto: statsRaw.listarAnalises.filter((a: any) => a.riscoAlto).length,
            taxaRiscoPercentual: ((statsRaw.listarAnalises.filter((a: any) => a.riscoAlto).length / statsRaw.listarAnalises.length) * 100).toFixed(1)
        }
    } : { stats: { totalAnalisados: 0, totalChurnPrevisto: 0, taxaRiscoPercentual: 0 } }

    // Estado para Simulador
    const [formData, setFormData] = useState({
        clienteId: "FRONTEND-TEST",
        idade: 30,
        genero: "Masculino",
        regiao: "Sudeste",
        tempoAssinaturaMeses: 12,
        planoAssinatura: "padrao",
        valorMensal: 29.90,
        visualizacoesMes: 20,
        tempoMedioSessaoMin: 45,
        contatosSuporte: 0,
        avaliacaoConteudoMedia: 4.0,
        avaliacaoConteudoUltimoMes: 4.0,
        avaliacaoPlataforma: 4.0,
        diasUltimoAcesso: 1,
        metodoPagamento: "credito",
        dispositivoPrincipal: "mobile"
    })

    const [analyze, { data: simData, loading: simLoading }] = useMutation(ANALYZE_SCENARIO)

    const handleSimulate = (e: React.FormEvent) => {
        e.preventDefault()
        analyze({ variables: { input: formData } })
    }

    // Estado para Upload
    const [uploading, setUploading] = useState(false)
    const [uploadMsg, setUploadMsg] = useState("")

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) return
        const file = e.target.files[0]

        const formData = new FormData()
        formData.append('file', file)

        setUploading(true)
        setUploadMsg("Enviando...")

        try {
            // NOTA: Endpoint de batch não implementado ainda no Spring Boot
            // Por enquanto, vamos criar registros um a um via REST
            setUploadMsg("⚠️ Processamento em lote ainda não disponível na API Spring Boot. Use o simulador individual.")

            /* Implementação futura quando o endpoint estiver pronto:
            const response = await fetch('/api/churnbatch', {
                method: 'POST',
                body: formData,
            })
            
            if (response.ok) {
                const blob = await response.blob()
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `resultado_${file.name}`
                a.click()
                setUploadMsg("✅ Processado com sucesso! Download iniciado.")
                refetchStats()
            } else {
                setUploadMsg("❌ Erro no processamento.")
            }
            */
        } catch (err) {
            setUploadMsg("❌ Erro de conexão.")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="container">
            <header>
                <div className="logo">ChurnInsight 🔮</div>
                <div style={{ marginLeft: 'auto', fontSize: '0.9rem', color: '#94a3b8' }}>
                    Ambiente: Fase 2 (React + GraphQL + Sandbox)
                </div>
            </header>

            {/* DASHBOARD KPI */}
            <section className="grid">
                <div className="card">
                    <div className="stat-label">Total Analisado</div>
                    <div className="stat-value">
                        {statsLoading ? "..." : statsData?.stats.totalAnalisados}
                    </div>
                </div>
                <div className="card">
                    <div className="stat-label">Risco Previsto</div>
                    <div className="stat-value high-risk">
                        {statsLoading ? "..." : statsData?.stats.totalChurnPrevisto}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Clientes em Perigo</div>
                </div>
                <div className="card">
                    <div className="stat-label">Taxa de Churn</div>
                    <div className="stat-value">
                        {statsLoading ? "..." : statsData?.stats.taxaRiscoPercentual}%
                    </div>
                </div>
            </section>

            <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>

                {/* SIMULADOR */}
                <div className="card">
                    <h3>⚡ Simulador de Cliente</h3>
                    <form onSubmit={handleSimulate}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label>ID Cliente</label>
                                <input type="text" value={formData.clienteId} onChange={e => setFormData({ ...formData, clienteId: e.target.value })} />
                            </div>
                            <div>
                                <label>Idade</label>
                                <input type="number" value={formData.idade} onChange={e => setFormData({ ...formData, idade: +e.target.value })} />
                            </div>
                            <div>
                                <label>Gênero</label>
                                <select value={formData.genero} onChange={e => setFormData({ ...formData, genero: e.target.value })}>
                                    <option>Masculino</option>
                                    <option>Feminino</option>
                                    <option>Outro</option>
                                </select>
                            </div>
                            <div>
                                <label>Região</label>
                                <select value={formData.regiao} onChange={e => setFormData({ ...formData, regiao: e.target.value })}>
                                    <option>Sudeste</option>
                                    <option>Sul</option>
                                    <option>Norte</option>
                                    <option>Nordeste</option>
                                    <option>Centro-Oeste</option>
                                </select>
                            </div>
                            <div>
                                <label>Mensalidade (R$)</label>
                                <input type="number" step="0.01" value={formData.valorMensal} onChange={e => setFormData({ ...formData, valorMensal: +e.target.value })} />
                            </div>
                            <div>
                                <label>Tempo Assinatura (Meses)</label>
                                <input type="number" value={formData.tempoAssinaturaMeses} onChange={e => setFormData({ ...formData, tempoAssinaturaMeses: +e.target.value })} />
                            </div>
                            <div>
                                <label>Plano</label>
                                <select value={formData.planoAssinatura} onChange={e => setFormData({ ...formData, planoAssinatura: e.target.value })}>
                                    <option value="basico">Básico</option>
                                    <option value="padrao">Padrão</option>
                                    <option value="premium">Premium</option>
                                </select>
                            </div>
                            <div>
                                <label>Método Pagamento</label>
                                <select value={formData.metodoPagamento} onChange={e => setFormData({ ...formData, metodoPagamento: e.target.value })}>
                                    <option value="credito">Crédito</option>
                                    <option value="boleto">Boleto</option>
                                    <option value="pix">Pix</option>
                                </select>
                            </div>
                            <div>
                                <label>Dispositivo Principal</label>
                                <select value={formData.dispositivoPrincipal} onChange={e => setFormData({ ...formData, dispositivoPrincipal: e.target.value })}>
                                    <option value="mobile">Mobile</option>
                                    <option value="desktop">Desktop</option>
                                    <option value="tv">Smart TV</option>
                                </select>
                            </div>
                            <div>
                                <label>Visualizações/Mês</label>
                                <input type="number" value={formData.visualizacoesMes} onChange={e => setFormData({ ...formData, visualizacoesMes: +e.target.value })} />
                            </div>
                            <div>
                                <label>Contatos Suporte</label>
                                <input type="number" value={formData.contatosSuporte} onChange={e => setFormData({ ...formData, contatosSuporte: +e.target.value })} />
                            </div>
                            <div>
                                <label>Avaliação Plataforma (0-5)</label>
                                <input type="number" step="0.1" min="0" max="5" value={formData.avaliacaoPlataforma} onChange={e => setFormData({ ...formData, avaliacaoPlataforma: +e.target.value })} />
                            </div>
                            <div>
                                <label>Aval. Conteúdo Média (0-5)</label>
                                <input type="number" step="0.1" min="0" max="5" value={formData.avaliacaoConteudoMedia} onChange={e => setFormData({ ...formData, avaliacaoConteudoMedia: +e.target.value })} />
                            </div>
                            <div>
                                <label>Aval. Conteúdo Último Mês (0-5)</label>
                                <input type="number" step="0.1" min="0" max="5" value={formData.avaliacaoConteudoUltimoMes} onChange={e => setFormData({ ...formData, avaliacaoConteudoUltimoMes: +e.target.value })} />
                            </div>
                            <div>
                                <label>Tempo Médio Sessão (min)</label>
                                <input type="number" value={formData.tempoMedioSessaoMin} onChange={e => setFormData({ ...formData, tempoMedioSessaoMin: +e.target.value })} />
                            </div>
                            <div>
                                <label>Dias Desde Último Acesso</label>
                                <input type="number" value={formData.diasUltimoAcesso} onChange={e => setFormData({ ...formData, diasUltimoAcesso: +e.target.value })} />
                            </div>
                        </div>
                        <button type="submit" disabled={simLoading}>
                            {simLoading ? "Calculando..." : "Simular Impacto"}
                        </button>
                    </form>

                    {simData?.registrarAnalise && (
                        <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: simData.registrarAnalise.riscoAlto ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)', borderRadius: '8px', border: simData.registrarAnalise.riscoAlto ? '1px solid #ef4444' : '1px solid #22c55e' }}>
                            <div style={{ fontWeight: 'bold', fontSize: '1.2rem', color: simData.registrarAnalise.riscoAlto ? '#ef4444' : '#22c55e' }}>
                                {simData.registrarAnalise.previsao}
                            </div>
                            <div>Probabilidade: <strong>{(simData.registrarAnalise.probabilidade * 100).toFixed(1)}%</strong></div>
                            <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>Modelo: {simData.registrarAnalise.modeloUsado}</div>
                        </div>
                    )}
                </div>

                {/* BATCH UPLOAD */}
                <div className="card">
                    <h3>📂 Processamento em Lote</h3>
                    <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
                        Envie um arquivo CSV com milhares de clientes. O sistema processará tudo e retornará o arquivo preenchido com as previsões.
                    </p>

                    <label className="upload-area">
                        <input type="file" accept=".csv" hidden onChange={handleFileUpload} />
                        <span style={{ fontSize: '1.2rem', display: 'block', marginBottom: '0.5rem' }}>
                            {uploading ? "Processando..." : "Clique para selecionar CSV"}
                        </span>
                        <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>
                            {uploadMsg || "Suporta arquivos grandes"}
                        </span>
                    </label>
                </div>

            </div>

            {/* SANDBOX SECTION */}
            <Sandbox />

        </div>
    )
}

export default App
