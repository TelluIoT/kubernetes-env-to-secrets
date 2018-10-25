# kubernetes-env-to-secrets
Convert environment files to kubernetes secrets

```
usage: main.py [-h] [--name [name]] [--env [.env]] [--secrets [.yaml]]

Convert environment files to kubernetes secrets

optional arguments:
  -h, --help         show this help message and exit
  --name [name]      Name of the secret store
  --env [.env]       Environment input file, stdin by default
  --secrets [.yaml]  Secrets output file, stdout by default
```

#### Example:

```sh
$ cat .env
CANARD=true
LAPIN=12343
BONJOUR_LES_GENS=abcdef
# Can also embed file content
SECRET_FILE=filecontent=./secret_file
```


```sh
$ python main.py --env .env --name lapin
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: lapin
type: Opaque
data:
  canard: dHJ1ZQ==
  lapin: MTIzNDM=
  bonjour_les_gens: YWJjZGVm
  secret_file: aGVsbG8K
```
