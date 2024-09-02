import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# aqui eu criei os cursos validos pra quando for adicionar novas informações, o usuario tem que adicionar cursos já existentes no sistema, no caso
# esses cursos abaixo e o mesmo em generos validos lá em baixo.
cursos_validos = [
    "Engenharia",
    "Direito",
    "Psicologia",
    "Adm",
    "CC",
    "Medicina",
    "Historia",
    "Biologia",
    "Matematica",
    "Letras",
    "Filosofia",
    "EdFisica",
    "ArtesVisuais",
    "Musica",
    "Geografia",
    "Sociologia",
    "Economia",
    "EngCivil",
    "Quimica",
    "Fisica",
]

generos_validos = [
    "M",
    "F",
    "NB",
]

# df = DataFrame, uma variavel criada para ler o arquivo csv.
df = pd.read_csv("tabela.csv")

# Identifica e remove valores ausentes
df = df.dropna()

# Remove IDs duplicados
df = df.drop_duplicates(subset=["id_estudante"])

# Aqui definimos que a idade não pode ser menor que 0
# em baixo que a media_geral tem que ser entre 0 e 10
# o id_estudante tem que ser diferente de 0
df = df[df["idade"] >= 0]
df = df[(df["media_geral"] >= 0) & (df["media_geral"] <= 10)]
df = df[df["id_estudante"] != 0]

# Depois de todo o processo de verificação de valores ausentes, remoção de valores que não existem ou exclusão de dado duplicado, ele salva e corrige a tabela.
df.to_csv("dados_corrigidos.csv", index=False)

# Aqui eu pego a variavel df (DataFrame), menciono a coluna idade e digo que ela recebe a "idade" como int, faço a mesma coisa pra horas estudo
# mas mudo na media geral pra float devido as notas nem sempre serem arredondadas.
# Eu coloquei o genero como category ao inves de object por que pelo que foi pesquisado, colunas que tem um valor fixo mais limitado, no caso como genero
# só tem apenas 3 valores, e participa_atividades_extra tem apenas 2, é mais eficiente o uso do category pela eficiencia da memoria, desempenho e
# a integridade de dados.
df["idade"] = df["idade"].astype(int)
df["horas_estudo_semana"] = df["horas_estudo_semana"].astype(int)
df["media_geral"] = df["media_geral"].astype(float)
df["genero"] = df["genero"].astype("category")
df["participa_atividades_extra"] = df["participa_atividades_extra"].astype("category")


def adicionar_informacoes():
    # aqui gera automaticamente o ID, impossibilitando o usuario de colocar o ID por conta própria pra evitar conflitos e erros.
    novo_id = df["id_estudante"].max() + 1 if not df.empty else 1

    # aqui é um loop pra fazer a validação.
    while True:
        curso = input("Informe o curso: ")
        if curso in cursos_validos:
            break
        else:
            print("Curso inválido. Por favor, escolha um curso da lista válida.")

    while True:
        genero = input("Informe o gênero: ")
        if genero in generos_validos:
            break
        else:
            print("Genero não reconhecido, Por favor, escolha um genero válido.")

    horas_estudo = int(input("Informe as horas de estudo por semana: "))
    idade = int(input("Informe a idade: "))
    media_geral = float(input("Informe a média geral: "))

    # Adiciona as novas informações ao DataFrame
    novo_registro = {
        "id_estudante": novo_id,
        "curso": curso,
        "genero": genero,
        "horas_estudo_semana": horas_estudo,
        "idade": idade,
        "media_geral": media_geral,
    }
    df.loc[len(df)] = novo_registro

    # Salva as mudanças no CSV
    df.to_csv("dados_corrigidos.csv", index=False)
    print("Informações adicionadas com sucesso!")


