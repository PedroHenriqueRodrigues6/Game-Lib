# Especificação: Biblioteca de Jogos

## REQ-01 — Gerenciar jogos
O sistema deve permitir cadastrar, consultar, editar e excluir jogos.
Cada jogo deve conter título, plataforma, ano de lançamento, gênero e status.

## REQ-02 — Gerenciar gêneros
O sistema deve permitir cadastrar e listar gêneros. O nome deve ser único. Gêneros associados a jogos não podem ser excluídos.

## REQ-03 — Empréstimos
O sistema deve permitir registrar empréstimo de jogo disponível, identificando a pessoa e a data.
Ao emprestar, o status do jogo deve mudar para "Emprestado".

## REQ-04 — Devoluções
O sistema deve permitir registrar a devolução de empréstimo ativo.
Ao devolver, deve preencher a data de devolução e liberar o jogo.

## REQ-05 — Painel
A página inicial deve exibir total de jogos, jogos disponíveis e empréstimos ativos.

## Critérios de aceite
1. Jogo cadastrado aparece na listagem.
2. Jogo editado exibe os novos dados.
3. Jogo sem empréstimos pode ser excluído.
4. Não é permitido emprestar jogo já emprestado.
5. Devolução altera o empréstimo para "Devolvido" e o jogo para "Disponível".
