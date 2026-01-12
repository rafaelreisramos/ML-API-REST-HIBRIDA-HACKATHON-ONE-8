package com.hackathon.churn;

import jakarta.validation.constraints.*;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Data
@Document(collection = "analises_churn") // Nome da coleção no MongoDB
public class ChurnData {

    @Id
    private String id; // MongoDB usa String (ObjectId) por padrão

    private LocalDateTime dataAnalise = LocalDateTime.now();

    // Controle de Arquivamento (Soft Delete)
    private Boolean ativo = true;
    private LocalDateTime dataArquivamento;

    // Dados do Cliente
    @NotBlank(message = "O ID do cliente é obrigatório")
    private String clienteId;

    @Min(value = 18, message = "A idade mínima é 18 anos")
    @Max(value = 120, message = "A idade máxima é 120 anos")
    private Integer idade;

    @NotBlank(message = "O gênero é obrigatório")
    private String genero;

    @NotBlank(message = "A região é obrigatória")
    private String regiao;

    @Positive(message = "O valor mensal deve ser positivo")
    private Double valorMensal;

    @Min(value = 0, message = "Tempo de assinatura não pode ser negativo")
    private Integer tempoAssinaturaMeses;

    @Min(value = 0, message = "Dias de último acesso não pode ser negativo")
    private Integer diasUltimoAcesso;

    // --- Campos do Modelo Legado (Python) ---
    @NotBlank(message = "O plano de assinatura é obrigatório")
    private String planoAssinatura; // basico, padrao, premium

    @NotBlank(message = "O método de pagamento é obrigatório")
    private String metodoPagamento; // credito, boleto, pix

    @NotBlank(message = "O dispositivo principal é obrigatório")
    private String dispositivoPrincipal; // mobile, desktop, tv

    @Min(value = 0)
    private Integer visualizacoesMes;

    @Min(value = 0)
    private Integer contatosSuporte;

    // --- Novos Campos V8 (Integração Hackathon G8) ---
    @NotBlank(message = "O tipo de contrato é obrigatório")
    private String tipoContrato; // "Mensal", "Anual"

    @NotBlank(message = "A categoria favorita é obrigatória")
    private String categoriaFavorita; // "Filmes", "Séries", etc.

    @Min(value = 0, message = "Acessibilidade deve ser 0 ou 1")
    @Max(value = 1, message = "Acessibilidade deve ser 0 ou 1")
    private Integer acessibilidade; // 0 ou 1
    // ------------------------------------------------

    // ----------------------------------------

    @Min(value = 0, message = "A nota mínima é 0")
    @Max(value = 5, message = "A nota máxima é 5")
    private Double avaliacaoPlataforma;

    // Novos campos V4
    @Min(value = 0)
    @Max(value = 5)
    private Double avaliacaoConteudoMedia;

    @Min(value = 0)
    @Max(value = 5)
    private Double avaliacaoConteudoUltimoMes;

    @PositiveOrZero
    private Integer tempoMedioSessaoMin;

    // Resultado da IA
    private String previsao; // "Vai cancelar"
    private Double probabilidade; // 0.85
    private Boolean riscoAlto; // true
    private String modeloUsado; // "V4-RandomForest"
}
