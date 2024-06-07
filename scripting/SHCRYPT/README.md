<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cryptographic File Encryption and Decryption with SHELL</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 20px;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 5px;
        }
        p {
            margin-bottom: 10px;
        }
        ul {
            margin-bottom: 10px;
        }
        li {
            margin-left: 20px;
        }
    </style>
</head>
<body>

<h1>Cryptographic File Encryption and Decryption</h1>
<p>This shell script provides functionality for encrypting and decrypting files using AES encryption with CBC mode and SHA-256 hashing.</p>

<h2>Usage</h2>
<p>Before running the script, make sure you have the necessary dependencies installed:</p>
<ul>
    <li>OpenSSL</li>
    <li>zsh shell</li>
</ul>

<h3>Encrypting Files</h3>
<p>To encrypt files, run the script and choose the option to encrypt (E). You will be prompted to enter a passphrase. The script will then encrypt all files in the current directory recursively. Encrypted files will have the ".encrypted" extension added to their names.</p>
<pre><code>./lock.sh</code></pre>

<h3>Decrypting Files</h3>
<p>To decrypt files, run the script and choose the option to decrypt (D). You will be prompted to enter the filename of the encrypted file you want to decrypt and the passphrase used for encryption. The decrypted file will be saved in the same directory without the ".encrypted" extension.</p>
<pre><code>./unlock.sh</code></pre>

<h2>Dependencies</h2>
<ul>
    <li>OpenSSL: For AES encryption and decryption.</li>
    <li>zsh shell</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.</p>

</body>
</html>
