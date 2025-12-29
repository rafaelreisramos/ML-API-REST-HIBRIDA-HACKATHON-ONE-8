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
import org.springframework.data.mongodb.core.MongoTemplate;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("ChurnBatchService - Testes Unitários")
class ChurnBatchServiceTest {

    @Mock
    private ChurnRepository repository;

    @Mock
    private ChurnService churnService;

    @Mock
    private MongoTemplate mongoTemplate;

    @InjectMocks
    private ChurnBatchService churnBatchService;

    private String csvValido;
    private ChurnData clienteExemplo;

    @BeforeEach
    void setUp() {
        csvValido = "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso\n"
                +
                "CLI-001,35,Masculino,Sudeste,49.90,12,premium,credito,mobile,25,1,4.5,4.0,3.5,45,2";

        clienteExemplo = new ChurnData();
        clienteExemplo.setClienteId("CLI-001");
        clienteExemplo.setIdade(35);
        clienteExemplo.setPrevisao("Churn");
        clienteExemplo.setProbabilidade(0.75);
        clienteExemplo.setRiscoAlto(true);
        clienteExemplo.setModeloUsado("RandomForest");
    }

    @Test
    @DisplayName("Deve ler CSV corretamente")
    void deveLerCSVCorretamente() throws IOException {
        // Arrange
        InputStream inputStream = new ByteArrayInputStream(csvValido.getBytes(StandardCharsets.UTF_8));

        // Act
        List<Map<String, String>> resultado = churnBatchService.lerCSV(inputStream);

        // Assert
        assertNotNull(resultado);
        assertEquals(1, resultado.size());
        assertEquals("CLI-001", resultado.get(0).get("clienteId"));
        assertEquals("35", resultado.get(0).get("idade"));
        assertEquals("Sudeste", resultado.get(0).get("regiao"));
    }

    @Test
    @DisplayName("Deve retornar lista vazia para CSV sem dados")
    void deveRetornarListaVaziaParaCSVSemDados() throws IOException {
        // Arrange
        String csvVazio = "clienteId,idade,genero\n";
        InputStream inputStream = new ByteArrayInputStream(csvVazio.getBytes(StandardCharsets.UTF_8));

        // Act
        List<Map<String, String>> resultado = churnBatchService.lerCSV(inputStream);

        // Assert
        assertNotNull(resultado);
        assertTrue(resultado.isEmpty());
    }

    @Test
    @DisplayName("Deve mapear Map para ChurnData corretamente")
    void deveMapearParaChurnDataCorretamente() {
        // Arrange
        Map<String, String> dados = Map.of(
                "clienteId", "CLI-002",
                "idade", "28",
                "genero", "Feminino",
                "regiao", "Sul",
                "valorMensal", "39.90",
                "tempoAssinaturaMeses", "6",
                "planoAssinatura", "basico");

        // Act
        ChurnData resultado = churnBatchService.mapearParaChurnData(dados);

        // Assert
        assertNotNull(resultado);
        assertEquals("CLI-002", resultado.getClienteId());
        assertEquals(28, resultado.getIdade());
        assertEquals("Feminino", resultado.getGenero());
        assertEquals("Sul", resultado.getRegiao());
        assertEquals(39.90, resultado.getValorMensal());
        assertTrue(resultado.getAtivo());
    }

    @Test
    @DisplayName("Deve gerar CSV com header e dados")
    void deveGerarCSVComHeaderEDados() {
        // Arrange
        clienteExemplo.setIdade(35);
        clienteExemplo.setGenero("Masculino");
        clienteExemplo.setRegiao("Sudeste");
        clienteExemplo.setValorMensal(49.90);
        clienteExemplo.setTempoAssinaturaMeses(12);
        clienteExemplo.setPlanoAssinatura("premium");
        clienteExemplo.setMetodoPagamento("credito");
        clienteExemplo.setDispositivoPrincipal("mobile");
        clienteExemplo.setVisualizacoesMes(25);
        clienteExemplo.setContatosSuporte(1);
        clienteExemplo.setAvaliacaoPlataforma(4.5);
        clienteExemplo.setAvaliacaoConteudoMedia(4.0);
        clienteExemplo.setAvaliacaoConteudoUltimoMes(3.5);
        clienteExemplo.setTempoMedioSessaoMin(45);
        clienteExemplo.setDiasUltimoAcesso(2);

        List<ChurnData> lista = List.of(clienteExemplo);

        // Act
        String csv = churnBatchService.gerarCSV(lista);

        // Assert
        assertNotNull(csv);
        assertTrue(csv.startsWith("clienteId,"));
        assertTrue(csv.contains("CLI-001"));
        assertTrue(csv.contains("Churn"));
        assertTrue(csv.contains("RandomForest"));
    }

    @Test
    @DisplayName("Deve processar lote e salvar no banco")
    void deveProcessarLoteESalvarNoBanco() throws IOException {
        // Arrange
        InputStream inputStream = new ByteArrayInputStream(csvValido.getBytes(StandardCharsets.UTF_8));
        when(churnService.chamarServicoIA(any(ChurnData.class))).thenReturn(clienteExemplo);
        when(repository.save(any(ChurnData.class))).thenReturn(clienteExemplo);

        // Act
        List<ChurnData> resultado = churnBatchService.processarLote(inputStream);

        // Assert
        assertNotNull(resultado);
        assertEquals(1, resultado.size());
        verify(churnService, times(1)).chamarServicoIA(any(ChurnData.class));
        verify(repository, times(1)).save(any(ChurnData.class));
    }
}
