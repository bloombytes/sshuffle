# SSHuffle

> A Python script for transferring files using Secure Copy Protocol and File Transfer Protocol

<br>

## Features

> - Transfers entire directories recursively
> - Progress bar for process monitoring
> - Logs file transfer details
> - File integrity verification
> - File compression (optional)
> - Support for custom FTP port
> - Anonymous FTP session (optional)

<br>

## Prerequisites

> - Python 3.x
> - ftplib 
> - paramiko  
>   - `pip install paramiko`
> - progressbar  
>   - `pip install progressbar2`

<br>

### Command-line Options

  > 
  > `--anonymous`: Perform an anonymous FTP session 
  > 
  
<br>
  
## Usage

```shell
python sshuffle.py [options]
```

<br>

 ### Examples
>   Download a file using SCP and upload it to an FTP server:
>
>  ```shell
>  python sshuffle.py --source-host abc.example.org --source-username ssh-admin --source-password changeme --source-file /path/to/source_file --local-file local_file.txt --destination-host ftp.example.org --destination-username ftp-user --destination-password Welcome1 --destination-file /path/to/destination_file
>  ```
##
>   Transfer an entire directory recursively:
>
> ```shell
> python sshuffle.py --source-host 10.10.0.5 --source-username webmaster --source-password password2023 --source-directory /etc/bin/plugins/ --local-directory /path/to/local_directory --destination-host 192.168.1.2 --destination-username  --destination-password pass2 --destination-directory /path/to/destination_directory --compress --ftp-port 2121
> ```
##
