import csv

def read_routes(path):
    rows = []
    routes_hash = {}
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    for i in range(len(rows)):
        routes_hash[int(rows[i][0])] = [int(j) for j in rows[i][1].split(',')[1:-2]] + [int(rows[i][1].split(',')[0].replace('[',''))] + [int(rows[i][1].split(',')[-1].replace(']',''))]
    return routes_hash

def link_counts(routes_eb, routes_wb):
    normal_links = {}
    for v in routes_eb.values():
        for eachv in v:
            if eachv not in normal_links:
                normal_links[eachv] = 1
            else:
                normal_links[eachv] += 1
    print("Number of links used by legs EB", len(normal_links)
    for v in routes_wb.values():
        for eachv in v:
            if eachv not in normal_links:
                normal_links[eachv] = 1
            else:
                normal_links[eachv] += 1

    print("Number of total links used by both direc legs", len(normal_links))
    return normal_links
