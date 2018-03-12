from database.operate import connector
import sys, getopt, json

#table has country code: aiwen_data, ip2location_data, ip2locationlite_data, maxmind_data

def countryQuery(table, countryCode, filename):
    if table == "" or countryCode == "" or filename == "":
        print "need -t, -c, -o param"
        return -1
    param_list = ["ip_from", "ip_to"]
    conn = connector()
    result = conn.searchall(table, param_list, "country_code = '%s'" % countryCode)
    conn.close()
    outfp = open(filename, "w")
    json.dump(result, outfp, indent = 4)
    outfp.close()
    return 0

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:t:o:",["output="])
        filename = ""
        table = ""
        countryCode = ""
        for opt, arg in opts:
            if opt == "-o":
                filename = arg
            elif opt == "-t":
                table = arg
            elif opt == "-c":
                countryCode = arg
        if countryQuery(table, countryCode, filename):
            print "failed."
        else:
            print "success."
    except getopt.GetoptError:
        sys.exit()
