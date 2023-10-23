from django.template.defaultfilters import title


# def findminmax (name):
#     new_name = []
#     a = iter(name)
#     x = next(a)
#     new_name.append(x.upper())
#     while True:
#         try:
#             x = next(a)
#             new_name.append(x.lower())
#         except StopIteration:
#             break
#     new_name = ''.join(new_name)
#     return new_name

if __name__ == "__main__":
    # name = ['Adam', 'Lisa', 'Bart']
    # r =  map(title, name)
    # print("ced+++:",list(r))
    from functools import reduce


    def string_to_float(string):
        return reduce(lambda x, y: x * 10 + y, map(int, string.split('.'))) / (10 ** len(string.split('.')[1]))


    string = "3.14"
    float_number = string_to_float(string)
    print(float_number)
    #print(list(filter(huishu,[[12321],[123454321],[321312]])))

