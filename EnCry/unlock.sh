#!/bin/zsh

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Decrypt function
decrypt() {
    local encryptedFile="$1"
    local IVFile="$encryptedFile.iv"
    local IV=""
    local password
    local key
    local success=0

    # Read IV from IV file
    IV=$(cat "$IVFile")

    while true; do
        # Prompt for passphrase
        printf "${BLUE}Enter the passphrase for $encryptedFile: ${NC}\n"
        read -rs password
        key="$(echo -n "$password" | sha256sum | cut -d" " -f1)"

        # Attempt to decrypt file
        openssl enc -aes-256-cbc -K "$key" -iv "$IV" -d -in "$encryptedFile" -out "${encryptedFile%.encrypted}.tmp"

        # Check if decryption was successful
        if [ $? -eq 0 ]; then
            mv "${encryptedFile%.encrypted}.tmp" "${encryptedFile%.encrypted}" # Rename decrypted file
            printf "${GREEN}Successfully decrypted: ${encryptedFile%.encrypted}${NC}\n"
            rm -f "$encryptedFile" # Remove the encrypted file after successful decryption
			rm -rf "$IVFile"
            success=1
            break
        else
            printf "${RED}Failed to decrypt: $encryptedFile. Please try again.${NC}\n"
            rm -f "${encryptedFile%.encrypted}.tmp" # Clean up any temporary files created during decryption

            # Ask if the user wants to continue trying or exit
            printf "${BLUE}Would you like to try again? (y/n): ${NC}"
            read -r answer

            if [[ "$answer" != "y" ]]; then
                printf "${RED}Keeping the encrypted file: $encryptedFile.${NC}\n"
                break
            fi
        fi
    done

    return $success
}

# Main function
main() {
    # Decrypt all encrypted files in the current directory and subdirectories
    for file in $(find . -type f -name "*.encrypted"); do
        decrypt "$file"
    done

    printf "${GREEN}Decryption process completed.${NC}\n"
}

# Call the main function
main

