
describers = {1: {"img1": {"d1": "des1"}, "img2": {"d2": "des2"}}, 2: {"img1": {"d3": "des3"}, "img2": {"d4": "des4"}}}
a = 3
b = "img1"
describers[a] = {b: {"d5": "des5"}, "img2": {"d6": "des6"}}



def get_img_id(d):
    # self.describers: {1: {"img1": {"d1": "des1"}, "img2": {"d2": "des2"}}, 2: {"img1": {"d3": "des3"}, "img2": {"d4": "des4"}}}
    # self.describers.values(): {"img1": {"d1": "des1"}, "img2": {"d2": "des2"}}, {"img1": {"d3": "des3"}, "img2": {"d4": "des4"}}
    for values in describers.values():
        for k, v in values.items(): # "img1": {"d1": "des1"}, "img2": {"d2": "des2"}
            if d in v:
                return k
    return None

print(get_img_id("d1"))

describers.get(1)["img4"] = {"d7": "des7"}

print(describers)

def get_descriptions():
    des = {}
    for v in describers.values():
        for i in v.values():
            des.update(i)
    return des

des = get_descriptions()

print(des)

for i, k in des.items():
    print(i + ":" + k)