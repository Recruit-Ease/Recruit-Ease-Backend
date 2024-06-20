from django.core import signing

def encrypt(data):
    # Serialize and sign the data
    signed_data = signing.dumps(data)
    return signed_data

def decrypt(signed_data):
    try:
        # Verify and deserialize the signed data
        data = signing.loads(signed_data)
        return data
    except signing.BadSignature:
        # Handle invalid or tampered data
        return None