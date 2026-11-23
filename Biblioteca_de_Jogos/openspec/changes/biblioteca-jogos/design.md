# Design técnico

## Arquitetura
Aplicação Flask com rotas HTTP, templates Jinja2, CSS e persistência SQLite.

## Modelo de dados
- `genres(id PK, name UNIQUE)`
- `games(id PK, title, platform, release_year, status, genre_id FK)`
- `loans(id PK, game_id FK, borrower, loan_date, return_date, status)`

## Relacionamentos
- Um gênero possui vários jogos (1:N).
- Um jogo pode ter vários empréstimos históricos (1:N).

## Decisões
SQLite simplifica a execução local para a avaliação. As chaves estrangeiras são ativadas em cada conexão. As regras de disponibilidade são validadas no servidor.

## Limitações
Protótipo acadêmico sem autenticação, permissões, testes automatizados ou deploy de produção.
