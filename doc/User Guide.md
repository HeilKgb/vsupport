## Como utilizar o vsupport para dar suporte aos aplicativos via trello ##

#### 1) Configuração com as chaves e tokens de acesso
   Criar, seguindo o Trello Delevoper Guides, o `Developer API Keys`e o `Application Token`.
   copiar o `config_demo.json` para `config.json` e preencher o `token` e a `key`.
   Carregar e utilizar o seguinte comando:
   ```pyhon
   with open('vsupport/config.json') as json_file:
      CONFIG = load(json_file)
   ```

#### 2) Instancias o VTrello
   ```python
   VTRELLO = VTrello(api_key=CONFIG['Makoto']['key'], api_token=CONFIG['Makoto']['token'])
   ```

#### 3) Definir a Organização/Projeto à qual o aplicativo pertence.
   ```python
   OrganizationId = '52e95acf41bc365d3806cab3' (Venidera)
   ```
   A Organização/Projeto também pode ser encontrada, utilizando /SEARCH, e buscando "Suporte" e a chave "modelTypes" "boards".
   ```python
   output = VTRELLO.search(query='Suporte', params={'modelTypes': 'boards'})
   ```
   resposta:
   ```json
   output['boards']: [
      {
         "id": "5fb579ae05c74459d063ada8",
         "idOrganization": "52e95acf41bc365d3806cab3",
         "name": "Suporte"
      },
   ]
   ```
   ```python
   for board in output['boards']:
      org_name = VTRELLO.get_organization(orgId=board['idOrganization'])
      board['organization'] = organization
   print(dumps(output['boards'], indent=4, sort_keys=True))
   ```
   A partir dos resultados, selecionar o 'idOrganization'

#### 4) Buscar o usuário (membro) que será adicionado ao cartão inicialmente:

   - Uma maneira seria utilizar o *'get_member'*

   ```python
   manager_member = 'marcosleonefilho'
   manager = VTRELLO.get_member(memberName=manager_member, params={'fields': 'fullName'})
   if not manager:
      raise Exception('Board não encontrado.')
   print(dumps(manager, indent=4, sort_keys=True))
   ```

   - Outra, utilizar o *get_organization* com *nested='memberships'*

      ```python
      member_names = list()

      members = VTRELLO.get_organization(orgId=OrganizationId, nested='memberships')

      for mb in members:
         member = VTRELLO.get_member(memberId=mb['idMember'], params={'fields': 'fullName'})
         member_names.append(member)

      manager = [member for member in member_names if member['fullName'] == manager_member]
      if not manager:
         raise Exception('Board não encontrado.')
      else:
         manager = manager[0]
      print(dumps(manager, indent=4, sort_keys=True))
      ```

#### 5) Buscar o Board Support, utilizando o id da Organização/Projeto

   ```python
   boards = VTRELLO.get_organization(
      orgId=OrganizationId, nested='boards', params={'fields': 'name'})

   boards = [b for b in boards if b['name'] == 'Suporte']
   if not boards:
      raise Exception('Board não encontrado.')
   else:
      board = boards[0]
   print(dumps(board, indent=4, sort_keys=True))
   ```

#### 6) Buscar a lista 'Novos Recursos' OU 'Correções'

   ```python
   # tipo_lista = 'Correções'
   tipo_lista = 'Novos Recursos'
   lists = VTRELLO.get_board(boardId=board['id'], nested='lists', params={'fields': 'name'})
   lists = [li for li in lists if li['name'] == tipo_lista]
   if not lists:
      raise Exception('Board não possui lista %s', tipo_lista)
   else:
      lista_cartoes = lists[0]
   print(dumps(lista_cartoes, indent=4, sort_keys=True))
   ```

#### 7) Criar o novo Cartão com os parâmetros desejados
   ```json
   card_name = 'Nome do Novo Cartão que vai ser criado'
   card_desc = 'Descrição para o Cartão que está sendo criado'
   idList = lista_cartoes['id']
   params = {
      'idList': idList,
      'name': card_name,
      'desc': card_desc,
      'pos': 'bottom', # posição do cartão na lista
      'due': "2020-11-25T18:00:00.000Z", # Prazo estimado para este cartão
      'idMembers': [manager['id']],
      'idLabels': []
      'urlSource':
      'fileSource':
      'idCardSource':  # The ID of a Card to Copy into the new card
   }
   ```
   ```python
      card = VTRELLO.create_card(params=params)
      print(dumps(card, indent=4, sort_keys=True))
   ```
   ```json
   Response - Important datas
   card: {
      "id": "5fbc1d7cae458b4eac54bbcc",
      "idAttachmentCover": null,
      "idBoard": "5fb579ae05c74459d063ada8",
      "idChecklists": [],
      "idLabels": [],
      "idList": "5fb579ae05c74459d063adaa",
      "idMembers": ["509aa706c3f9df790a008465"],
      "name": "Nome do Novo Cart\u00e3o que vai ser criado",
      "desc": "Descri\u00e7\u00e3o para o Cart\u00e3o que est\u00e1 sendo criado"
   }
   ```

