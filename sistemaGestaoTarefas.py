# Definição da classe Tarefa
class Tarefa:
    def __init__(self, nome, prioridade, condicao_execucao, tempo_execucao):
        self.nome = nome  # Nome da tarefa
        self.prioridade = prioridade  # Prioridade da tarefa
        self.condicao_execucao = condicao_execucao  # Função que verifica se a tarefa pode ser executada
        self.concluida = False  # Indica se a tarefa foi concluída
        self.tempo_execucao = tempo_execucao  # Tempo necessário para executar a tarefa

    def pode_executar(self, estado):
        return self.condicao_execucao(estado) and not self.concluida

# Definição da classe Agente
class Agente:
    def __init__(self, nome, tarefa):
        self.nome = nome  # Nome do agente
        self.tarefa = tarefa  # Atribui uma tarefa ao agente

    def executar_tarefa(self, estado):
        if self.tarefa.pode_executar(estado):
            print(f"{self.nome} está executando a tarefa: {self.tarefa.nome}")
            self.tarefa.concluida = True  # Marca a tarefa como concluída
            return self.tarefa.tempo_execucao  # Retorna o tempo gasto na execução
        return 0

# Definição da classe SistemaGestao
class SistemaGestao:
    def __init__(self, tarefas, agentes, estado_inicial, tempo_total):
        self.tarefas = sorted(tarefas, key=lambda t: t.prioridade, reverse=True)
        self.agentes = agentes
        self.estado = estado_inicial
        self.tempo_total = tempo_total  # Tempo total disponível para a execução das tarefas

    def tempo_estimado(self):
        return sum(tarefa.tempo_execucao for tarefa in self.tarefas if not tarefa.concluida)

    def verificar_tempo(self):
        tempo_estimado = self.tempo_estimado()
        if self.tempo_total < tempo_estimado:
            print(f"Alerta: O tempo total disponível ({self.tempo_total} minutos) é menor que o tempo estimado para as tarefas ({tempo_estimado} minutos).")
        else:
            print("O tempo total disponível é suficiente para executar todas as tarefas.")

    def executar(self):
        self.verificar_tempo()  # Verifica o tempo antes de executar
        while not all(tarefa.concluida for tarefa in self.tarefas) and self.tempo_total > 0:
            for tarefa in self.tarefas:
                for agente in self.agentes:
                    if agente.tarefa == tarefa:
                        tempo_gasto = agente.executar_tarefa(self.estado)
                        self.tempo_total -= tempo_gasto  # Desconta o tempo gasto
                        self.atualizar_estado()  # Atualiza o estado do sistema após a execução de uma tarefa
                        if tempo_gasto > 0:  # Se tempo foi gasto, saímos do loop para reavaliar o estado
                            break

    def atualizar_estado(self):
        for tarefa in self.tarefas:
            if tarefa.nome == "Lavar Pratos" and tarefa.concluida:
                self.estado["pia_cheia"] = False
            elif tarefa.nome == "Varrer Chão" and tarefa.concluida:
                self.estado["chao_sujo"] = False
            elif tarefa.nome == "Regar Plantas" and tarefa.concluida:
                self.estado["plantas_secas"] = False

# Funções de condição para execução de tarefas
def condicao_lavar_pratos(estado):
    return estado["pia_cheia"]

def condicao_varrer_chao(estado):
    return estado["chao_sujo"]

def condicao_regar_plantas(estado):
    return estado["plantas_secas"]

# Função para obter o estado inicial e o tempo total a partir da entrada do usuário
def obter_estado_inicial():
    print("Sistema de Gestão de Tarefas Domésticas com Regras e Multiagentes")
    print("Responda as perguntas com 's' ou 'n' :)")
    print("-------------------------------------------------------------------------")
    pia_cheia = input("A pia está cheia? ").strip().lower() == 's'
    chao_sujo = input("O chão está sujo? ").strip().lower() == 's'
    plantas_secas = input("As plantas estão secas? ").strip().lower() == 's'
    return {"pia_cheia": pia_cheia, "chao_sujo": chao_sujo, "plantas_secas": plantas_secas}

def obter_tempo_total():
    return int(input("Qual é o tempo total disponível para a execução das tarefas? (em minutos) "))

# Função para designar agentes a tarefas em ordem de prioridade
def designar_agentes(tarefas, nomes_agentes):
    agentes = []
    for tarefa in sorted(tarefas, key=lambda t: t.prioridade, reverse=True):
        print(f"\nDesignando agente para a tarefa de prioridade {tarefa.prioridade}: {tarefa.nome}")
        for idx, nome_agente in enumerate(nomes_agentes):
            print(f"{idx + 1}. {nome_agente}")
        escolha = int(input("Escolha o número do agente: ")) - 1
        agente = Agente(nomes_agentes[escolha], tarefa)
        agentes.append(agente)
    return agentes

# Definição das tarefas com suas respectivas prioridades, condições de execução e tempo de execução
tarefa1 = Tarefa("Lavar Pratos", prioridade=3, condicao_execucao=condicao_lavar_pratos, tempo_execucao=10)
tarefa2 = Tarefa("Varrer Chão", prioridade=2, condicao_execucao=condicao_varrer_chao, tempo_execucao=15)
tarefa3 = Tarefa("Regar Plantas", prioridade=1, condicao_execucao=condicao_regar_plantas, tempo_execucao=5)

# Lista de nomes de agentes disponíveis
nomes_agentes = ["Agente 1", "Agente 2", "Agente 3"]

# Obter o estado inicial do sistema e o tempo total disponível
estado_inicial = obter_estado_inicial()
tempo_total = obter_tempo_total()

# Designar agentes às tarefas com base na escolha do usuário, em ordem de prioridade
agentes = designar_agentes([tarefa1, tarefa2, tarefa3], nomes_agentes)

# Criação do sistema de gestão e execução da simulação
sistema = SistemaGestao([tarefa1, tarefa2, tarefa3], agentes, estado_inicial, tempo_total)
sistema.executar()
