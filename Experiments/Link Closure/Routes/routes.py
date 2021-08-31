import pandas
import os
import csv

routes_eb, routes_wb  = read_routes(os.path.join(routePath,r1, f1)), read_routes(os.path.join(routePath,r1, f2))
print("Number of legs crossing RSR EB: %s, WB %d" %(len(routes_eb),len(routes_wb)))
normal_links = link_counts(routes_eb, routes_wb)

closureroutes_eb, closureroutes_wb = read_routes(os.path.join(routePath,r2, f1)), read_routes(os.path.join(routePath,r2, f2))
print("Number of legs crossing RSR EB: %s, WB %d on Closure day" %(len(closureroutes_eb),len(closureroutes_wb)))

# We are interested in the legs that were unable to cross bridge due to link closure.
print("Number of legs that couldnt cross ", len(routes_eb)+len(routes_wb)-len(closureroutes_eb)-len(closureroutes_wb))

def main_normal():
    reroutedlegs_eb = list(routes_eb.keys() - closureroutes_eb.keys())
    reroutedlegs_wb = list(routes_wb.keys() - closureroutes_wb.keys())
    rerouted_eb = {req_key: routes_eb[req_key] for req_key in reroutedlegs_eb }
    rerouted_wb = {req_key: routes_wb[req_key] for req_key in reroutedlegs_wb }

    normallinks_55k = {}
    for v in rerouted_eb.values():
        for eachv in v:
            if eachv not in normallinks_55k:
                normallinks_55k[eachv] = 1
            else:
                normallinks_55k[eachv] += 1
    print("Number of links used by EB legs", len(normallinks_55k))
    for v in rerouted_wb.values():
        for eachv in v:
            if eachv not in normallinks_55k:
                normallinks_55k[eachv] = 1
            else:
                normallinks_55k[eachv] += 1
    print("Number of total links used by both direc legs", len(normallinks_55k))

def main_closure():
    closureroutes = read_routes(os.path.join(routePath,r2,'routes.csv')
    closurererouted_eb = {req_key: closureroutes[req_key] for req_key in reroutedlegs_eb }
    closurererouted_wb = {req_key: closureroutes[req_key] for req_key in reroutedlegs_wb }

    closurelinks_55k = {}
    for v in closurererouted_eb.values():
        for eachv in v:
            if eachv not in closurelinks_55k:
                closurelinks_55k[eachv] = 1
            else:
                closurelinks_55k[eachv] += 1
    print("Number of links used by EB legs", len(closurelinks_55k))
    for v in closurererouted_wb.values():
        for eachv in v:
            if eachv not in closurelinks_55k:
                closurelinks_55k[eachv] = 1
            else:
                closurelinks_55k[eachv] += 1

    print("Number of total links used by both direc legs", len(closurelinks_55k))
