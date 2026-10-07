# Especificacao de Requisitos: Portal de Cadastro de Fornecedores

O portal permite que empresas interessadas em fornecer para a Empresa Alfa solicitem o seu cadastro, que os compradores da Empresa Alfa analisem as solicitacoes e que os fornecedores aprovados sejam enviados ao ERP.

- **REQ-01:** O fornecedor deve enviar a solicitacao de cadastro com CNPJ, razao social, endereco e contato comercial.
- **REQ-02:** Os fornecedores devem criar uma conta no portal, com e-mail e senha, para acompanhar a sua solicitacao.
- **REQ-03:** O portal deve ficar disponivel 99,9% do tempo.
- **REQ-04:** Para evitar cadastros duplicados, o portal deve consultar diretamente a tabela de fornecedores no banco de dados do ERP.
- **REQ-05:** O comprador deve aprovar ou reprovar cada solicitacao em ate 3 dias uteis, registrando a justificativa em caso de reprovacao.
- **REQ-06:** Os documentos enviados pelos fornecedores (contrato social, certidoes e notas fiscais) devem ser armazenados no servico gerenciado de armazenamento de arquivos da nuvem corporativa.
- **REQ-07:** A tela de consulta de fornecedores deve exibir a todos os compradores a conta bancaria completa do fornecedor e o CPF do seu representante legal.
- **REQ-08:** As notas fiscais dos fornecedores devem ser excluidas 2 anos apos o pagamento, para reduzir o custo de armazenamento.
- **REQ-09:** Os logs do portal devem ser mantidos por 90 dias no armazenamento padrao e, depois, arquivados em camada de armazenamento de baixo custo por 5 anos, prazo exigido pela auditoria interna.
- **REQ-10:** Os compradores da Empresa Alfa devem acessar o portal com usuario e senha proprios do portal, criados pelo administrador.
- **REQ-11:** Quando o cadastro for aprovado, o portal deve enviar os dados do fornecedor ao ERP pela API de fornecedores publicada pelo ERP.
- **REQ-12:** O ambiente de homologacao deve permanecer ligado 24 horas por dia, 7 dias por semana, para executar os testes automatizados noturnos.
- **REQ-13:** O fornecedor deve ser notificado por e-mail sempre que o status da sua solicitacao mudar.
