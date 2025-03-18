
#       integrantes do grupo - ECO CONNECT -
# ------------------------------------------------
#       -   MIGUEL BARROS       - RM556652       -
#       -   PEDRO VALENTIM      - RM556826       -
#       -   THOMAS RODRIGUES    - RM558042       -
# ------------------------------------------------

import time
from datetime import datetime
import oracledb  # Oracle database connection
import pandas as pd
import json
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Exibe uma saudação de acordo com a hora do dia.
def saudacao_dia() -> None:

    hora_atual = datetime.now().hour
    if hora_atual < 12:
        saudacao = "Bom dia"
    elif 12 <= hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    print("\n" + "=" * 40)
    print(f"{saudacao}, Seja bem-vindo à ECO CONNECT!".center(30))
    print("=" * 40 + "\n")

# Conecta ao banco de dados Oracle e retorna a conexão e o cursor.
def gerar_conexao() -> tuple:

    try:
        conn = oracledb.connect(user="rm556652", password="120206", dsn="oracle.fiap.com.br:1521/ORCL")
        cursor = conn.cursor()
        conexao = True
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        conexao = False
        conn, cursor = None, None
    return conn, cursor, conexao

# Verifica e cria a tabela PROJETO caso ela não exista.
def verificar_ou_criar_tabela_projeto(cursor, conn) -> None:

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM user_tables
            WHERE table_name = 'PROJETO'
        """)
        existe = cursor.fetchone()[0] > 0

        if not existe:
            cursor.execute("""
                CREATE TABLE PROJETO (
                    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    nome_projeto VARCHAR2(100),
                    tipo_fonte VARCHAR2(50),
                    regiao VARCHAR2(50),
                    custo NUMBER,
                    status VARCHAR2(50),
                )
            """)
            conn.commit()
    except oracledb.Error as error:
        print("Erro ao verificar ou criar a tabela:", error)


#Função auxiliar para exibir as opções e capturar a escolha do usuário.
#Retorna a opção escolhida ou 'Indefinido' se a escolha for inválida.
def escolher_opcao(nome_opcao: str, opcoes_map: dict) -> str:

    limpar_tela()
    while True:
        print(f"\n       Escolha {nome_opcao}:       ")
        print("-" * 60)
        for chave, valor in opcoes_map.items():
            print(f"{chave} - {valor}")
        print("0 - Voltar")

        escolha = input(f"Digite o número correspondente a {nome_opcao}: ").strip()

        if escolha == "0":
            return "Voltar"
        elif escolha in opcoes_map:
            return opcoes_map[escolha]
        else:
            print("Escolha inválida, tente novamente.")

        # Perguntar se deseja tentar novamente ou continuar
        confirmacao = input("Digite 1 para tentar novamente ou Enter para continuar: ").strip()
        if confirmacao == '1':
            continue  # Voltar ao início do loop para uma nova escolha
        elif confirmacao == '':
            break  # Continuar com a escolha atual
        else:
            print("Opção inválida. Continuando com a escolha atual.")
            break


# def para inserir um projeto
def inserir_projeto(conn, menu_principal) -> None:
    while True:
        limpar_tela()
        print("\n       Inserir Novo Projeto       ")
        print("-" * 50)

        # Solicita o nome do projeto
        while True:
            nome_projeto = input("Digite o nome do projeto: ").strip()
            if nome_projeto:
                break
            else:
                print("Erro: o nome do projeto não pode ser vazio.")

        # Solicita o ID do projeto, permitindo que inicie com 0
        while True:
            id_projeto = input("Digite o ID do projeto: ").strip()
            if id_projeto.isdigit() and int(id_projeto) >= 0:
                break
            else:
                print("Erro: o ID do projeto deve ser um número positivo ou zero e não pode estar vazio.")

        # Escolha do tipo de energia
        tipo_fonte = escolher_opcao("o tipo de fonte de energia", {
            "1": "Solar", "2": "Eólica", "3": "Biomassa", "4": "Hidrelétrica",
            "5": "Geotérmica", "6": "Ondas e Marés", "7": "Nuclear Limpa"
        })
        if tipo_fonte == "Voltar":
            continue

        # Escolha da região do projeto
        regiao = escolher_opcao("a região do projeto", {
            "1": "Norte", "2": "Nordeste", "3": "Centro-Oeste", "4": "Sudeste", "5": "Sul"
        })
        if regiao == "Voltar":
            continue

        # Custo estimado
        while True:
            try:
                custo_estimado = float(input("Digite o custo estimado do projeto (em reais): "))
                if custo_estimado < 0:
                    raise ValueError("O custo deve ser um número positivo.")
                break
            except ValueError:
                print("Erro: apenas números são permitidos para o custo estimado.")

        # Escolha do status do projeto
        status = escolher_opcao("o status do projeto", {
            "1": "Em Andamento", "2": "Concluído", "3": "Planejado"
        })
        if status == "Voltar":
            continue

        # Exibir os dados inseridos para confirmação
        while True:
            print("\n       Confira os dados do projeto:       ")
            print("-" * 50)
            print(f"\nNome do Projeto: {nome_projeto}")
            print(f"ID do Projeto: {id_projeto}")
            print(f"Tipo de Fonte: {tipo_fonte}")
            print(f"Região: {regiao}")
            print(f"Custo Estimado: {custo_estimado} reais")
            print(f"Status: {status}")
            print('\n1 - Confirmar\n2 - Corrigir')

            sn = input("Selecione a opção: ").strip()

            if sn == '1':
                # Confirmar e inserir os dados no banco de dados
                try:
                    cursor = conn.cursor()
                    query = """
                    INSERT INTO PROJETO (id_projeto, nome_projeto, tipo_fonte, regiao, custo_estimado, status)
                    VALUES (:id_projeto, :nome_projeto, :tipo_fonte, :regiao, :custo_estimado, :status)
                    """
                    cursor.execute(query, {
                        "id_projeto": id_projeto,
                        "nome_projeto": nome_projeto,
                        "tipo_fonte": tipo_fonte,
                        "regiao": regiao,
                        "custo_estimado": custo_estimado,
                        "status": status
                    })
                    conn.commit()
                    cursor.close()

                    print(f"Projeto {nome_projeto} inserido com sucesso!")
                    print(
                        f"ID: {id_projeto}, Tipo de Fonte: {tipo_fonte}, Região: {regiao}, Custo Estimado: {custo_estimado}, Status: {status}")
                    limpar_tela()
                    # Retornar ao menu principal após a inserção
                    menu_principal()
                    break

                except Exception as e:
                    print(f"Erro ao inserir o projeto: {e}")
                    break

            elif sn == '2':
                # Permite corrigir os dados e voltar ao início da coleta
                print("Por favor, digite as informações corretamente novamente!\n")
                break

            else:
                print("Escolha inválida, tente novamente.")


# Consulta os projetos no banco de dados com base no nome ou exibe todos.
def consultar_projetos(cursor) -> None:

    limpar_tela()
    print("\n        Consultar Projetos      ")
    print("-" * 30)

    # Solicita filtro de nome
    nome_filtro = input("Filtrar por nome (deixe vazio para todos): ")

    # Exibindo as opções digitadas
    if nome_filtro:
        print(f"Filtrando por nome: {nome_filtro}")
    else:
        print("Consultando todos os projetos.")

    try:
        if nome_filtro:
            # Caso o filtro de nome seja fornecido
            cursor.execute("SELECT * FROM PROJETO WHERE nome_projeto LIKE :1", ('%' + nome_filtro + '%',))
        else:
            # Caso contrário, consulta todos os projetos
            cursor.execute("SELECT * FROM PROJETO")

        projetos = cursor.fetchall()

        if projetos:
            for projeto in projetos:
                id_projeto = str(projeto[0]).zfill(3)
                print(
                    f"ID: {id_projeto}, Nome: {projeto[1]}, Tipo de Fonte: {projeto[2]}, Região: {projeto[3]}, Custo Estimado: {projeto[4]}, Status: {projeto[5]}")
        else:
            print("Nenhum projeto encontrado.")
    except Exception as e:
        print(f"Erro ao consultar projetos: {e}")


# Atualiza um projeto com base no ID fornecido.
def atualizar_projeto(conn, cursor, id: int) -> None:

    limpar_tela()
    print("\n        Atualizar Projeto      ")
    print("-" * 30)
    try:
        # Verifica se o projeto com o ID existe e obtém os dados atuais
        cursor.execute("SELECT * FROM PROJETO WHERE ID_PROJETO = :1", (id,))
        projeto = cursor.fetchone()

        if not projeto:
            print("ID não encontrado.")
            return

        # Coleta as novas informações, permitindo que o usuário pressione Enter para manter o valor atual
        print(f"\nNome atual do projeto: {projeto[1]}")
        novo_nome = input("Novo nome do projeto (pressione Enter para manter): ").strip() or projeto[1]

        print(f"\nTipo de Fonte atual: {projeto[2]}")
        tipo_fonte = escolher_opcao("o tipo de fonte de energia", {
            "1": "Solar", "2": "Eólica", "3": "Biomassa", "4": "Hidrelétrica",
            "5": "Geotérmica", "6": "Ondas e Marés", "7": "Nuclear Limpa"
        }) or projeto[2]

        print(f"\nRegião atual do projeto: {projeto[3]}")
        regiao = escolher_opcao("a região do projeto", {
            "1": "Norte", "2": "Nordeste", "3": "Centro-Oeste", "4": "Sudeste", "5": "Sul"
        }) or projeto[3]

        print(f"\nCusto estimado atual do projeto: {projeto[4]}")
        while True:
            custo_estimado_input = input("Novo custo estimado (pressione Enter para manter): ").strip()
            if custo_estimado_input:
                try:
                    custo_estimado = float(custo_estimado_input)
                    if custo_estimado < 0:
                        raise ValueError("O custo deve ser um número positivo.")
                    break
                except ValueError:
                    print("Erro: apenas números são permitidos para o custo estimado.")
            else:
                custo_estimado = projeto[4]
                break

        print(f"\nStatus atual do projeto: {projeto[5]}")
        status = escolher_opcao("o status do projeto", {
            "1": "Em Andamento", "2": "Concluído", "3": "Planejado"
        }) or projeto[5]

        # Atualiza o projeto no banco de dados com as novas informações
        cursor.execute("""
            UPDATE PROJETO
            SET nome_projeto = :1, tipo_fonte = :2, regiao = :3, custo_estimado = :4, status = :5
            WHERE ID_PROJETO = :6
        """, (novo_nome, tipo_fonte, regiao, custo_estimado, status, id))
        print(f"ID: {projeto[0]}, Nome: {projeto[1]}, Tipo de Fonte: {projeto[2]}, Região: {projeto[3]}, Custo Estimado: {projeto[4]}, Status: {projeto[5]}")
        conn.commit()
        print("Projeto atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar projeto: {e}")


 # Exclui um projeto com base no ID fornecido.
def excluir_projeto(conn, cursor, id: int) -> None:

    limpar_tela()
    try:
        # Verifica se o ID existe no banco de dados
        cursor.execute("SELECT * FROM PROJETO WHERE ID_PROJETO = :1", (id,))
        projeto = cursor.fetchone()

        if not projeto:
            print("ID não encontrado.")
            return

        # Exibe as informações do projeto e pede confirmação para excluir
        print(
            f"ID: {projeto[0]}, Nome: {projeto[1]}, Tipo de Fonte: {projeto[2]}, Região: {projeto[3]}, Custo Estimado: {projeto[4]}, Status: {projeto[5]}")

        confirmacao = input("Tem certeza que deseja excluir este projeto? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return

        # Exclui o projeto
        cursor.execute("DELETE FROM PROJETO WHERE ID_PROJETO = :1", (id,))
        conn.commit()
        print("Projeto excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir projeto: {e}")


# Menu para exportar dados para JSON ou Excel.
def exportar_dados_menu(conn, cursor) -> None:

    limpar_tela()
    print("        Exportar Dados       ")
    print("-" * 30)
    print("1. Exportar para JSON")
    print("2. Exportar para Excel")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        exportar_para_json(cursor)
    elif choice == '2':
        exportar_para_excel(cursor)
    else:
        print("Opção inválida.")


# Exporta os dados para um arquivo JSON.
def exportar_para_json(cursor) -> None:

    try:
        cursor.execute("SELECT * FROM PROJETO")
        rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        with open('projetos.json', 'w') as json_file:
            json.dump(rows, json_file, indent=4)
        print("Dados exportados para JSON com sucesso!")
    except Exception as e:
        print(f"Erro ao exportar para JSON: {e}")


# Exporta os dados para um arquivo Excel.
def exportar_para_excel(cursor) -> None:

    try:
        cursor.execute("SELECT * FROM PROJETO")
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        df.to_excel('projetos.xlsx', index=False)
        print("Dados exportados para Excel com sucesso!")
    except Exception as e:
        print(f"Erro ao exportar para Excel: {e}")


# Menu principal da aplicação.
def menu_principal() -> None:

    conn, cursor, conexao = gerar_conexao()
    if not conexao:
        return
    verificar_ou_criar_tabela_projeto(cursor, conn)

    while True:
        print("       MENU PRINCIPAL       ")
        print("-" * 30)
        print("1. Inserir Projeto")
        print("2. Consultar Projetos")
        print("3. Atualizar Projeto")
        print("4. Excluir Projeto")
        print("5. Exportar Dados")
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            # Passando o menu_principal como argumento
            inserir_projeto(conn, menu_principal)
        elif escolha == '2':
            consultar_projetos(cursor)
        elif escolha == '3':
            try:
                id = int(input("Digite o ID do projeto: "))
                atualizar_projeto(conn, cursor, id)
            except ValueError:
                print("Erro: O ID deve ser um número válido.")
        elif escolha == '4':
            try:
                print("\n        Excluir Projeto     ")
                print("-" * 30)
                id = int(input("Digite o ID do projeto: "))
                excluir_projeto(conn, cursor, id)
            except ValueError:
                print("Erro: O ID deve ser um número válido.")
        elif escolha == '5':
            exportar_dados_menu(conn, cursor)
        elif escolha == '6':
            print("Saindo...")
            exit()
        else:
            print("Opção inválida.")
        input("\nPressione a tecla enter para continuar...")
        limpar_tela()

    cursor.close()
    conn.close()


# Inicia o sistema solicitando o ID do projeto e direciona o fluxo.
def iniciar_sistema() -> None:

    conn, cursor, conexao = gerar_conexao()
    if not conexao:
        return

    limpar_tela()
    saudacao_dia()

    while True:
        try:
            id_projeto = input("Digite o ID do projeto: ").strip()
            if not id_projeto.isdigit():
                print("Erro: o ID deve ser um número válido. Tente novamente.")
                continue

            # Verifica se o projeto já existe
            query = "SELECT nome_projeto FROM PROJETO WHERE id_projeto = :id_projeto"
            cursor.execute(query, {"id_projeto": id_projeto})
            resultado = cursor.fetchone()

            if resultado:
                nome_projeto = resultado[0]
                print(f"Seja bem-vindo de volta!, {nome_projeto}!")
                menu_principal()
            else:
                print(f"ID {id_projeto} não encontrado. Vamos cadastrá-lo.")
                inserir_projeto(conn, menu_principal)

            break  # Sai do loop após o fluxo ser concluído

        except Exception as e:
            print(f"Erro ao verificar o ID: {e}")
            break

    cursor.close()
    conn.close()

# Executa o sistema
if __name__ == "__main__":
    iniciar_sistema()