#### 8) Buscar atividades no cartão

   A) Buscar as atividades de todos os cartões de uma lista

   - Dados fornecidos:
      ```python
         actions = VTRELLO.get_list(listId=lista_cartoes['id'],  nested='actions')
         print(dumps(actions, indent=4, sort_keys=True))
      ```

   B) Buscar as atividades por cartão, para todos os cartões de uma lista

   ```python
      cards = VTRELLO.get_list(listId=lista_cartoes['id'], nested='cards')
      card_actions = dict()
      for card in cards:
         actions = VTRELLO.get_card(cardId=card['id'], nested='actions')
         card_actions[card['id']] = {
            'card_name': card['name'],
            'actions': actions
         }
      print(dumps(card_actions, indent=4, sort_keys=True))
   ```

   C) Buscar atividade de um cartão específico (cardId fornecido)

   ```python
      actions = VTRELLO.get_card(cardId='5fbc1d7cae458b4eac54bbcc',  nested='actions')
      print(dumps(actions, indent=4, sort_keys=True))
   ```

#### 9) Atualizar dados no cartão

   Para o cartão, com cardId="5fbc1d7cae458b4eac54bbcc" e os dados do cartão abaixo:
   ```json
     params = {
        'name': 'Novo Nome 1 2 3.',
        'desc': 'Mudando a cor.',
        'cover': {
           'idAttachment': None,
           'color': 'green',
           'idUploadedBackground': None,
           'size': 'full',
           'brightness': 'light'
        } # Updates the card's cover
        # 'closed': true, # Whether the card should be archived (closed: true)
        # 'due': "2020-11-21T13:00:00.000Z", # When the card is due, or null, Nullable: true, Format: date
        # 'dueComplete': # Whether the due date should be marked complete
        # 'idMembers': ["509aa706c3f9df790a008465"],
        # 'idAttachmentCover': # The ID of the image attachment the card should use as its cover, or null for none
        # 'idList': # The ID of the list the card should be in
        # 'idLabels': [] # Comma-separated list of label IDs
        # 'idBoard': # The ID of the board the card should be on
        # 'pos': 'bottom', # top, bottom
        # 'dueComplete': # Whether the due date should be marked complete
        # 'subscribed': # Whether the member is should be subscribed to the card
     }
   ```
   Atualizar o cartão, como segue:
   ```python
      card = VTRELLO.update_card(cardId=cardId, params=params)
      print(dumps(card, indent=4, sort_keys=True))
   ```

## Alguns exemplos de comandos:

1) *SEARCH - Fazer busca no trello. Existem várias chaves que vc pode fornecer, como idBoards, idOrganizations, idCards, modelTypes (actions/boards/cards/members/organizations), etc.*

    a) Buscar Organizations/Projects usando o SEARCH
    ```python
        organizations = VTRELLO.search(query='Suporte')
        print(dumps(organizations, indent=4, sort_keys=True))
    ```
    b) Buscar um Membros do Trello usando o SEARCH
    ```python
        members = VTRELLO.search(query='Joao', nested='members')
        print(dumps(members, indent=4, sort_keys=True))
    ```

2) *GET Organization's Info (Project's Info)*
    ```python
        organizations = VTRELLO.get_organization(orgId=OrganizationId)
        print(dumps(organizations, indent=4, sort_keys=True))
    ```
    *GET Organization's Memberships (Project's Memberships)*
    ```python
        members = VTRELLO.get_organization(orgId=OrganizationId, nested='memberships')
        print(dumps(members, indent=4, sort_keys=True))
    ```
    *GET actions of organization*
    ```python
        actions = VTRELLO.get_organization(orgId=OrganizationId, nested='actions')
        print(dumps(actions, indent=4, sort_keys=True))
    ```

3) *GET Boards' Info*
    ```python
        board = VTRELLO.get_board(boardId=boardId)
        print(dumps(board, indent=4, sort_keys=True))
    ```
    *GET actions from the Board*
    ```python
        actions = VTRELLO.get_board(boardId=boardId, nested='actions')
        print(dumps(actions, indent=4, sort_keys=True))
    ```
    *GET members from the Board*
    ```python
        members = VTRELLO.get_board(boardId=boardId, nested='members')
        print(dumps(members, indent=4, sort_keys=True))
    ```
    *GET lists from the Board*
    ```python
        lists = VTRELLO.get_board(boardId=boardId, nested='lists')
        print(dumps(lists, indent=4, sort_keys=True))
    ```
    *GET cards from the Board*
    ```python
        cards = VTRELLO.get_board(boardId=boardId, nested='cards')
        print(dumps(cards, indent=4, sort_keys=True))
    ```
    *GET lists from the Board*
    ```python
        lists = VTRELLO.get_board(boardId=boardId, nested='lists')
        print(dumps(lists, indent=4, sort_keys=True))
    ```
*obs: o 'nested' pode ser utilizado para várias outras combinações, como 'cards/{filter}', 'customfields', 'lists/{filter}', entre outros.

4) *GET Card's Info*
    ```python
        card = VTRELLO.get_card(cardId='5fbc1d7cae458b4eac54bbcc')
        print(dumps(card, indent=4, sort_keys=True))
    ```
    *GET actions from a card*
    ```python
        actions = VTRELLO.get_card(cardId=cardId,  nested='actions')
        print(dumps(actions, indent=4, sort_keys=True))
    ```
    *obs:

5) *GET Member's Info*
    ```python
        member = VTRELLO.get_member(memberId=memberId, params={'fields': 'fullName'})
        member = VTRELLO.get_member(memberName=memberName, params={'fields': 'fullName'})
        print(dumps(member, indent=4, sort_keys=True))
    ```
    *obs:

