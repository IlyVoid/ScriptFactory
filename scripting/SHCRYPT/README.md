<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabolical-scripting-piscine</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            overflow: auto;
        }
        code {
            font-family: monospace;
        }
        .code-block {
            margin-bottom: 20px;
        }
        .code-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .comment {
            color: #888;
        }
        .keyword {
            color: #0077cc;
        }
        .function {
            color: #00a000;
        }
        .variable {
            color: #c7254e;
        }
        .string {
            color: #d14;
        }
        .output {
            color: #0000cc;
        }
        .success {
            color: #008000;
        }
        .error {
            color: #b94a48;
        }
    </style>
</head>
<body>

<h1>lock.sh</h1>
<div class="code-block">
    <div class="code-title">lock.sh</div>
    <pre><code class="bash">
#!/bin/zsh

# Define colors
<span class="variable">RED</span>='\033[0;31m'
<span class="variable">GREEN</span>='\033[0;32m'
<span class="variable">BLUE</span>='\033[0;34m'
<span class="variable">NC</span>='\033[0m' # No Color

# Encrypt function with progress bar
<span class="function">encrypt</span>() {
    local key="$<span class="variable">1</span>"
    local filename="$<span class="variable">2</span>"
    local outFile="$filename.encrypted"
    local fileSize=$(stat -c %s "$filename")
    local IV=""

    for _ in {1..16}; do
        IV+=$(printf "%02x" $(( RANDOM % 256 )))
    done

    printf "$fileSize" | awk '{printf "%016d", $<span class="variable">1</span>}' &gt; "$outFile"
    printf "$IV" &gt; "$outFile.iv"

    cat "$filename" | openssl enc -aes-256-cbc -K "$key" -iv "$IV" -e -pbkdf2 &gt; "$outFile"

    rm -f "$filename" # Remove the original file after encryption
}

# Main function
<span class="function">main</span>() {
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
    </code></pre>
</div>

<h1>unlock.sh</h1>
<div class="code-block">
    <div class="code-title">unlock.sh</div>
    <pre><code class="bash">
#!/bin/zsh

# Define colors
<span class="variable">RED</span>='\033[0;31m'
<span class="variable">GREEN</span>='\033[0;32m'
<span class="variable">BLUE</span>='\033[0;34m'
<span class="variable">NC</span>='\033[0m' # No Color

# Decrypt function
<span class="function">decrypt</span>() {
    local key="$<span class="variable">1</span>"
    local encryptedFile="$<span class="variable">2</span>"
    local outFile="${encryptedFile%.encrypted}"
    local IVFile="$encryptedFile.iv"
    local IV=""
    local fileSize=0

    # Read IV from IV file
    IV=$(cat "$IVFile")
    # Remove IV file
    rm -f "$IVFile"

    # Get file size
    IFS= read -r -n 16 fileSize &lt; "$encryptedFile"

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
<span class="function">main</span>() {
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
    </code></pre>
</div>

</body>
</html>

