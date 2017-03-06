from airbnb import gen_comm_list
from util import read_partitions, gen_fsq_nodes


def gen_comm_csv(fsq_nodes, d_fsq_comm, comm_list, output):
    with open(output, 'w') as f:
        f.write("id, longitude, latitude, comm\n")
        for nid, n in fsq_nodes.iteritems():
            comm = d_fsq_comm[nid]
            if comm in comm_list:
                f.write("{},{},{},{}\n".format(nid, n["longtitude"], n["latitude"], comm))
                print "{},{},{},{}\n".format(nid, n["longtitude"], n["latitude"], comm)

if __name__ == "__main__":
    gen_comm_csv(gen_fsq_nodes(), read_partitions(), gen_comm_list(), "fsq.csv")