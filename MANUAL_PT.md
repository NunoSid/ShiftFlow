# Manual ShiftFlow (PT)

## 1) Visao geral
ShiftFlow e uma plataforma web para planeamento, distribuicao e publicacao de horarios. Os perfis profissionais (grupos) sao configuraveis por cada hospital. Inclui gestao de profissionais, necessidades, disponibilidades, regras do mes, geracao automatica de horarios, trocas, chat e exportacoes.

## 2) Perfis e permissoes

### ADMIN
- Criar, editar e eliminar utilizadores.
- Definir nome da plataforma e da clinica/hospital.
- Carregar e ativar/desativar logos (ShiftFlow e unidade).
- Alterar cores da interface.
- Configurar texto do rodape do PDF.
- Criar/editar/remover categorias profissionais e os respetivos perfis (roles).
- Criar/editar/remover equipas, servicos, turnos e associacoes servico-turno.
- Criar/editar/remover profissionais.
- Gerar horarios, publicar, editar/lock, limpar horarios.
- Aprovar/rejeitar pedidos de disponibilidades.
- Aprovar/rejeitar trocas.
- Exportar horario, disponibilidades e trocas.

### COORDENADOR
- Criar/editar/remover equipas, servicos, turnos e associacoes.
- Criar/editar/remover profissionais.
- Gerar horarios, publicar, editar/lock, limpar horarios.
- Aprovar/rejeitar pedidos de disponibilidades.
- Aprovar/rejeitar trocas (com motivo).
- Exportar horario, disponibilidades e trocas.

### ENFERMEIRO
- Ver horario, necessidades e avisos.
- Submeter disponibilidades/indisponibilidades (para aprovacao).
- Pedir troca de turno.
- Chat com outros utilizadores.
- Exportar horario, disponibilidades e trocas.

### ASSISTENTE OPERACIONAL
- Ver horario, necessidades e avisos.
- Submeter disponibilidades/indisponibilidades (para aprovacao).
- Pedir troca de turno.
- Chat com outros utilizadores.
- Exportar horario, disponibilidades e trocas.

## 3) Login e idioma
- O idioma pode ser alterado no login e no topo da plataforma.
- A escolha fica guardada no browser.
- Todos os textos do UI mudam entre PT e EN.
- O seletor **Equipa** no topo mostra todos os perfis configurados.

## 4) Estrutura dos menus

### Dashboard
- **Gerar horario** (Admin/Coordenador).
- **Exportar horario** (todos os perfis).
- **Exportar disponibilidades** (todos os perfis).
- Indicadores: necessidades, turnos atribuidos, locks, alertas.

### Profissionais
- Lista de profissionais (nome, utilizador, servicos permitidos, horas semanais, saldo).
- Adicionar/editar/remover profissional.
- Associar utilizador a profissional.
- Definir categoria, servicos permitidos, horas semanais, permissao de noite, max noites/mes.

### Necessidades
- Grelha mensal por **Servico/Turno** e por dia.
- Preencher rapido (1 em todas as celulas) ou limpar.
- Guardar para persistir no mes atual.

### Disponibilidades / Pedidos
- Grelha mensal por profissional/dia (Admin/Coordenador).
- **As minhas disponibilidades**: cada utilizador preenche o seu mapa e envia para aprovacao.
- Aprovar/rejeitar pedidos pendentes.

### Regras do mes
- Definir limites de horas/semana e alvo medio.
- Definir descansos minimos.
- Penalizacoes do solver.
- Feriados do mes (auto) e feriados manuais.
- Ajustes manuais (feriados trabalhados, horas extra, reducoes).
- Tabela de horarios dos turnos (inicio/fim por codigo).

### Horario do mes
- Grelha mensal por profissional/dia.
- Editar celula com o editor flutuante.
- Lock/deslock rapido (tecla L).
- Limpar celula (Delete).
- Publicar horario por equipa.
- Estatisticas: horas por profissional e contagem de manhas/tardes/noites/folgas/descansos/ferias.
- Listas de faltas de cobertura e alertas.

### Equipas
- Criar equipas por perfil configurado (qualquer role definido nas categorias).
- Associar servico e membros da equipa.

### Servicos e turnos
- Criar/editar servicos (com cor) para qualquer perfil.
- Criar turnos (codigo, etiqueta, tipo, inicio/fim).
- Associar servicos a turnos.

### Trocas de turno
- Pedir troca (data, turno atual/pretendido, motivo e observacoes).
- Participantes aceitam/recusam.
- Coordenador aprova/recusa (com motivo opcional).
- Exportar lista de trocas.

### Chat
- Lista de utilizadores por perfil.
- Conversas organizadas.
- Arquivar/Eliminar apenas para quem clica.
- Alertas visuais de mensagens nao lidas.

### Admin
- Configurar nomes da plataforma/unidade.
- Logos (upload e visibilidade).
- Cores.
- Texto do rodape do PDF (editavel, vazio por defeito).
- Categorias profissionais.
- Utilizadores (criar, editar, eliminar).
- Criar/apagar demos.

## 5) Exportacoes
- **Horario**: Excel ou PDF.
- **Disponibilidades**: Excel ou PDF.
- **Trocas**: Excel.
- Em PDF: logos (se ativos), legenda de turnos, rodape configuravel.

## 6) Seed e dados demo
- `SHIFTFLOW_SEED_MODE=demo` cria:
  - Utilizadores demo
  - Profissionais associados
  - Servicos e turnos demo
  - Necessidades demo do mes atual
- Botao **Criar demos** e **Apagar demos** no Admin.

## 7) Instalar e iniciar
- `./start.sh` cria `.env` a partir de `.env.example`, prepara ambiente e inicia o servidor.
- Aceder a `http://localhost:8010/`.

## 8) Dicas
- Para acesso remoto: iniciar com `--host 0.0.0.0` e abrir a porta 8010.
- O texto do rodape do PDF fica vazio por defeito e pode ser editado no Admin.
