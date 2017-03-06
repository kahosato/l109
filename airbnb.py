import csv

from util import gen_listings, gen_fsq_nodes, read_partitions


def _compute_distance(listing, fsq_node):
    return pow(pow((listing["longitude"] - fsq_node["longtitude"]), 2)
               + pow((listing["latitude"] - fsq_node["latitude"]), 2), 0.5)


def assign_community(listings, fsq_nodes, d_fsq_comm, output, comm_list, nbh_list):
    # todo: iterate through listings, assign fsq community and output
    # 30 valid communities. IF the closest one is not valid then ignore
    with open(output, 'w') as f:
        f.write("id,latitude,longitude,neighbourhood,comm\n")
        for lid, listing in listings.iteritems():
            first_n_id, first_node = fsq_nodes.iteritems().next()
            min_distance = _compute_distance(listing, first_node)
            closest = first_n_id
            for n_id, n in fsq_nodes.iteritems():
                if _compute_distance(listing, n) < min_distance:
                    closest = n_id
            comm = d_fsq_comm[closest]
            neighbourhood = listing["neighbourhood"]
            if comm in comm_list and neighbourhood in nbh_list:
                f.write("{},{},{},{},{}\n".format(lid, listing["latitude"], listing["longitude"], neighbourhood, comm))
                print "{},{},{},{},{}\n".format(lid, listing["latitude"], listing["longitude"], neighbourhood, comm)

def gen_nbh_list():
    to_return = set()
    with open("abnb_filtered_nbh.txt") as f:
        for l in f:
            to_return.add(l.strip())
    return to_return

def gen_comm_list():
    with open("30_fsq_comm_correct.txt") as f:
        comms = map(int, f.read().strip().split(" "))
        return set(comms)

def gen_filtered_abnb_data(input="abnb.csv"):
    # read abnb csv
    to_return = {}
    with open(input, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            to_return[int(row["id"])] = {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "neighbourhood": row["neighbourhood"],
                "comm": int(row["comm"])
            }
    return to_return

def compute_accuracy(input="abnb.csv"):
    abnb = gen_filtered_abnb_data(input)
    nbh_listings = {}
    for lid, l in abnb.iteritems():
        if not l["neighbourhood"] in nbh_listings:
            nbh_listings[l["neighbourhood"]] = set()
        lst_in_n = nbh_listings[l["neighbourhood"]]
        lst_in_n.add(lid)
    accuracy = {}
    total_correct = 0
    nbh_fsq_comm = {}
    total_count = 0
    for n, ls in nbh_listings.iteritems():
        counter_for_n = {}
        for lid in ls:
            l = abnb[lid]
            fsq_comm_id = l["comm"]
            total_count += 1
            if fsq_comm_id not in counter_for_n:
                counter_for_n[fsq_comm_id] = 0
            counter_for_n[fsq_comm_id] += 1
        max_count = 0
        chosen_fsq_comm = None
        total_count_in_n = 0
        for fsq_comm_id, count in counter_for_n.iteritems():
            if count > max_count:
                chosen_fsq_comm = fsq_comm_id
                max_count = count
            total_count_in_n += count
        nbh_fsq_comm[n] = chosen_fsq_comm
        accuracy[n] = float(max_count) / total_count_in_n
        total_correct += max_count
    total_accuracy = float(total_correct) / total_count
    return total_accuracy, accuracy

if __name__ == "__main__":
    ta, a = compute_accuracy()
    print ta
    print a
