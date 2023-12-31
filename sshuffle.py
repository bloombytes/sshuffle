from ftplib import FTP
import argparse, paramiko, sys, os, hashlib, tarfile, logging, progressbar

def progress_bar_create(file_size):
    return progressbar.ProgressBar(maxval=file_size,
                                   widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

def download_directory(sftp, source_directory, local_directory):
    os.makedirs(local_directory, exist_ok=True)

    for root, dirs, files in sftp.walk(source_directory):
        relative_path = os.path.relpath(root, source_directory)
        local_dir = os.path.join(local_directory, relative_path)
        os.makedirs(local_dir, exist_ok=True)

        for file in files:
            remote_file = os.path.join(root, file)
            local_file = os.path.join(local_dir, file)

            file_size = sftp.stat(remote_file).st_size
            bar = progress_bar_create(file_size)
            bar.start()

            def callback(bytes_so_far, total_size):
                bar.update(bytes_so_far)

            sftp.get(remote_file, local_file, callback=callback)
            bar.finish()
            print("File downloaded successfully:", remote_file)

def upload_directory(ftp, destination_directory, local_directory):
    ftp.cwd(destination_directory)

    for root, dirs, files in os.walk(local_directory):
        relative_path = os.path.relpath(root, local_directory)

        for dir in dirs:
            remote_dir = os.path.join(destination_directory, relative_path, dir)
            ftp.mkd(remote_dir)

        for file in files:
            local_file = os.path.join(root, file)
            remote_file = os.path.join(destination_directory, relative_path, file)

            bar = progress_bar_create(os.path.getsize(local_file))
            bar.start()

            def callback(bytes_so_far):
                bar.update(bytes_so_far)

            with open(local_file, 'rb') as f:
                ftp.storbinary('STOR ' + remote_file, f, callback=callback)
            bar.finish()
            print("File uploaded successfully:", remote_file)

def main():
    logging.info("Downloading directory from %s:%s", args.source_host, args.source_directory)

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(args.source_host, username=args.source_username, password=args.source_password)
            with ssh.open_sftp() as sftp:
                download_directory(sftp, args.source_directory, args.local_directory)

        if args.compress:
            compressed_file = args.local_directory + '.tar.gz'
            logging.info("Compressing directory to %s", compressed_file)
            compress_directory(args.local_directory, compressed_file)
            args.local_directory = compressed_file

        if args.verify:
            logging.info("Verifying checksum")
            checksum_matched = verify_checksum(args.local_directory, args.verify)
            if checksum_matched:
                logging.info("Checksum matched.")
            else:
                logging.error("Checksum verification failed.")
                sys.exit(1)

        logging.info("Uploading directory to %s:%s", args.destination_host, args.destination_directory)

        with FTP(args.destination_host) as ftp:
            if args.destination_username:
                ftp.login(user=args.destination_username, passwd=args.destination_password)
            else:
                ftp.login('anonymous', '')
            upload_directory(ftp, args.destination_directory, args.local_directory)

        if args.compress:
            os.remove(args.local_directory)

        logging.info("Directory transfer completed.")

    except (paramiko.AuthenticationException, paramiko.SSHException, paramiko.sftp.SFTPError) as e:
        print(f"An error occurred during SSH/SFTP connection: {str(e)}")
        sys.exit(1)
    except (TimeoutError, ConnectionRefusedError) as e:
        print(f"An error occurred during FTP connection: {str(e)}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Local directory not found: {args.local_directory}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

