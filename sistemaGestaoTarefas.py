# Definição da classe Tarefa
# A classe Tarefa representa uma tarefa que pode ser realizada por um agente.
class Tarefa:
    def __init__(self, nome, prioridade, condicao_execucao):
        # Inicializa os atributos da tarefa
        self.nome = nome  # Nome da tarefa
        self.prioridade = prioridade  # Prioridade da tarefa (quanto maior o valor, maior a prioridade)
        self.condicao_execucao = condicao_execucao  # Função que verifica se a tarefa pode ser executada
        self.concluida = False  # Indica se a tarefa foi concluída
 
    def pode_executar(self, estado):
        # Verifica se a tarefa pode ser executada com base no estado atual e se não está concluída
        return self.condicao_execucao(estado) and not self.concluida
 
# Definição da classe Agente
# A classe Agente representa um agente que pode executar uma tarefa.
class Agente:
    def __init__(self, nome, tarefa):
        # Inicializa os atributos do agente
        self.nome = nome  # Nome do agente
        self.tarefa = tarefa  # Atribui uma tarefa ao agente
 
    def executar_tarefa(self, estado):
        # Executa a tarefa se ela puder ser executada
        if self.tarefa.pode_executar(estado):
            print(f"{self.nome} está executando a tarefa: {self.tarefa.nome}")
            self.tarefa.concluida = True  # Marca a tarefa como concluída
 
# Definição da classe SistemaGestao
# A classe SistemaGestao gerencia a execução das tarefas pelos agentes com base nas prioridades e condições de execução.
class SistemaGestao:
    def __init__(self, tarefas, agentes, estado_inicial):
        # Inicializa os atributos do sistema de gestão
        self.tarefas = sorted(tarefas, key=lambda t: t.prioridade, reverse=True)  # Ordena as tarefas por prioridade
        self.agentes = agentes  # Lista de agentes atribuídos a tarefas
        self.estado = estado_inicial  # Estado inicial do sistema
 
    def executar(self):
        # Executa as tarefas em ordem de prioridade enquanto houver tarefas não concluídas
        while not all(tarefa.concluida for tarefa in self.tarefas):
            for tarefa in self.tarefas:
                for agente in self.agentes:
                    if agente.tarefa == tarefa:
                        agente.executar_tarefa(self.estado)  # O agente executa a tarefa se possível
                        self.atualizar_estado()  # Atualiza o estado do sistema após a execução de uma tarefa
 
    def atualizar_estado(self):
        # Atualiza o estado do sistema com base nas tarefas concluídas
        for tarefa in self.tarefas:
            if tarefa.nome == "Lavar Pratos" and tarefa.concluida:
                self.estado["pia_cheia"] = False  # Marca a pia como vazia após lavar os pratos
            elif tarefa.nome == "Varrer Chão" and tarefa.concluida:
                self.estado["chao_sujo"] = False  # Marca o chão como limpo após varrê-lo
            elif tarefa.nome == "Regar Plantas" and tarefa.concluida:
                self.estado["plantas_secas"] = False  # Marca as plantas como regadas
 
# Funções de condição para execução de tarefas
# Estas funções verificam se as condições necessárias para executar as tarefas são atendidas
def condicao_lavar_pratos(estado):
    return estado["pia_cheia"]  # A tarefa "Lavar Pratos" só pode ser executada se a pia estiver cheia
 
def condicao_varrer_chao(estado):
    return estado["chao_sujo"]  # A tarefa "Varrer Chão" só pode ser executada se o chão estiver sujo
 
def condicao_regar_plantas(estado):
    return estado["plantas_secas"]  # A tarefa "Regar Plantas" só pode ser executada se as plantas estiverem secas
 
# Função para obter o estado inicial a partir da entrada do usuário
def obter_estado_inicial():
    print("Sistema de Gestão de Tarefas Domésticas com Regras e Multiagentes")
    print("Responda as perguntas com 's' ou 'n' :)")
    print("-------------------------------------------------------------------------")
    # Coleta o estado inicial do ambiente a partir das respostas do usuário
    pia_cheia = input("A pia está cheia?").strip().lower() == 's'
    chao_sujo = input("O chão está sujo?").strip().lower() == 's'
    plantas_secas = input("As plantas estão secas?").strip().lower() == 's'
    return {"pia_cheia": pia_cheia, "chao_sujo": chao_sujo, "plantas_secas": plantas_secas}
 
# Função para designar agentes a tarefas em ordem de prioridade
def designar_agentes(tarefas, nomes_agentes):
    agentes = []
    for tarefa in sorted(tarefas, key=lambda t: t.prioridade, reverse=True):
        print(f"\nDesignando agente para a tarefa de prioridade {tarefa.prioridade}: {tarefa.nome}")
        # Exibe a lista de agentes disponíveis para o usuário escolher
        for idx, nome_agente in enumerate(nomes_agentes):
            print(f"{idx + 1}. {nome_agente}")
        escolha = int(input("Escolha o número do agente: ")) - 1  # Solicita ao usuário que escolha um agente
        agente = Agente(nomes_agentes[escolha], tarefa)  # Atribui o agente à tarefa
        agentes.append(agente)
    return agentes
 
# Definição das tarefas com suas respectivas prioridades e condições de execução
tarefa1 = Tarefa("Lavar Pratos", prioridade=3, condicao_execucao=condicao_lavar_pratos)
tarefa2 = Tarefa("Varrer Chão", prioridade=2, condicao_execucao=condicao_varrer_chao)
tarefa3 = Tarefa("Regar Plantas", prioridade=3, condicao_execucao=condicao_regar_plantas)
 
# Lista de nomes de agentes disponíveis
nomes_agentes = ["Agente 1", "Agente 2", "Agente 3"]
 
# Obter o estado inicial do sistema com base na entrada do usuário
estado_inicial = obter_estado_inicial()
 
# Designar agentes às tarefas com base na escolha do usuário, em ordem de prioridade
agentes = designar_agentes([tarefa1, tarefa2, tarefa3], nomes_agentes)
 
# Criação do sistema de gestão e execução da simulação
sistema = SistemaGestao([tarefa1, tarefa2, tarefa3], agentes, estado_inicial)
sistema.executar()
