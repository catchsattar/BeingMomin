from AmbassadorPortal.models import people


def get_person_from_id(pid):
    person = people.objects.get(id=pid)
    return person

