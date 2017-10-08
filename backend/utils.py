import random
from geopy.geocoders import Nominatim

hard_limit = 12

def load_keys():
    d = {}
    with open('secret.keys') as f:
        content = f.readlines()
    for line in content:
        line = line.split(',')
        d[line[0]] = line[1]
    return d

def rand_int(low, high):
    return random.randint(low, high)

def to_str(*strings):
    string = ""
    for each in strings:
        string += each
        if(each):
            string += ", "
    return string[:-2]


class LocationLoader():

    def __init__(self, filename, db):
        self.filename = filename
        self.geolocator = Nominatim()
        with open(filename) as f:
            content = f.readlines()
        for each in content:
            temp = each.split('-')
            p = load_place(temp[0])
            t = load_tag(temp[1][1:-2])
            db.execute('INSERT INTO results(place, latitude, longitude) VALUES (?, ?, ?)', (p[0], p[1], p[2]))
            db.commit()
            cur_row = db.fetchone('SELECT LAST_INSERT_ROWID()')[0]
            tag_ids = []
            for tag in t:
                db.execute('INSERT INTO tags(tag) VALUES (?)', (tag,))
                temp = db.fetchone('SELECT id FROM tags WHERE tag=?', (tag,))[0]
                tag_ids.append(temp)
            for relation in tag_ids:
                db.execute('INSERT INTO result_tag(r_id, t_id) VALUES (?, ?)', (cur_row, relation))

        t = load_tag(temp[1])
        tag_ids = []
        for x in t:
            x=str(x)
            print(x)
            try:
                db.execute('INSERT INTO tags(tag) VALUES (?)', (str(x),))
                cur = db.execute('SELECT id FROM tags WHERE tag=?', (str(x), ))
                temp = cur.fetchone()[0]
                tag_ids.append(temp)
            except (sqlite3.IntegrityError, sqlite3.InterfaceError):
                d['fail'] += 1
                d['description'] += "%s " % x
                print("exists")
        for relation in tag_ids:
            db.execute('INSERT INTO result_tag(r_id, t_id) VALUES (?, ?)', (cur_row, relation))
        db.commit()


    def load_place(place):
        g = self.geolocator
        s = place.split(', ')
        x = to_str(s[0], s[1], s[2])
        location = g.geocode(x)
        if(not location):
            lat, lon = 0.0, 0.0
        else:
            lat, lon = location.latitude, location.longitude
        return (x, lat, lon)

    def load_tag(tag):
        if(tag[-1]=='\n'):
            tag=tag[1:-2]
        else:
            tag=tag[1:-1]
        return tag.split(',')

