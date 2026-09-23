## Purpose

Permite que os alunos se cadastrem, visualizem, atualizem e gerenciem disciplinas acadêmicas, acompanhando professores, semestres e o status ativo.

## ADDED Requirements

### Requirement: Criação de Disciplina
O sistema DEVE permitir que os usuários cadastrem uma nova disciplina acadêmica com nome, código da disciplina opcional, nome do professor, semestre e status.

#### Scenario: Criação de disciplina bem-sucedida
- **WHEN** o usuário enviar detalhes válidos da disciplina, incluindo um nome não vazio
- **THEN** o sistema cria o registro da disciplina e confirma o cadastro realizado com sucesso

#### Scenario: Criação rejeitada quando o nome está ausente
- **WHEN** o usuário tentar enviar uma disciplina sem nome
- **THEN** o sistema rejeita o envio e exibe um erro de validação exigindo o nome

### Requirement: Listagem e Recuperação de Disciplinas
O sistema DEVE recuperar e exibir todas as disciplinas cadastradas, mostrando seu nome, código, professor, semestre e status atual.

#### Scenario: Listar disciplinas existentes
- **WHEN** o usuário navegar até a seção de disciplinas
- **THEN** o sistema exibe todas as disciplinas cadastradas com seus respectivos metadados

#### Scenario: Exibição de estado vazio
- **WHEN** nenhuma disciplina tiver sido cadastrada no sistema
- **THEN** o sistema exibe uma mensagem clara de estado vazio orientando o usuário a adicionar uma disciplina

### Requirement: Modificação de Disciplina
O sistema DEVE permitir que os usuários atualizem os detalhes de disciplinas existentes, incluindo a modificação do professor, semestre e status (por exemplo, Ativa ou Concluída).

#### Scenario: Atualizar detalhes da disciplina com sucesso
- **WHEN** o usuário editar uma disciplina existente e enviar as informações atualizadas
- **THEN** o sistema salva as alterações e reflete os detalhes atualizados na lista de disciplinas

### Requirement: Exclusão de Disciplina
O sistema DEVE permitir que os usuários excluam uma disciplina acadêmica de seus registros.

#### Scenario: Excluir uma disciplina
- **WHEN** o usuário selecionar uma disciplina para exclusão e confirmar a ação
- **THEN** o sistema remove a disciplina e atualiza a lista de disciplinas

### Requirement: Contagem de Disciplinas Ativas no Painel
O sistema DEVE calcular e exibir o número de disciplinas ativas no painel principal (dashboard).

#### Scenario: A métrica do painel é atualizada com base nas disciplinas ativas
- **WHEN** o usuário visualizar o painel
- **THEN** o sistema exibe a contagem das disciplinas cujo status é ativo