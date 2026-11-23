# Biblioteca de Jogos

Sistema web acadêmico para organizar um acervo de jogos e controlar empréstimos.

## Funcionalidades
- CRUD completo de jogos: cadastrar, listar, editar e excluir.
- Cadastro e listagem de gêneros.
- Registro de empréstimos para pessoas.
- Registro de devoluções e atualização automática da disponibilidade.
- Painel com total de jogos, jogos disponíveis e empréstimos ativos.

## Tecnologias
Python 3.10+, Flask, SQLite, HTML, CSS e Jinja2.

## Executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000. O banco `biblioteca.db` e dados demonstrativos são criados automaticamente.

## Banco de dados
- `genres`: gêneros dos jogos.
- `games`: título, plataforma, ano, status e gênero.
- `loans`: pessoa que pegou o jogo, data do empréstimo e devolução, status.

Relacionamentos: um gênero possui vários jogos (1:N); um jogo pode possuir vários registros de empréstimo ao longo do tempo (1:N).

## Regras de negócio
- Só jogos disponíveis podem ser emprestados.
- Ao registrar empréstimo, o jogo muda para "Emprestado".
- Ao registrar devolução, o jogo volta para "Disponível".
- Não é possível excluir jogos com histórico de empréstimos ou gêneros associados a jogos.
