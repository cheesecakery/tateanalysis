# TO DO:
    # get dates (dateRange, startDate, endDate)

import json
import os

root = "./collection-master/artworks"

# Get to each file
json_data = []
for outer in os.listdir(root):
    for folder in os.listdir(f"{root}/{outer}"):
        for file in os.listdir(f"{root}/{outer}/{folder}"):
            with open(f"{root}/{outer}/{folder}/{file}") as artwork_data:
                json_data.append(json.load(artwork_data))

stats = {}
categories = {
    'photography': {'polaroid', 'photographic', 'photograph'},
    'printing': {'engraving', 'silkscreen', 'lithograph', 'etching', 'blueprint', 'aquatint', 'intaglio', 'chromogenic', 'linocut', 'wood', 'drypoint'},
    'painting': {'acrylic', 'watercolour', 'gouache', 'oil', 'tempera', 'spray'},
    'drawing': {'graphite', 'pencil', 'pastel', 'chalk', 'pen', 'crayon', 'ink', 'charcoal'},
    'performance / film / sound': {'film', 'video', 'performance', 'sound', 'voice', 'stereo', 'light', 'lights', 'lighting'},
    'sculpture': {'copper', 'enamel', 'steel', 'brass', 'aluminium', 'aluminuim', 'sand', 'fibreglass', 'nylon', 'terracotta', 'plastic', 'rubber', 'cement', 'concrete', 'plaster', 'clay', 'ceramic', 'porcelain'},
    'experimental': {'table', 'toilet', 'ladder', 'bowl', 'mirror', 'beanbag', 'mattress', 'chair', 'bath', 'lamp', 'vacuum', 'sofas', 'tights', 'shoe', 'scarf', 'banknote', 'hair', 'excrement', 'dung', 'couscous', 'egg', 'coca'},
    # 'textile': {'textile', 'fibre', 'felt', 'wool', 'fabric'}
}

# badWords = ['photography', 'silver', 'gelatin', 'verso:', 'paint', 'or', 'with', 'paper']
for data in json_data:
    # Only record data if have the year
    if data['dateRange'] and data['dateRange']['startYear'] != 'no date':
        if 'endYear' in data['dateRange']:
            year = data['dateRange']['endYear']
        else:
            year = data['dateRange']['startYear']

        if isinstance(year, str):
            year = int(year)

        # Creates a new inner dict
        if year not in stats:
            stats[year] = {'mediums': {
                m: 0 for m in categories
            }, 'movements': {}, 'count': 0}

        # Adds medium to the year
        if (data['medium']):
            mediums = data['medium'].lower().split()
            mediums = {m.strip(".,") for m in mediums}
            for category in categories:
                if bool(categories[category] & mediums):
                    stats[year]['count'] += 1
                    stats[year]['mediums'][category] += 1

        if data['movementCount'] > 0:
            for movement in data['movements']:
                if movement['name'] not in stats[year]['movements']:
                    stats[year]['movements'][movement['name']] = 1
                else:
                    stats[year]['movements'][movement['name']] += 1

# Sort by year
stats = dict(sorted(stats.items()))

# Get by percentage
stats = {
    yr: {
        'mediums': dict([[m, round(stats[yr]['mediums'][m] / stats[yr]['count'], 2)] for m in stats[yr]['mediums'].keys()]),
        'movements': stats[yr]['movements'],
        'count': stats[yr]['count']
    } for yr in stats.keys()
}

# sort the mediums & movements of each year
stats = {
    yr: {
        'mediums': dict(sorted(stats[yr]['mediums'].items(), key= lambda item: item[1], reverse=True)),
        'movements': dict(sorted(stats[yr]['movements'].items(), key= lambda item: item[1], reverse=True)),
        'count': stats[yr]['count']
    } for yr in stats.keys()
}

# Dump into json file !
with open('stats.json', 'w') as outfile:
    json.dump(stats, outfile, indent=4)

# Create info about artworks !!
# mediumTypes = {}
# movementTypes = {}
# for data in json_data:
#     if (data['medium']):
#         mediums = data['medium'].lower().split()
#         mediums = [m.strip(".,") for m in mediums]
#         if "and" in mediums: mediums.remove("and")
#         if "on" in mediums: mediums.remove("on")
#         if "verso:" in mediums: mediums.remove("verso:")
#         if "paper" in mediums: mediums.remove("paper")
#         if "paint" in mediums: mediums.remove("paint")

#         for medium in mediums:
#             if medium not in mediumTypes:
#                 mediumTypes[medium] = 1
#             else:
#                 mediumTypes[medium] += 1

#     if data['movementCount'] > 0:
#         movements = []
#         for movement in data['movements']:
#             movements.append(movement['name'])

#             if movement['name'] not in movementTypes:
#                 movementTypes[movement['name']] = 1
#             else:
#                 movementTypes[movement['name']] += 1

# mediumTypes = dict(sorted(mediumTypes.items(), key=lambda item: item[1], reverse=True))
# movementTypes = dict(sorted(movementTypes.items(), key=lambda item: item[1], reverse=True))

# # Dump into files
# with open('mediumTypes.json', 'w') as outfile: 
#     json.dump(mediumTypes, outfile, indent=4)

# with open('movementTypes.json', 'w') as outfile: 
#     json.dump(movementTypes, outfile, indent=4)

# for data in json_data:
#     artwork = {
#         'id': data['id']
#     }

#     if data['dateRange'] and data['dateRange']['startYear'] != 'no date':
#         if 'endYear' in data['dateRange']:
#             artwork['year'] = data['dateRange']['endYear']
#         else:
#             artwork['year'] = data['dateRange']['startYear']
            
#     if (data['medium']):
#         mediums = data['medium'].lower().split()
#         mediums = [m.strip(".,") for m in mediums]
#         if "and" in mediums: mediums.remove("and")
#         if "on" in mediums: mediums.remove("on")
#         if "verso:" in mediums: mediums.remove("verso:")
#         if "paper" in mediums: mediums.remove("paper")
#         if "paint" in mediums: mediums.remove("paint")
#         artwork['mediums'] = mediums

#         for medium in mediums:
#             if medium not in mediumTypes:
#                 mediumTypes[medium] = 1
#             else:
#                 mediumTypes[medium] += 1

#     if data['movementCount'] > 0:
#         movements = []
#         for movement in data['movements']:
#             movements.append(movement['name'])

#             if movement = 

#         artwork['movements'] = movements

#     artworkData.append(artwork)

# mediumTypes = dict(sorted(mediumTypes.items(), key=lambda item: item[1], reverse=True))

# # Dump into a file
# with open('artworkData.json', 'w') as outfile: 
#     json.dump(artworkData, outfile)


