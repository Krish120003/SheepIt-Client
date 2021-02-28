import psutil
import platform
import cpuinfo


def sheep_system_info():

    temp = cpuinfo.get_cpu_info()

    info = {}

    info["os"] = platform.system().lower().replace("Darwin", "mac")

    info["cpu_family"] = temp["family"]
    info["cpu_model"] = temp["model"]
    info["cpu_model_name"] = temp["brand_raw"]
    info["cpu_cores"] = temp["count"]
    info["bits"] = str(temp["bits"]) + "bit"

    info["ram_max"] = psutil.virtual_memory().total // 1024

    info["headless"] = 0

    return info


if __name__ == "__main__":
    print(sheep_system_info())