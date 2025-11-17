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

interface Config {
  handle: string;
  password: string;
  download_path: string;
  limit: number;
}

async function main() {
  try {
    const config = await readYamlConfigFile('config.yaml');
    const data = yaml.load(config) as Config;

    console.log('Connecting to AT Protocol...');
    console.log('Handle:', data.handle);
    console.log('Download path:', data.download_path);

    // Create download directory if it doesn't exist
    if (!existsSync(data.download_path)) {
      await fs.mkdir(data.download_path, { recursive: true });
      console.log('Created download directory');
    }

    // Initialize AT Protocol agent
    const agent = new AtpAgent({
      service: 'https://bsky.social'
    });

    await agent.login({
      identifier: data.handle,
      password: data.password
    });

    console.log('Logged in successfully!');
    console.log(`Will download up to ${data.limit} images`);

    // TODO: Fetch feed and download images
    console.log('Image download functionality coming soon...');

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main()