import struct

# ================= AES (SIMPLIFIED) =================

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def key_expansion(key):
    return [key] * 11  # simplified

def aes_encrypt_block(block, round_keys):
    return xor_bytes(block, round_keys[0])


# ================= CMAC =================

def cmac(key_hex, message_str):
    try:
        key_bytes = bytes.fromhex(key_hex)
        if len(key_bytes) != 16:
            print("Key must be 32 hex chars!")
            return
    except:
        print("Invalid Key Format!")
        return

    message = message_str.encode()

    BLOCK_SIZE = 16

    # Padding
    if len(message) % BLOCK_SIZE != 0:
        pad_len = BLOCK_SIZE - (len(message) % BLOCK_SIZE)
        message += b'\x80' + b'\x00' * (pad_len - 1)

    # Split into blocks
    blocks = [message[i:i+16] for i in range(0, len(message), 16)]

    round_keys = key_expansion(key_bytes)

    X = b'\x00' * 16

    for block in blocks:
        xored = xor_bytes(X, block)
        X = aes_encrypt_block(xored, round_keys)

    print("CMAC:", X.hex().upper())


# ================= SHA-512 =================

MASK64 = 0xFFFFFFFFFFFFFFFF

def rotr(x,n): return ((x>>n)|(x<<(64-n))) & MASK64
def ch(x,y,z): return (x&y) ^ (~x&z)
def maj(x,y,z): return (x&y) ^ (x&z) ^ (y&z)
def s0(x): return rotr(x,1)^rotr(x,8)^(x>>7)
def s1(x): return rotr(x,19)^rotr(x,61)^(x>>6)
def S0(x): return rotr(x,28)^rotr(x,34)^rotr(x,39)
def S1(x): return rotr(x,14)^rotr(x,18)^rotr(x,41)

H = [
0x6a09e667f3bcc908,0xbb67ae8584caa73b,0x3c6ef372fe94f82b,0xa54ff53a5f1d36f1,
0x510e527fade682d1,0x9b05688c2b3e6c1f,0x1f83d9abfb41bd6b,0x5be0cd19137e2179]

def sha512(msg):
    msg_bytes = msg.encode()
    msg = bytearray(msg_bytes)
    l = len(msg)*8

    msg.append(0x80)
    while len(msg)%128 != 112:
        msg.append(0)
    msg += l.to_bytes(16,'big')

    h = H[:]

    for i in range(0,len(msg),128):
        w = list(struct.unpack('>16Q', msg[i:i+128])) + [0]*64

        for j in range(16,80):
            w[j] = (w[j-16]+s0(w[j-15])+w[j-7]+s1(w[j-2])) & MASK64

        a,b,c,d,e,f,g,hh = h

        for j in range(80):
            T1 = (hh + S1(e) + ch(e,f,g) + w[j]) & MASK64
            T2 = (S0(a) + maj(a,b,c)) & MASK64
            hh,g,f,e,d,c,b,a = g,f,e,(d+T1)&MASK64,c,b,a,(T1+T2)&MASK64

        h = [(x+y)&MASK64 for x,y in zip(h,[a,b,c,d,e,f,g,hh])]

    digest = ''.join(f"{x:016x}" for x in h).upper()
    print("SHA-512:", digest)


# ================= MAIN PROGRAM =================

print("1. SHA-512")
print("2. CMAC")

choice = input("Enter choice: ")

message = input("Enter message: ")

if choice == "1":
    sha512(message)

elif choice == "2":
    key = input("Enter key (32 hex chars): ")
    cmac(key, message)

else:
    print("Invalid choice")
