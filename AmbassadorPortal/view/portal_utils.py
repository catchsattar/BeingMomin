from AmbassadorPortal.models import people, locality_mapping


def get_person_from_id(pid):
    return people.objects.get(id=pid)


def get_locality_from_name(locality_key):
    return locality_mapping.objects.get(locality_key=locality_key)


