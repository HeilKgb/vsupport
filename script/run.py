"""
Code source: Venidera Research & Development
Modified by Makoto Kadowaki
License: GNU GPL version 3
"""

import logging
from logging import info
import locale
import random
from json import load, dump, loads, dumps

from vsupport.vtrello import VTrello

# General procedures to show the log
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: ' +
           '(%(filename)s:%(funcName)s at %(lineno)d): %(message)s',
    datefmt='%b %d %H:%M:%S',
    level=logging.INFO)
locale.setlocale(locale.LC_ALL, ('pt_BR.UTF-8'))

# Configuração com as chaves e tokens de acesso
with open('config.json') as json_file:
    CONFIG = load(json_file)

# Trello WebHock Callback URL
callbackURL = 'https://suporte.risk3.xyz/trello/webhooks'
# callbackURL = 'https://miran-lt.venidera.net/trello/webhooks'

# Instancias o VTrello
VTRELLO = VTrello(
    api_key=CONFIG['Makoto']['key'],
    api_token=CONFIG['Makoto']['token'],
    callbackURL=callbackURL
)

# Id da Organização ou Projeto à qual o aplicativo pertence
# OrganizationId = '52e95acf41bc365d3806cab3'
manager_member = 'marcosleonefilho'

manager = VTRELLO.get(
    resource='members',
    member_id=manager_member,
    params={'fields': 'fullName'}
)

if not manager:
    raise Exception('Board não encontrado.')

print(dumps(manager, indent=4, sort_keys=True))

# Organizations - return name
org_list = VTRELLO.get(
    resource='members',
    member_id=manager_member,
    nested="organizations",
    params={"fields": ["name" , "displayName"]}
)

# Get All members of organization
members = []
for org in org_list:
    member = VTRELLO.get(
        resource='_organizations',
        org_id=org["id"],
        nested="members",
        params={}
    )
    members.append({'org': org, 'members': member})

# Filter [
#   {"displayName": "Risk3 - Curadorias", "name": "projetoavaliacaodecredito", "id": "5eff78fda1c12141253f1f8c"},
#   {"displayName": "Risk3 - Desenvolvimento", "name": "risk3desenvolvimento", "id": "6052a9c0cd408d379571f9f7"}
# ]
# [x for x in org_list if 'risk3'in x['displayName'].lower()] or
# next((x for x in org_list if 'risk3'in x['displayName'].lower()), None)

OrganizationId = next((x['id'] for x in org_list if 'risk3desenvolvimento'in x['name']), None)

# A) Processo para criar um cartão:

# 1. Buscar o Board Support, utilizando o id do Projeto
boards = VTRELLO.get(
    resource='organizations',
    org_id=OrganizationId,
    nested='boards',
    params={'fields': ['name', 'url', 'shortUrl', 'labelNames'] }
)

boards = [b for b in boards if b['name'] == 'Suporte']

if not boards:
    raise Exception('Board não encontrado.')
else:
    board = boards[0]

# Buscar membros do board
board_members = VTRELLO.get(
    resource='boards',
    board_id=board["id"],
    nested="members"
)

# ** Carregar lista de LABELS
# Labels Valid colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime
org = 'Apolo'

labels = VTRELLO.get(
    resource='boards',
    board_id=board['id'],
    nested='labels',
    params={'fields': ['name', 'color']}
)

label = next((item for item in labels if item['name'] == org),None)

if not label:
    colors = list(set(map(lambda d: d['color'], labels)))
    color = random.choice(colors)
    label = VTRELLO.post(
        resource='labels',
        params={'name': org, 'color': color, 'idBoard': board['id']}
    )

# 2. Buscar a lista 'Novos Recursos' OU 'Correções''
    # tipo_lista = 'Novos Recursos'
tipo_lista = 'Correções'

lists = VTRELLO.get(
    resource='boards',
    board_id=board['id'],
    nested='lists',
    params={'fields': 'name'}
)

lista_cartoes = [li for li in lists if li['name'] == tipo_lista]

if not lista_cartoes:
    raise Exception('Board possui lista %s', tipo_lista)
else:
    lista_cartoes = lista_cartoes[0]

print(dumps(lista_cartoes, indent=4, sort_keys=True))

webhooks = VTRELLO.get(
    resource='tokens',
    nested='webhooks'
)
print(dumps(webhooks, indent=4, sort_keys=True))

# webhook = webhooks[0]
# resp = VTRELLO.delete(
#     resource='webhooks',
#     webhook_id=webhook['id']
# )

# # Caso 2) Buscar as atividades por cartão, para todos os cartões de uma lista
cards = VTRELLO.get(
    resource='lists',
    list_id=lista_cartoes['id'],
    nested='cards'
)

print(dumps(cards, indent=4, sort_keys=True))

for card in cards:
    if 'idChecklists' in card:
        idChecklists = card['idChecklists']
        for idCheck in idChecklists:
            checklist = VTRELLO.get(
                resource='checklists',
                checklist_id=idCheck,
            )
            print(dumps(checklist, indent=4, sort_keys=True))

            # if
            #     checkitem = VTRELLO.post(
            # resource='checklists',
            # checklist_id=idChecklists[0],
            # params={'name': 'item 1', 'checked': True, 'pos': 'bottom'},
            # nested='checkItems')
            # print(dumps(checkitem, indent=4, sort_keys=True))

# webhook = VTRELLO.post(
#     resource='webhooks',
#     params={'idModel': cards[0]['id']}
# )

# card_actions = dict()

# for card in cards:
#     actions = VTRELLO.get(
#         resource='cards',
#         card_id=card['id'],
#         nested='actions'
#     )
#     card_actions[card['id']] = {
#         'card_name': card['name'],
#         'actions': actions
#     }

