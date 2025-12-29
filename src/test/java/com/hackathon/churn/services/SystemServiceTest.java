package com.hackathon.churn.services;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.Repository.ChurnRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("SystemService - Testes Unitários")
class SystemServiceTest {

    @Mock
    private ChurnRepository repository;

    @InjectMocks
    private SystemService systemService;

    private ChurnData clienteRiscoAlto;
    private ChurnData clienteRiscoBaixo;

    @BeforeEach
    void setUp() {
        clienteRiscoAlto = new ChurnData();
        clienteRiscoAlto.setClienteId("CLI-001");
        clienteRiscoAlto.setRiscoAlto(true);
        clienteRiscoAlto.setProbabilidade(0.85);
        clienteRiscoAlto.setPrevisao("Churn");
        clienteRiscoAlto.setPlanoAssinatura("basico");
        clienteRiscoAlto.setRegiao("Sudeste");

        clienteRiscoBaixo = new ChurnData();
        clienteRiscoBaixo.setClienteId("CLI-002");
        clienteRiscoBaixo.setRiscoAlto(false);
        clienteRiscoBaixo.setProbabilidade(0.15);
        clienteRiscoBaixo.setPrevisao("Não Churn");
        clienteRiscoBaixo.setPlanoAssinatura("premium");
        clienteRiscoBaixo.setRegiao("Sul");
    }

    @Test
    @DisplayName("Health check deve retornar status UP")
    void healthCheckDeveRetornarStatusUp() {
        // Arrange
        when(repository.count()).thenReturn(100L);

        // Act
        Map<String, Object> resultado = systemService.healthCheck();

        // Assert
        assertNotNull(resultado);
        assertEquals("UP", resultado.get("status"));
        assertEquals("ChurnInsight API", resultado.get("service"));
        assertEquals("2.0.0", resultado.get("version"));
        assertNotNull(resultado.get("timestamp"));
    }

    @Test
    @DisplayName("Health check MongoDB deve mostrar total de documentos")
    void healthCheckMongoDBDeveMostrarTotalDocumentos() {
        // Arrange
        when(repository.count()).thenReturn(500L);

        // Act
        Map<String, Object> resultado = systemService.healthCheck();

        // Assert
        @SuppressWarnings("unchecked")
        Map<String, Object> mongodb = (Map<String, Object>) resultado.get("mongodb");
        assertNotNull(mongodb);
        assertEquals("UP", mongodb.get("status"));
        assertEquals(500L, mongodb.get("totalDocuments"));
    }

    @Test
    @DisplayName("Stats deve calcular totais corretamente")
    void statsDeveCalcularTotaisCorretamente() {
        // Arrange
        List<ChurnData> dados = Arrays.asList(clienteRiscoAlto, clienteRiscoBaixo);
        when(repository.findAll()).thenReturn(dados);

        // Act
        Map<String, Object> resultado = systemService.getStats();

        // Assert
        assertNotNull(resultado);
        assertEquals(2, resultado.get("totalAnalisados"));
        assertEquals(1L, resultado.get("totalRiscoAlto"));
        assertEquals(1L, resultado.get("totalRiscoBaixo"));
    }

    @Test
    @DisplayName("Stats deve calcular taxa de churn percentual")
    void statsDeveCalcularTaxaChurnPercentual() {
        // Arrange
        List<ChurnData> dados = Arrays.asList(clienteRiscoAlto, clienteRiscoBaixo);
        when(repository.findAll()).thenReturn(dados);

        // Act
        Map<String, Object> resultado = systemService.getStats();

        // Assert
        assertEquals(50.0, resultado.get("taxaChurnPercentual"));
    }

    @Test
    @DisplayName("Stats deve retornar distribuição por plano")
    void statsDeveRetornarDistribuicaoPorPlano() {
        // Arrange
        List<ChurnData> dados = Arrays.asList(clienteRiscoAlto, clienteRiscoBaixo);
        when(repository.findAll()).thenReturn(dados);

        // Act
        Map<String, Object> resultado = systemService.getStats();

        // Assert
        @SuppressWarnings("unchecked")
        Map<String, Long> distribuicao = (Map<String, Long>) resultado.get("distribuicaoPorPlano");
        assertNotNull(distribuicao);
        assertEquals(1L, distribuicao.get("basico"));
        assertEquals(1L, distribuicao.get("premium"));
    }

    @Test
    @DisplayName("Stats deve retornar top 5 maior risco")
    void statsDeveRetornarTop5MaiorRisco() {
        // Arrange
        List<ChurnData> dados = Arrays.asList(clienteRiscoAlto, clienteRiscoBaixo);
        when(repository.findAll()).thenReturn(dados);

        // Act
        Map<String, Object> resultado = systemService.getStats();

        // Assert
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> top5 = (List<Map<String, Object>>) resultado.get("top5MaiorRisco");
        assertNotNull(top5);
        assertFalse(top5.isEmpty());
        assertEquals("CLI-001", top5.get(0).get("clienteId")); // Maior probabilidade primeiro
    }

    @Test
    @DisplayName("Stats com lista vazia deve retornar zeros")
    void statsComListaVaziaDeveRetornarZeros() {
        // Arrange
        when(repository.findAll()).thenReturn(Collections.emptyList());

        // Act
        Map<String, Object> resultado = systemService.getStats();

        // Assert
        assertNotNull(resultado);
        assertEquals(0, resultado.get("totalAnalisados"));
        assertEquals(0L, resultado.get("totalRiscoAlto"));
        assertEquals(0L, resultado.get("totalRiscoBaixo"));
        assertEquals(0.0, resultado.get("taxaChurnPercentual"));
    }
}
