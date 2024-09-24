
# Relatório do Sistema de Gestão de Tarefas Domésticas com Regras e Multiagentes

## Introdução

Este relatório apresenta um sistema de gestão de tarefas domésticas que utiliza um modelo multiagente para realizar tarefas com base em regras predefinidas. Cada tarefa tem uma prioridade e só pode ser executada se certas condições forem atendidas. O sistema é implementado em Python e simula um ambiente onde os agentes trabalham em conjunto para concluir as tarefas domésticas.

## Código Fonte

### Definição da Classe `Tarefa`

A classe `Tarefa` representa uma tarefa que pode ser realizada por um agente.

```python
# Definição da classe Tarefa
class Tarefa:
    def __init__(self, nome, prioridade, condicao_execucao):
        self.nome = nome
        self.prioridade = prioridade
        self.condicao_execucao = condicao_execucao
        self.concluida = False

    def pode_executar(self, estado):
        return self.condicao_execucao(estado) and not self.concluida
```

### Definição da Classe `Agente`

A classe `Agente` representa um agente que pode executar uma tarefa.

```python
# Definição da classe Agente
class Agente:
    def __init__(self, nome, tarefa):
        self.nome = nome
        self.tarefa = tarefa

    def executar_tarefa(self, estado):
        if self.tarefa.pode_executar(estado):
            print(f"{self.nome} está executando a tarefa: {self.tarefa.nome}")
            self.tarefa.concluida = True
```

### Definição da Classe `SistemaGestao`

A classe `SistemaGestao` gerencia a execução das tarefas pelos agentes com base nas prioridades e condições de execução.

```python
# Definição da classe SistemaGestao
class SistemaGestao:
    def __init__(self, tarefas, agentes, estado_inicial):
        self.tarefas = sorted(tarefas, key=lambda t: t.prioridade, reverse=True)
        self.agentes = agentes
        self.estado = estado_inicial

    def executar(self):
        while not all(tarefa.concluida for tarefa in self.tarefas):
            for tarefa in self.tarefas:
                for agente in self.agentes:
                    if agente.tarefa == tarefa:
                        agente.executar_tarefa(self.estado)
                        self.atualizar_estado()

    def atualizar_estado(self):
        for tarefa in self.tarefas:
            if tarefa.nome == "Lavar Pratos" and tarefa.concluida:
                self.estado["pia_cheia"] = False
            elif tarefa.nome == "Varrer Chão" and tarefa.concluida:
                self.estado["chao_sujo"] = False
            elif tarefa.nome == "Regar Plantas" and tarefa.concluida:
                self.estado["plantas_secas"] = False
```

### Funções de Condição para Execução de Tarefas

```python
def condicao_lavar_pratos(estado):
    return estado["pia_cheia"]

def condicao_varrer_chao(estado):
    return estado["chao_sujo"]

def condicao_regar_plantas(estado):
    return estado["plantas_secas"]
```

### Função para Obter o Estado Inicial

```python
def obter_estado_inicial():
    print("Sistema de Gestão de Tarefas Domésticas com Regras e Multiagentes")
    print("Responda as perguntas com 's' ou 'n' :)")
    pia_cheia = input("A pia está cheia?").strip().lower() == 's'
    chao_sujo = input("O chão está sujo?").strip().lower() == 's'
    plantas_secas = input("As plantas estão secas?").strip().lower() == 's'
    return {"pia_cheia": pia_cheia, "chao_sujo": chao_sujo, "plantas_secas": plantas_secas}
```

### Função para Designar Agentes a Tarefas

```python
def designar_agentes(tarefas, nomes_agentes):
    agentes = []
    for tarefa in sorted(tarefas, key=lambda t: t.prioridade, reverse=True):
        print(f"
Designando agente para a tarefa de prioridade {tarefa.prioridade}: {tarefa.nome}")
        for idx, nome_agente in enumerate(nomes_agentes):
            print(f"{idx + 1}. {nome_agente}")
        escolha = int(input("Escolha o número do agente: ")) - 1
        agente = Agente(nomes_agentes[escolha], tarefa)
        agentes.append(agente)
    return agentes
```

### Definição e Execução do Sistema

```python
# Definição das tarefas
tarefa1 = Tarefa("Lavar Pratos", prioridade=3, condicao_execucao=condicao_lavar_pratos)
tarefa2 = Tarefa("Varrer Chão", prioridade=2, condicao_execucao=condicao_varrer_chao)
tarefa3 = Tarefa("Regar Plantas", prioridade=3, condicao_execucao=condicao_regar_plantas)

# Lista de nomes de agentes
nomes_agentes = ["Agente 1", "Agente 2", "Agente 3"]

# Obter o estado inicial do usuário
estado_inicial = obter_estado_inicial()

# Designar agentes às tarefas
agentes = designar_agentes([tarefa1, tarefa2, tarefa3], nomes_agentes)

# Criação do sistema de gestão e execução da simulação
sistema = SistemaGestao([tarefa1, tarefa2, tarefa3], agentes, estado_inicial)
sistema.executar()
```

## Documentação do Sistema

### Visão Geral

O sistema simula um ambiente doméstico onde múltiplos agentes executam tarefas com base em regras e condições específicas. Cada agente é responsável por uma tarefa e a executa apenas quando as condições necessárias são atendidas.

### Funcionamento

- **Tarefas:** Definidas com um nome, prioridade e condição de execução. Só são executadas se a condição for verdadeira.
- **Agentes:** São designados a tarefas e as executam quando as condições são atendidas.
- **Sistema de Gestão:** Gerencia a execução das tarefas pelos agentes de acordo com a prioridade.

### Regras de Execução

- Tarefas são executadas em ordem de prioridade.
- Uma tarefa só é concluída se a condição correspondente for atendida.

## Conclusão

O sistema apresentado é um executor de tarefas em um ambiente doméstico, utilizando agentes que trabalham de forma colaborativa.

