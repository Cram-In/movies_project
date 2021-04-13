def get_id(cast, actor):
    for dict_item in cast:
        if dict_item["name"] == actor:
            person_id = dict_item["id"]
            return person_id