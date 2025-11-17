import { AtpAgent } from '@atproto/api'
import { existsSync } from 'fs';
import { access } from 'fs/promises'
import { promises as fs } from 'fs';
import * as yaml from 'js-yaml';
import * as path from 'path';

interface Config {
  handle: string;
  password: string;
  download_path: string;
  limit: number;
}

async function readYamlConfigFile(filePath: string) {
  const fileContents = await fs.readFile(filePath, 'utf8');
  return fileContents;
}

async function compareFilenames(filename: string, downloadPath: string): Promise<string | null> {
  const filePath = path.join(downloadPath, filename);
  if (existsSync(filePath)) {
    return downloadPath;
  }
  return null;
}

async function downloadImages(allLikes: any[], downloadPath: string, limit: number) {
  const duplicates: string[] = [];
  console.log(`Total liked posts: ${allLikes.length}\n`);
  console.log('Downloading media files...');
  // Process only up to the limit
  const likesToProcess = allLikes.slice(0, limit);
  // Initialize cache file
  const cacheFile = path.join(downloadPath, '.cache.json');
  let cache: string[] = [];
  if (existsSync(cacheFile)) {
    cache = JSON.parse(await fs.readFile(cacheFile, 'utf8'));
  }
  const cacheSet = new Set(cache);
  for (const item of likesToProcess) {
    let imageLink = '';
    try {
      // Check for images in different embed types
      if (item.post.embed?.images) {
        imageLink = item.post.embed.images[0].fullsize;
      } else if (item.post.embed?.media?.images) {
        imageLink = item.post.embed.media.images[0].fullsize;
      } else {
        continue; // No image found, skip
      }
    } catch (error) {
      console.log(`No image found for post ${item.post.uri}`);
      continue;
    }
    // Generate filename from post URI
    const filename = `${item.post.uri.split('/').pop()}.png`;
    // Check if file already exists in the download path
    const pathOfDupe = await compareFilenames(filename, downloadPath);
    if (pathOfDupe) {
      console.log(`File ${filename} already exists in path ${pathOfDupe}`);
      duplicates.push(filename);
      continue;
    }
    // Check if the file already exists in the program cache
    const uri = item.post.uri.split('/').pop();
    if (cacheSet.has(uri)) {
      console.log(`Skipping cached file ${uri}`)
      continue;
    }
    // Download the image
    try {
      const response = await fetch(imageLink);
      const buffer = await response.arrayBuffer();
      // Save to file
      const filePath = path.join(downloadPath, filename);
      await fs.writeFile(filePath, Buffer.from(buffer));
      console.log(`Downloaded: ${filename}`)
    } catch (error) {
      console.error(`Failed to download ${filename}`, error)
    }
  }
  console.log('Finished!');
  console.log(`There are ${duplicates.length} duplicate files in the download path.`)
}

async function getAllLikes(agent: AtpAgent, handle: string) {
  let cursor: string | undefined = undefined;
  let allLikes: any[] = [];
  let numFetched = 0;
  console.log(`Fetching liked posts for ${handle}...`);
  while (true) {
    const resp = await agent.app.bsky.feed.getActorLikes({
      actor: handle,
      cursor: cursor
    });
    allLikes.push(...resp.data.feed);
    // Break if no more results
    if (!resp.data.cursor) {
      break;
    }
    cursor = resp.data.cursor;
    // Break if empty response
    if (resp.data.feed.length === 0) {
      break;
    }
    numFetched += resp.data.feed.length;
    process.stdout.write(`\r(${numFetched} liked posts so far)`);
  }
  console.log(`\nTotal liked posts: ${allLikes.length}\n`);
  return allLikes;
}

(async () => {
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

    // Fetch likes from agent
    const allLikes = await getAllLikes(agent, data.handle)

    // Download the images
    downloadImages(allLikes, data.download_path, data.limit)

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
})();