#!/bin/zsh

GREEN='\033[0;32m'
NC='\033[0m'

# Function to unlock .c files
unlock_c_files() {
  local directory="$1"
  local password="$2"
  # Find all .c files in the specified directory and its subdirectories
  find "$directory" -type f -name "*.c.gpg" | while read -r file; do
    # Decrypt the file with GPG using symmetric decryption
    gpg --quiet --decrypt --passphrase "$password" "$file" > "${file%.gpg}"
    # Remove the encrypted file after decryption
    rm "$file"
    echo "Unlocked ${file%.gpg}"
  done
}

# Function to unlock a password-protected directory
unlock_directory() {
  local directory="$1"
  local password="$2"
  # Decrypt the directory with GPG using symmetric decryption
  gpg --quiet --decrypt --passphrase "$password" "$directory.tar.gz.gpg" | tar -xz
  # Remove the encrypted tarball after decryption
  rm "$directory.tar.gz.gpg"
  echo "Unlocked directory: $directory"
}

# Function to unlock .c files and directories in the specified directory and its subdirectories
unlock_recursive() {
  local directory="$1"
  local password="$2"
  # Unlock .c files in the specified directory
  unlock_c_files "$directory" "$password"
  # Unlock the directory and its contents
  unlock_directory "$directory" "$password"
}

# Check if a directory and password are provided as arguments
if [ "$#" -eq 2 ]; then
  directory="$1"
  password="$2"
  # Unlock .c files and directories in the specified directory and its subdirectories
  unlock_recursive "$directory" "$password"
else
  # If no directory or password is provided, display an error message
  echo "Usage: $0 <directory> <password>"
fi


echo "${GREEN}Files have been unlocked, lock your pc the next time${NC}"
