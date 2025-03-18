
ECO CONNECT
Descrição do Projeto
Este projeto foi desenvolvido como parte de um trabalho acadêmico para a faculdade, focado em soluções de energia limpa. O objetivo do projeto é gerenciar informações sobre diferentes projetos de energia sustentável, incluindo detalhes como tipo de fonte de energia, região, custo estimado e status do projeto.

Funcionalidades
Saudação Personalizada: Exibe uma saudação de acordo com a hora do dia.
Conexão com Banco de Dados: Conecta-se ao banco de dados Oracle para armazenar e gerenciar informações dos projetos.
Gerenciamento de Projetos: Permite inserir, consultar, atualizar e excluir projetos de energia limpa.
Exportação de Dados: Exporta os dados dos projetos para arquivos JSON ou Excel.
Menu Interativo: Interface de menu para facilitar a navegação e execução das funcionalidades.
Tecnologias Utilizadas
Python: Linguagem de programação principal.
Oracle Database: Banco de dados utilizado para armazenar as informações dos projetos.
Pandas: Biblioteca utilizada para manipulação e exportação de dados.
JSON: Formato de exportação de dados.
Excel: Formato de exportação de dados.
Como Executar
Instale as dependências:

pip install oracledb pandas
Configure a conexão com o banco de dados:

Atualize as credenciais de conexão no método gerar_conexao.
Execute o script:

python eco_connect.py
