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
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("ChurnService - Testes Unitários")
class ChurnServiceTest {

    @Mock
    private ChurnRepository repository;

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private ChurnService churnService;

    private ChurnData clienteExemplo;

    @BeforeEach
    void setUp() {
        clienteExemplo = new ChurnData();
        clienteExemplo.setId("123");
        clienteExemplo.setClienteId("CLI-001");
        clienteExemplo.setIdade(35);
        clienteExemplo.setGenero("Masculino");
        clienteExemplo.setRegiao("Sudeste");
        clienteExemplo.setValorMensal(49.90);
        clienteExemplo.setTempoAssinaturaMeses(12);
        clienteExemplo.setPlanoAssinatura("premium");
        clienteExemplo.setAtivo(true);
    }

    @Test
    @DisplayName("Deve listar apenas análises ativas")
    void deveListarApenasAnalisesAtivas() {
        // Arrange
        List<ChurnData> listaAtivos = Arrays.asList(clienteExemplo);
        when(repository.findByAtivoTrue()).thenReturn(listaAtivos);

        // Act
        List<ChurnData> resultado = churnService.listarAnalises();

        // Assert
        assertNotNull(resultado);
        assertEquals(1, resultado.size());
        assertTrue(resultado.get(0).getAtivo());
        verify(repository, times(1)).findByAtivoTrue();
    }

    @Test
    @DisplayName("Deve listar análises com risco alto")
    void deveListarAnalisesRiscoAlto() {
        // Arrange
        clienteExemplo.setRiscoAlto(true);
        List<ChurnData> listaRiscoAlto = Arrays.asList(clienteExemplo);
        when(repository.findByRiscoAltoTrue()).thenReturn(listaRiscoAlto);

        // Act
        List<ChurnData> resultado = churnService.listarRiscoAlto();

        // Assert
        assertNotNull(resultado);
        assertEquals(1, resultado.size());
        assertTrue(resultado.get(0).getRiscoAlto());
        verify(repository, times(1)).findByRiscoAltoTrue();
    }

    @Test
    @DisplayName("Deve buscar análise por ID existente")
    void deveBuscarAnalisePorIdExistente() {
        // Arrange
        when(repository.findById("123")).thenReturn(Optional.of(clienteExemplo));

        // Act
        Optional<ChurnData> resultado = churnService.buscarPorId("123");

        // Assert
        assertTrue(resultado.isPresent());
        assertEquals("CLI-001", resultado.get().getClienteId());
        verify(repository, times(1)).findById("123");
    }

    @Test
    @DisplayName("Deve retornar vazio para ID inexistente")
    void deveRetornarVazioParaIdInexistente() {
        // Arrange
        when(repository.findById("999")).thenReturn(Optional.empty());

        // Act
        Optional<ChurnData> resultado = churnService.buscarPorId("999");

        // Assert
        assertFalse(resultado.isPresent());
        verify(repository, times(1)).findById("999");
    }

    @Test
    @DisplayName("Deve registrar análise e salvar no banco")
    void deveRegistrarAnaliseESalvarNoBanco() {
        // Arrange
        when(repository.save(any(ChurnData.class))).thenReturn(clienteExemplo);

        // Act
        ChurnData resultado = churnService.registrarAnalise(clienteExemplo);

        // Assert
        assertNotNull(resultado);
        assertTrue(resultado.getAtivo());
        verify(repository, times(1)).save(any(ChurnData.class));
    }
}
