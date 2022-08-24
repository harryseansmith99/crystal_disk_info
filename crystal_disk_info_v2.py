import os
from pathlib import Path
import re
from prometheus_client import CollectorRegistry, Gauge, write_to_textfile


def run_regexes(input_filepath, output_filepath, regex):
    """ Run a list of regex matches on an input file, and generate an output. """
    results = dict()

    temp = dict()
    temp_list = []

    with open(input_filepath, 'r') as extract:
        for line in extract.readlines():
            for key, reg in regex.items():
                test = re.findall(reg, line)
                if not test == []:
                    new_regex = reg_expr_specific_info.get(key)
                    test = re.search(new_regex, line)
                    if test:
                        temp[key] = test.group(1)
                        if key == "Drive":
                            temp_list.append(temp)
                            print(temp)
                            temp = dict()
                            break

    
    print(temp_list)

    for i in temp_list:
        temp = dict()
        temp["Model"] = i.get("Model")
        temp["Disk"] = i.get("Disk")
        temp["Temperature"] = i.get("Temperature")
        temp["Health"] = i.get("Health")
        results[i.get("Drive")] = temp


    print("----------------")

    print("'results' dict ->   ", results, "\n")


    registry = CollectorRegistry()

    g = Gauge('drive_status', '1 if drive_status is present', registry=registry, labelnames=["drive_name", "model", "size", "temperature", "status"])


    try:
        for each_drive, drive_details in results.items():
            g.labels (
                drive_name = each_drive, 
                model = drive_details.get("Model", 0), 
                size = drive_details.get("Disk", 0), 
                temperature = drive_details.get("Temperature", 0), 
                status = drive_details.get("Health", 0)
            ).set(1)

        write_to_textfile(output_filepath, registry)

    except Exception:
        print("An error occured -> ", Exception, "\nDefault value set to 0")
        for each_drive, drive_results in results.items():
            g.labels (
                drive_name = each_drive, 
                model = drive_results.get("Model", 0), 
                size = drive_results.get("Disk", 0), 
                temperature = drive_results.get("Temperature", 0), 
                status = drive_results.get("Health", 0)
                ).set(0)

        write_to_textfile(output_filepath, registry)


# execute DiskInfo command, specify regex expressions for search
if __name__ == "__main__":

    os.chdir("C:\\CrystalDiskInfo8_17_3")
    os.system("DiskInfo64.exe /CopyExit")
    diskinfo = r"C:\CrystalDiskInfo8_17_3\DiskInfo.txt"

    path = Path(diskinfo)
    if path.is_file():
        print(f"\nThe file {diskinfo} exists\n")
    else:
        print(f"\nThe file {diskinfo} does not exist\n")

    output = r"C:\CrystalDiskInfo8_17_3\results.prom"    # only needed if writing to file

    reg_expr = {
        'Disk': r".*\ Disk.*",
        'Temperature': r".*\ \ Temperature.*",
        'Model': r".*Model.*",
        'Health': r".*Health Status.*",
        'Drive': r".*Drive.*"
    }
    
    reg_expr_specific_info = {
        'Disk': r":\s(\d+)",
        'Temperature': r"(\d{1,2})",
        'Model': r":\s(.*)",
        'Health': r":\s(\w{1,4})",
        'Drive': r":\s(\w)"
    }
    

    run_regexes(diskinfo, output, reg_expr)