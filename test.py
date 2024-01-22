import random

def mask_string(message):
    # Convert the message to bytes
    byte_message = bytes(message, 'utf-8')

    # Generate two random bytes
    random_byte1 = random.randint(0, 255)
    random_byte2 = random.randint(0, 255)

    # XOR each bit of the message with the corresponding bit in the random bytes
    masked_message = bytes(x ^ y for x, y in zip(byte_message, [random_byte1, random_byte2]))

    return masked_message, random_byte1, random_byte2

def unmask_string(masked_message, random_byte1, random_byte2):
    # XOR each bit of the masked message with the corresponding bit in the random bytes
    original_message = bytes(x ^ y for x, y in zip(masked_message, [random_byte1, random_byte2]))

    return original_message

# Example usage
original_message = 'Hello world!'
print(f"Original message: {original_message}")

# Mask the message
masked_message, random_byte1, random_byte2 = mask_string(original_message)
print(f"Random Byte 1: {random_byte1}")
print(f"Random Byte 2: {random_byte2}")
print(f"Masked message: {masked_message}")

# Unmask the message
restored_message = unmask_string(masked_message, random_byte1, random_byte2)
print(f"Restored message: {restored_message}")
