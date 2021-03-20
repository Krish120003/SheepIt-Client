import bpy
import json

cuda, opencl = bpy.context.preferences.addons['cycles'].preferences.get_devices()

data = {"CUDA":[(item.id, item.name) for item in cuda], "OPENCL":[(item.id, item.name) for item in opencl]}

print(uid,json.dumps(data))

{"CUDA": [["CUDA_GeForce RTX 2060_0000:01:00", "GeForce RTX 2060"], ["CPU", "Intel Core i5-9300HF CPU @ 2.40GHz"]], "OPENCL": [["CPU", "Intel Core i5-9300HF CPU @ 2.40GHz"]]}