import PyDest
import pprint

TOKEN = 'd5edb10339334ef6bed1889657d8465a'

destiny = PyDest.PyDest(TOKEN)

# memId = destiny.api.GetMembershipIdFromBungieId("Kutto#9246")

player = destiny.api.search_destiny_player(1, "Kutto#9246")
memId = player['Response'][0]['membershipId']

print(memId)

# pprint.pprint(memId)

# ['Response']['profile']['data']['characterIds'][0]

# e = destiny.api.get_profile(1, memId, [100])

# pprint.pprint(e)

# c = destiny.api.get_character(1, memId, '2305843009265615844', [204])

# pprint.pprint(destiny.decode_hash(2148295091, 'DestinyInventoryItemDefinition'))

# pprint.pprint(c)

# Print Current Nightfall
# for activity in c['Response']['activities']['data']['availableActivities']:
#     x = destiny.decode_hash(
#         activity['activityHash'], 'DestinyActivityDefinition')
#     pprint.pprint(x)

#     if 'Nightfall: Master' in x['displayProperties']['name']:
#         name = x['displayProperties']['description']
#         # print(name)
#         # pprint(x)

#         # for rewards in x['rewards'][0]['rewardItems']:
#         #     # p.pprint(rewards)
#         #     pprint(destiny.decode_hash(
#         #         rewards['itemHash'], 'DestinyInventoryItemDefinition'))

#         for modifiers in x['modifiers']:
#             modifierHash = modifiers['activityModifierHash']
#             y = destiny.decode_hash(
#                 modifierHash, 'DestinyActivityModifierDefinition')
#             # p.pprint(y)
#             print(y['displayProperties']['name'])
#             print(y['displayProperties']['description'])

#         # Print seasons of profile
#         for seasonHash in e['Response']['profile']['data']['seasonHashes']:
#             print(seasonHash)
#             x = destiny.decode_hash(seasonHash, "DestinySeasonDefinition")
#             # p.pprint(x)
#             print(x['displayProperties']['name'])
