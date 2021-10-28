import sqlite3
import random


def correlate(type, color=None):
    dct = {'table': ['chair', 'swivelchair'], 'wardrobe': ['dresser', 'bed', 'sofa'], 'armchair': ['sofa'],
           'bed': ['wardrobe', 'sofa', 'dresser'], 'chair': ['table'], 'dresser': ['wardrobe', 'bed'], 'sofa': ['wardrobe'],
           'swivelchair': ['table']}
    colors = {'yellow': ['red', 'blue', 'dark pink', 'green'], 'orange': ['pink', 'blue'],
              'red': ['blue', 'yellow', 'dark blue'],
              'pink': ['orange', 'blue'], 'black': 'white', 'dark blue': ['red', 'yellow'], 'white': 'black',
              'green': 'yellow', 'dark brown': 'blue'}
    colors_corr = colors[color]
    con = sqlite3.connect('db/furniture.db')
    cur = con.cursor()
    types = tuple(dct[type])
    param_holders = ",".join("?" for i in types)
    res = cur.execute(f'''SELECT furniture.link, furniture.photo_id, furniture.color, type.type FROM [furniture], [type]
                          WHERE type.type IN (%s) AND furniture.type_id == type.id''' % param_holders, types).fetchall()
    res_furn = set()
    lst = list()
    ids = list()
    for i in res:
        res_furn.add(i[-1])
        if i[-2] in colors_corr:
            ids.append((i[0], i[1], i[-1]))
    true_types = list()
    for i in range(3):
        result = random.choice(ids)
        if result[-1] not in lst:
            lst.append(result[-1])
            true_types.append(result)
    while len(true_types) != 3:
        true_types.append(random.choice(ids))

    return true_types
