#!/bin/zsh

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Decrypt function
decrypt() {
    local key="$1"
    local encryptedFile="$2"
    local outFile="${encryptedFile%.encrypted}"
    local IVFile="$encryptedFile.iv"
    local IV=""
    local fileSize=0

    # Read IV from IV file
    IV=$(cat "$IVFile")
    # Remove IV file
    rm -f "$IVFile"

    # Get file size
    IFS= read -r -n 16 fileSize < "$encryptedFile"

    # Decrypt file
    openssl enc -aes-256-cbc -K "$key" -iv "$IV" -d -in "$encryptedFile" -out "$outFile.tmp"

    # Check if decryption was successful
    if [ $? -eq 0 ]; then
        mv "$outFile.tmp" "$outFile" # Rename decrypted file
        printf "${GREEN}Decrypted: $outFile${NC}\n"
    else
        printf "${RED}Failed to decrypt: $encryptedFile${NC}\n"
        rm -f "$outFile.tmp" # Remove temporary file
    fi

    # Remove encrypted file
    rm -f "$encryptedFile"
}

# Main function
main() {
    local password

    echo -e "${BLUE}Enter the passphrase: ${NC}"
    read -rs password

    # Decrypt all encrypted files in the current directory and subdirectories
    for file in $(find . -type f -name "*.encrypted"); do
        decrypt "$(echo -n "$password" | sha256sum | cut -d" " -f1)" "$file"
    done

    printf "${GREEN}All files have been decrypted.${NC}\n"
}

# Call the main function
main

