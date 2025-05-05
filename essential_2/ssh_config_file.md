### SSH Configuration

To set up SSH for a specific host, follow these steps:

1. Open the SSH configuration file:
    ```bash
    nano ~/.ssh/config
    ```

2. Add the following configuration to the file:

    ```bash
    Host 233
       HostName 192.168.1.233
       User tigerit
    ```

3. Save and exit the editor by pressing `Ctrl + X`, then confirm the changes by pressing `Y`, and hit `Enter`.

### Usage

Once the configuration is saved, you can SSH into the machine using the alias `233` by running:

```bash
ssh 233
