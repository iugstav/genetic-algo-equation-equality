import random


def rand(first):
    r = random.random()
    while r <= first:
        r = random.random()

    return r


def fitness(chromo):
    return abs((chromo[0] + 2 * chromo[1] + 3 * chromo[2] + 4 * chromo[3]) - 30)


def crossover(a, b, cut):
    child = []
    for i in range(0, cut):
        child.append(a[i])

    for j in range(cut, len(b)):
        child.append(b[j])

    return child

# cada gene corresponde a uma das 4 variáveis da equação
chromo = [
    [
        random.randrange(0, 30, 1),
        random.randrange(0, 30, 1),
        random.randrange(0, 30, 1),
        random.randrange(0, 30, 1),
    ]
    for _ in range(0, 10)
]

generations = 0
MUTATION_RATE = 0.08  # 8%
CROSSOVER_RATE = 0.7  # 70%

result = []
while len(result) == 0:
    # aplica a função objetivo para cada cromossomo
    objective = [fitness(c) for c in chromo]
    # calcula o fit de cada cromossomo
    selection = [1 / (f + 1) for f in objective]
    selection_total = sum(selection)
    # calcula a probabilidade de fitness para ser selecionado na próxima geração
    fitness_score = [sel / selection_total for sel in selection]

    # método da seleção roleta
    cumulative_prob = []
    cumu_sum = 0
    for i in range(1, len(fitness_score) + 1):
        for j in range(0, i):
            cumu_sum += fitness_score[j]

        cumulative_prob.append(cumu_sum)
        cumu_sum = 0

    random_nums = [rand(cumulative_prob[0]) for _ in range(0, len(chromo))]
    new_chromos = []
    for i in range(0, len(chromo)):
        for j in range(0, len(chromo) - 1):
            if (
                random_nums[i] > cumulative_prob[j]
                and random_nums[i] < cumulative_prob[j + 1]
            ):
                new_chromos.append(chromo[j + 1])
                break

    for i in range(0, len(chromo)):
        chromo[i] = new_chromos[i]

    parent = []
    # seleciona os pais para a nova geração
    for k in range(0, len(chromo)):
        random_nums[k] = random.random()
        if random_nums[k] < CROSSOVER_RATE:
            parent.append((k, chromo[k]))

    crossover_tuples = []
    # cria os pares de crossover com base nos pais para gerar novos cromossomos
    for i in range(0, len(parent)):
        if i == len(parent) - 1:
            crossover_tuples.append((parent[i], parent[0]))
            continue
        crossover_tuples.append((parent[i], parent[i + 1]))

    cut_points = []
    # seleciona os pontos de corte pro crossover de forma aleatória
    for i, c in enumerate(crossover_tuples):
        chromo_index = c[0][0]
        cut_points.append(random.randrange(1, len(chromo[0]), 1))
        chromo[chromo_index] = crossover(
            c[0][1], c[1][1], cut_points[len(cut_points) - 1]
        )

    # numero de cromossomos * numero de genes em um cromossomo
    total_genes = len(chromo) * len(chromo[0])
    # quantos cromossomos vão sofrer mutação
    mutation_num = round(MUTATION_RATE * total_genes)

    # o primeiro elemento é um chromossomo aleatório e o segundo, um gene desse cromossomo
    mutation_indexes = [
        (
            random.randrange(0, len(chromo), 1),
            random.randrange(0, len(chromo[0]), 1),
        )
        for _ in range(0, mutation_num)
    ]

    # aplica a mutação no gene selecionado de cada cromossomo
    for m in mutation_indexes:
        r = random.randrange(0, 30, 1)
        chromo[m[0]][m[1]] = r

    for c in chromo:
        if fitness(c) == 0:
            result = c
            break

    generations += 1

print("\nRESULTADO")
print(f"chromossomo {result}: fitness: {fitness(result)} em {generations} gerações")
