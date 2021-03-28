import uuid


def get_randon_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code