def exibir_tabelas_por_genero():
    # Estatísticas descritivas por gênero
    estatisticas_por_genero = df.groupby("genero").agg(
        {
            "media_geral": ["mean", "median", lambda x: x.mode()[0], "std"],
            "horas_estudo_semana": ["mean", "median", lambda x: x.mode()[0], "std"],
        }
    )

    # Renomeando as colunas para facilitar a leitura
    estatisticas_por_genero.columns = [
        "Média Média Geral",
        "Mediana Média Geral",
        "Moda Média Geral",
        "Desvio Padrão Média Geral",
        "Média Horas Estudo",
        "Mediana Horas Estudo",
        "Moda Horas Estudo",
        "Desvio Padrão Horas Estudo",
    ]

    # Distribuição percentual por gênero
    distribuicao_genero = df["genero"].value_counts(normalize=True) * 100

    # Plotando gráficos
    fig, axs = plt.subplots(2, 1, figsize=(16, 10), tight_layout=True)

    # Gráfico de Estatísticas Descritivas por Gênero
    sns.barplot(
        data=estatisticas_por_genero.reset_index(),
        x="genero",
        y="Média Média Geral",
        ax=axs[0],
        palette="viridis",
    )
    axs[0].set_title("Média da Média Geral por Gênero")
    axs[0].set_ylabel("Média Média Geral")
    axs[0].set_xlabel("Gênero")

    # Gráfico de Distribuição Percentual por Gênero
    sns.barplot(
        x=distribuicao_genero.index,
        y=distribuicao_genero.values,
        ax=axs[1],
        palette="coolwarm",
    )
    axs[1].set_title("Distribuição Percentual por Gênero")
    axs[1].set_ylabel("Percentual (%)")
    axs[1].set_xlabel("Gênero")

    # Adicionando valores aos gráficos
    for ax in axs.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 9),
                textcoords="offset points",
            )

    plt.show()


def exibir_tabelas_por_curso():
    # Estatísticas descritivas por curso
    estatisticas_por_curso = df.groupby("curso").agg(
        {
            "media_geral": ["mean", "median", lambda x: x.mode()[0], "std"],
            "horas_estudo_semana": ["mean", "median", lambda x: x.mode()[0], "std"],
        }
    )

    estatisticas_por_curso.columns = [
        "Média Média Geral",
        "Mediana Média Geral",
        "Moda Média Geral",
        "Desvio Padrão Média Geral",
        "Média Horas Estudo",
        "Mediana Horas Estudo",
        "Moda Horas Estudo",
        "Desvio Padrão Horas Estudo",
    ]

    # Distribuição percentual por curso
    distribuicao_curso = df["curso"].value_counts(normalize=True) * 100

    # Plotando gráficos
    fig, axs = plt.subplots(2, 1, figsize=(16, 10), tight_layout=True)

    # Gráfico de Estatísticas Descritivas por Curso
    sns.barplot(
        data=estatisticas_por_curso.reset_index(),
        x="curso",
        y="Média Média Geral",
        ax=axs[0],
        palette="viridis",
    )
    axs[0].set_title("Média da Média Geral por Curso")
    axs[0].set_ylabel("Média Média Geral")
    axs[0].set_xlabel("Curso")

    # Gráfico de Distribuição Percentual por Curso
    sns.barplot(
        x=distribuicao_curso.index,
        y=distribuicao_curso.values,
        ax=axs[1],
        palette="coolwarm",
    )
    axs[1].set_title("Distribuição Percentual por Curso")
    axs[1].set_ylabel("Percentual (%)")
    axs[1].set_xlabel("Curso")

    # Adicionando valores aos gráficos
    for ax in axs.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 9),
                textcoords="offset points",
            )

    plt.show()


def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar informações")
        print("2. Exibir tabelas por gênero")
        print("3. Exibir tabelas por curso")
        print("4. Sair")
        escolha = input("Opção: ")

        if escolha == "1":
            adicionar_informacoes()
        elif escolha == "2":
            exibir_tabelas_por_genero()
        elif escolha == "3":
            exibir_tabelas_por_curso()
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()
