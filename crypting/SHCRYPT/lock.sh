#!/bin/zsh

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Encrypt function with progress bar
encrypt() {
    local key="$1"
    local filename="$2"
    local outFile="$filename.encrypted"
    local fileSize=$(stat -c %s "$filename")
    local IV=""

    for _ in {1..16}; do
        IV+=$(printf "%02x" $(( RANDOM % 256 )))
    done

    printf "$fileSize" | awk '{printf "%016d", $1}' > "$outFile"
    printf "$IV" > "$outFile.iv"

    cat "$filename" | openssl enc -aes-256-cbc -K "$key" -iv "$IV" -e -pbkdf2 > "$outFile"

    rm -f "$filename" # Remove the original file after encryption
}

# Main function
main() {
    local password

    echo -e "${BLUE}Enter the passphrase: ${NC}"
    read -rs password

    # Encrypt all files in the current directory and subdirectories
    for file in $(find . -type f); do
        encrypt "$(echo -n "$password" | sha256sum | cut -d" " -f1)" "$file"
        printf "${GREEN}Encrypted: $file${NC}\n"
    done

    printf "${GREEN}All files have been encrypted.${NC}\n"
}

# Call the main function
main