# print(dumps(card_actions, indent=4, sort_keys=True))

# webhook = VTRELLO.post(
#     resource='webhooks',
#     params={'idModel': lista_cartoes['id']}
# )

# if webhook:
#     print('webhook exist')
# resp = VTRELLO.get(
#     resource='webhooks',
#     webhook_id=webhook['id']
# )
#     print(dumps(resp, indent=4, sort_keys=True))
#     print('deleting webhook')
#     resp = VTRELLO.delete(
#         resource='webhooks',
#         webhook_id=webhook['id']
#     )
#     print(dumps(resp, indent=4, sort_keys=True))
#     print('getting webhook')
#     webhooks = VTRELLO.get(
#         resource='tokens',
#         nested='webhooks'
#     )
#     print(dumps(webhooks, indent=4, sort_keys=True))
# else:
#     print('check existency of webhooks')
#     webhooks = VTRELLO.get(
#         resource='tokens',
#         nested='webhooks'
#     )
#     print(dumps(resp, indent=4, sort_keys=True))
#     print('deleting webhook')
#     resp = VTRELLO.delete(
#         resource='webhooks',
#         webhook_id=webhooks[0]['id']
#     )
#     print(dumps(resp, indent=4, sort_keys=True))
#     print('getting webhook')
#     resp = VTRELLO.get(
#         resource='tokens',
#         nested='webhooks'
#     )
#     print(dumps(resp, indent=4, sort_keys=True))

# print(dumps(resp, indent=4, sort_keys=True))

# resp = VTRELLO.delete_webhook(webhookId=webhook['id'])
# print(dumps(resp, indent=4, sort_keys=True))

card_name = 'Criar um módulo para integrar os aplicativos e o Trello'
card_desc = 'Este módulo, utilizando a linguagem python, será o responsável pela\n'\
            ' criação de novos cartões, sem que o usuário precise entrar no trello.'\
            ' Será criada uma interface nos aplicativos, onde o usuário poderá solicitar'\
            ' as demandas de suporte.'
idList = lista_cartoes['id']
params = {
    'idList': idList,
    'name': card_name,
    'desc': card_desc,
    'pos': 'bottom', # posição do cartão na lista
    'due': "2020-11-30T18:00:00.000Z", # Prazo estimado para este cartão
    'idMembers': [manager['id']],
    'idLabels': []
    # 'urlSource':
    # 'fileSource':
    # 'idCardSource':  # The ID of a Card to Copy into the new card
}

newcard = VTRELLO.post(
    resource='cards',
    params=params
)

print(dumps(newcard, indent=4, sort_keys=True))

# # B) Processo para buscar atividades no cartão

# # Caso 1) Buscar as atividades de todos os cartões de uma lista
# actions = VTRELLO.get_list(listId=lista_cartoes['id'],  nested='actions')
# print(dumps(actions, indent=4, sort_keys=True))

# # Caso 2) Buscar as atividades por cartão, para todos os cartões de uma lista
# cards = VTRELLO.get_list(listId=lista_cartoes['id'], nested='cards')
# card_actions = dict()
# for card in cards:
#     actions = VTRELLO.get(resource='cards', card_id=card['id'], nested='actions')
#     card_actions[card['id']] = {
#         'card_name': card['name'],
#         'actions': actions
#     }

# print(dumps(card_actions, indent=4, sort_keys=True))

# # C) Atualizar um cartão
# cardId = newcard['id']
# params = {
#     'name': 'Novo Nome 1 2 3.',
#     'desc': 'Mudando a cor.',
#     'cover': {
#         'idAttachment': None,
#         'color': 'green',
#         'idUploadedBackground': None,
#         'size': 'full',
#         'brightness': 'light'
#     } # Updates the card's cover
#     # 'closed': true, # Whether the card should be archived (closed: true)
#     # 'due': "2020-11-21T13:00:00.000Z", # When the card is due, or null, Nullable: true, Format: date
#     # 'dueComplete': # Whether the due date should be marked complete
#     # 'idMembers': ["509aa706c3f9df790a008465"],
#     # 'idAttachmentCover': # The ID of the image attachment the card should use as its cover, or null for none
#     # 'idList': # The ID of the list the card should be in
#     # 'idLabels': [] # Comma-separated list of label IDs
#     # 'idBoard': # The ID of the board the card should be on
#     # 'pos': 'bottom', # top, bottom
#     # 'dueComplete': # Whether the due date should be marked complete
#     # 'subscribed': # Whether the member is should be subscribed to the card
# }
# card = VTRELLO.update_card(cardId=cardId, params=params)
# print(dumps(card, indent=4, sort_keys=True))

# B) Processo para buscar atividades no cartão

# # Caso 1) Buscar as atividades de todos os cartões de uma lista
# actions = VTRELLO.get_list(listId=lista_cartoes['id'],  nested='actions')
# print(dumps(actions, indent=4, sort_keys=True))

# # Caso 2) Buscar as atividades por cartão, para todos os cartões de uma lista
# cards = VTRELLO.get_list(listId=lista_cartoes['id'], nested='cards')
# card_actions = dict()
# for card in cards:
#     actions = VTRELLO.get_card(cardId=card['id'], nested='actions')
#     card_actions[card['id']] = {
#         'card_name': card['name'],
#         'actions': actions
#     }
# print(dumps(card_actions, indent=4, sort_keys=True))

# all_members = VTRELLO.get(resource='organizations', org_id=OrganizationId, nested='memberships')

# full_members = []
# params={'fields': ['fullName', 'username']}
# for member in all_members:
#     print(member)
#     memb = VTRELLO.get(resource='members', member_id=member['idMember'], params=params)
#     full_members.append(memb)

# print(dumps(full_members, indent=4, sort_keys=True))