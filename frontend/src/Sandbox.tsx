import { useState } from 'react'
import { fakerPT_BR as faker } from '@faker-js/faker'

// Utilitário para gerar CSV no navegador
const generateFakeData = (count: number) => {
    const data = []
    const headers = [
        "idade", "tempo_assinatura_meses", "plano_assinatura",
        "valor_mensal", "visualizacoes_mes", "tempo_medio_sessao_min",
        "contatos_suporte", "avaliacao_conteudo", "metodo_pagamento", "dispositivo_principal"
    ]

    for (let i = 0; i < count; i++) {
        data.push([
            faker.number.int({ min: 18, max: 75 }), // idade
            faker.number.int({ min: 1, max: 60 }),  // tempo_assinatura
            faker.helpers.arrayElement(['Basico', 'Standard', 'Premium']), // plano
            faker.finance.amount({ min: 19.90, max: 59.90, dec: 2 }), // valor
            faker.number.int({ min: 0, max: 200 }), // visualizacoes
            faker.number.int({ min: 10, max: 180 }), // sessao
            faker.number.int({ min: 0, max: 5 }), // suporte
            faker.number.float({ min: 1, max: 5, multipleOf: 0.1 }), // avaliacao
            faker.helpers.arrayElement(['credito', 'debito', 'boleto']), // metodo
            faker.helpers.arrayElement(['mobile', 'smart_tv', 'computer']) // dispositivo
        ].join(','))
    }

    return [headers.join(','), ...data].join('\n')
}

export default function Sandbox() {
    const [generatedCount, setGeneratedCount] = useState(100)
    const [isGenerating, setIsGenerating] = useState(false)

    const handleDownloadFake = () => {
        setIsGenerating(true)
        setTimeout(() => {
            const csvContent = generateFakeData(generatedCount)
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
            const url = URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = `simulacao_futura_${generatedCount}_clientes.csv`
            link.click()
            setIsGenerating(false)
        }, 500) // Fake delay
    }

    return (
        <div className="card" style={{ marginTop: '2rem', border: '1px solid #a855f7' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>🧪 Sandbox de Negócios (Business Intelligence)</h3>
                <span style={{ background: '#a855f7', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>BETA</span>
            </div>

            <p style={{ color: '#cbd5e1', marginBottom: '1.5rem' }}>
                Gere cenários hipotéticos baseados em dados sintéticos para projetar o futuro da companhia.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>

                {/* GERADOR */}
                <div style={{ background: 'rgba(168, 85, 247, 0.1)', padding: '1rem', borderRadius: '8px' }}>
                    <h4 style={{ margin: '0 0 1rem 0', color: '#d8b4fe' }}>1. Gerar Massa de Dados</h4>
                    <label>Quantidade de Clientes Virtuais</label>
                    <input
                        type="number"
                        value={generatedCount}
                        onChange={e => setGeneratedCount(Number(e.target.value))}
                        min="10" max="10000"
                    />
                    <button
                        onClick={handleDownloadFake}
                        style={{ width: '100%', background: '#a855f7' }}
                        disabled={isGenerating}
                    >
                        {isGenerating ? "Gerando..." : "📥 Baixar Dataset Sintético"}
                    </button>
                </div>

                {/* INSIGHTS */}
                <div>
                    <h4 style={{ margin: '0 0 1rem 0' }}>2. O que fazer com isso?</h4>
                    <ul style={{ paddingLeft: '1.2rem', color: '#94a3b8', fontSize: '0.9rem' }}>
                        <li style={{ marginBottom: '0.5rem' }}>Use o arquivo gerado no <strong>Processamento em Lote</strong> acima.</li>
                        <li style={{ marginBottom: '0.5rem' }}>Analise como o modelo se comporta com perfis extremos (ex: gere mil idosos com plano Premium).</li>
                        <li>Valide estratégias de pricing antes de aplicar na base real.</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
