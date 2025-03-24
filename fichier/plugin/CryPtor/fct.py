

def crypt(text, cle):
    result = ""
    # transverse the plain text
    t = 0
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            # Encrypt uppercase characters in plain text
            if (t % 2) == 0:
                if (char.isupper()):
                    result += chr((ord(char) + int(cle) - 65) % 26 + 65)
                # Encrypt lowercase characters in plain text
                else:
                    result += chr((ord(char) + int(cle) - 97) % 26 + 97)
            else:
                if (char.isupper()):
                    result += chr((ord(char) + int(cle) + 65) % 26 + 65)
                # Encrypt lowercase characters in plain text
                else:
                    result += chr((ord(char) + int(cle) + 97) % 26 + 97)

        elif char.isdigit():
            result += str(int(char)+int(cle))
        else:
            result += "_"
        t +=1
    return result