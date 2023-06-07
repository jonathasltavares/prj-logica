from pysat.solvers import Glucose3

def criar_formula(minicursos, m, pares):
    num_minicursos = len(minicursos)
    num_slots = m

    variaveis = [[c * num_slots + s + 1 for s in range(num_slots)] for c in range(num_minicursos)]

    clausulas = []

    # Restrição: Cada minicurso deve ser ofertado em pelo menos um slot
    for c in range(num_minicursos):
        clausula = [variaveis[c][s] for s in range(num_slots)]
        clausulas.append(clausula)

    # Restrição: Cada minicurso deve ser ofertado em no máximo um slot
    for c in range(num_minicursos):
        for s1 in range(num_slots):
            for s2 in range(s1 + 1, num_slots):
                clausulas.append([-variaveis[c][s1], -variaveis[c][s2]])

    # Restrição: Minicursos com inscrições em comum não podem ser ofertados no mesmo slot
    for p in pares:
        i, j = p
        for s in range(num_slots):
            clausulas.append([-variaveis[i - 1][s], -variaveis[j - 1][s]])

    return variaveis, clausulas

def resolver_formula(variaveis, clausulas):
    solver = Glucose3()

    # Adicionar cláusulas ao solver
    for clausula in clausulas:
        solver.add_clause(clausula)

    # Verificar se a fórmula é satisfatível
    if solver.solve():
        # Obter valoração que satisfaz a fórmula
        val = solver.get_model()

        # Verificar quais variáveis estão verdadeiras na valoração
        horarios = []
        for c in range(len(variaveis)):
            for s in range(len(variaveis[c])):
                if variaveis[c][s] in val and val[variaveis[c][s]]:
                    horarios.append(f"{c + 1} s{s + 1}")

        return horarios

    return None

def main():
    print("Informe os dados do evento:")
    print("# Minicursos:")
    minicursos = []
    while True:
        minicurso = input()
        if minicurso == "":
            break
        minicursos.append(minicurso)

    print("# Slots:")
    m = int(input())

    print("# Pares de minicursos com inscrições em comum:")
    pares = []
    while True:
        linha = input()
        if linha == "":
            break
        par = tuple(map(int, linha.split()))
        pares.append(par)

    variaveis, clausulas = criar_formula(minicursos, m, pares)
    horarios = resolver_formula(variaveis, clausulas)

    if horarios:
        print("Saída:")
        for horario in horarios:
            print(horario)
    else:
        print("Não é possível agendar os minicursos com as restrições fornecidas.")

if __name__ == "__main__":
    main()
