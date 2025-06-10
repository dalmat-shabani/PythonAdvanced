from Tools.scripts.make_ctype import values

contact_info ={
    "Kroni" : "555-1234",
    "Rroni" : "123232-211"
}

print(contact_info)

kroni_phone = contact_info["Kroni"]
print(kroni_phone)


contact_info["Rroni"] = "1234-567"
print(contact_info)


contact_info["Dalmati"] = "555-5555"
print(contact_info)



del contact_info["Kroni"]
print(contact_info)


keys = contact_info.keys()
print(keys)


values= contact_info.values()
print(values)


items = contact_info.items()
print(items)