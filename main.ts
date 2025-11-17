import { AtpAgent } from '@atproto/api'
import { existsSync } from 'fs';
import { access } from 'fs/promises'
import { promises as fs } from 'fs';
import * as yaml from 'js-yaml';
import * as path from 'path';

async function readYamlConfigFile(filePath: string) {
  const fileContents = await fs.readFile(filePath, 'utf8');
  return fileContents;
}

async function main() {
  const config = await readYamlConfigFile('config.yaml');

  interface Config {
    handle: string,
    password: string,
    downloadPath: string,
    limit: number
  };

  const data = yaml.load(config) as Config;
  console.log(data.handle)
}

main()