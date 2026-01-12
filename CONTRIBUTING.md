# Guia de Contribuição para o ConectaFAPES

Este documento descreve como você pode contribuir e quais são as expectativas que temos para garantir um processo de colaboração produtivo e transparente

## Como posso contribuir?
Existem várias maneiras de contribuir para o projeto, dependendo de suas habilidades e interesses:

- **Reportar bugs:** Se encontrar algum problema, abra uma issue descrevendo o bug.
- **Sugerir melhorias:** Sugestões de novas funcionalidades ou melhorias são sempre bem-vindas.
- **Escrever código:** Você pode resolver problemas abertos, desenvolver novos recursos ou melhorar o código existente.
- **Melhorar a documentação:** Documentação clara é fundamental. Ajude a melhorar tutoriais, manuais e outros materiais de suporte.
- **Discutir ideias:** Participe das discussões em issues e pull requests.

## Processo de Contribuição

### 1. Fork e Clone o Repositório

Faça o fork do repositório do **ConectaFAPES** para o seu próprio GitHub, e clone-o localmente.

### 2. Crie uma Branch

Para fazer suas alterações, crie uma nova branch a partir da `main`. Nomeie a branch de forma descritiva para a mudança que você está propondo.

```bash
git checkout -b seu-username-github/nome-da-feature-a-ser-trabalhada-nabranch
```

### 3. Faça suas alterações

Realize as mudanças desejadas no código. Certifique-se de seguir os padrões de codificação e de adicionar comentários ou documentação se necessário.

### 4. Teste suas alterações

Garanta que todas as funcionalidades estejam funcionando corretamente. Execute os testes automatizados (se aplicável) para verificar que suas mudanças não causaram regressões.

### 5. Commit e Push

Faça o commit (utilizando o padrão de commit semântico) das suas mudanças com uma mensagem clara e concisa:

```bash
git commit -m "Descrição clara da mudança"
```

Em seguida, faça o push da sua branch para o GitHub:

```bash
git push origin nome-da-sua-branch
```

### 6. Abra um Pull Request

Vá até o repositório original do **ConectaFAPES** no GitHub e crie um *pull request* (PR) a partir da sua branch. Na descrição do PR:

- Descreva o problema ou a funcionalidade abordada
- Explique a solução implementada
- Mencione se houve alterações que afetem outras áreas do projeto

Aguarde feedback dos mantenedores. Eles revisarão seu PR e poderão solicitar ajustes.

## Padrões de Código

Para garantir que o código seja legível e de alta qualidade, siga estes padrões:

- **Clareza**: Escreva código claro e fácil de entender. Nomeie variáveis e funções de maneira descritiva.
- **Documentação**: Sempre que possível, adicione comentários explicando trechos de código que possam ser complexos ou não óbvios.
- **Boas práticas**: Siga as melhores práticas de desenvolvimento e qualquer *style guide* que o projeto esteja utilizando.

## Feedback e Revisão

Todas as contribuições passarão por revisão. Durante o processo de revisão, você pode receber sugestões ou solicitações de mudanças. Esteja preparado para discutir as decisões de design e ajustar sua contribuição conforme o feedback da comunidade e dos mantenedores.

## Código de Conduta

Ao contribuir, você deve seguir nosso [Código de Conduta](./CODE_OF_CONDUCT.md). Respeite todos os membros da comunidade e garanta um ambiente colaborativo, seguro e acolhedor.

## Dúvidas?

Se tiver qualquer dúvida sobre o processo de contribuição, sinta-se à vontade para perguntar abrindo uma *issue* ou entrando em contato com a equipe do projeto.