import argparse
import sys
import configparser
import itertools
import base64
from string import Template

parser = argparse.ArgumentParser(description='Convert environment files to kubernetes secrets')
parser.add_argument('--name', metavar='name', nargs='?', type=str, default='my-secrets', help='Name of the secret store')
parser.add_argument('--env', metavar='.env', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Environment input file, stdin by default')
parser.add_argument('--secrets', metavar='.yaml', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Secrets output file, stdout by default')

args = parser.parse_args()

config = configparser.ConfigParser()
config.read_file(itertools.chain(['[global]'], args.env), source="env")
secrets = config.items('global')
args.env.close()

encodedSecrets = ['  {0}: {1}'.format(
    secret[0],
    base64.b64encode(secret[1].encode('utf-8')).decode('utf-8')
) for secret in secrets]

yamlTemplate = Template("""apiVersion: v1
kind: Secret
metadata: $name
type: Opaque
data:
$encodedSecrets""")
yamlOutput = yamlTemplate.substitute(name=args.name, encodedSecrets='\n'.join(encodedSecrets))

args.secrets.write(yamlOutput)
args.secrets.close()