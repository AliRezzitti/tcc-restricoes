# Restricoes organizacionais da Empresa Alfa

Restricoes obrigatorias que toda nova solucao deve seguir desde a especificacao.

- **ARQ-01 (Arquitetura):** Novas aplicacoes devem ser hospedadas na nuvem corporativa, usando servicos gerenciados homologados. E vedado instalar servidores proprios, inclusive servidores de arquivos locais, sem aprovacao do comite de arquitetura.
- **ARQ-02 (Arquitetura):** A autenticacao de usuarios internos deve ocorrer exclusivamente pelo login unico corporativo (SSO). Nenhuma aplicacao pode manter cadastro proprio de usuarios e senhas para usuarios internos.
- **ARQ-03 (Arquitetura):** A integracao entre sistemas deve ocorrer por APIs ou eventos publicados pelo sistema dono do dado. E vedado acessar diretamente o banco de dados de outro sistema.
- **CUS-01 (Custos):** Logs de aplicacao devem ser mantidos em armazenamento padrao por no maximo 90 dias. Depois disso, so podem ser arquivados em camada de armazenamento de baixo custo, e apenas quando houver exigencia legal ou de auditoria, pelo prazo que ela determinar.
- **CUS-02 (Custos):** Ambientes nao produtivos (desenvolvimento, teste e homologacao) devem ser desligados fora do horario comercial.
- **CUS-03 (Custos):** Disponibilidade acima de 99,5% exige justificativa de negocio e aprovacao previa da area de custos, por causa do custo da alta disponibilidade.
- **SEG-01 (Seguranca):** Dados pessoais e bancarios (como CPF e conta bancaria) devem ser armazenados criptografados e exibidos mascarados. O acesso aos dados completos e restrito aos perfis que precisam deles para executar sua funcao.
- **DAD-01 (Dados):** Comprovantes e documentos fiscais devem ser mantidos por 5 anos, por exigencia fiscal, e excluidos apos esse prazo.
