import { AtpAgent } from '@atproto/api';
import { existsSync } from 'fs';
import { promises as fs } from 'fs';
import * as yaml from 'js-yaml';
async function readYamlConfigFile(filePath) {
    const fileContents = await fs.readFile(filePath, 'utf8');
    return fileContents;
}
async function getAllLikes(agent, handle) {
    let cursor = undefined;
    let allLikes = [];
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
        const data = yaml.load(config);
        const HANDLE = data.handle;
        const PASSWORD = data.password;
        const DOWNLOAD_PATH = data.download_path;
        const DOWNLOAD_LIMIT = data.limit;
        console.log('Connecting to AT Protocol...');
        console.log('Handle:', HANDLE);
        console.log('Download path:', DOWNLOAD_PATH);
        // Create download directory if it doesn't exist
        if (!existsSync(DOWNLOAD_PATH)) {
            await fs.mkdir(DOWNLOAD_PATH, { recursive: true });
            console.log('Created download directory');
        }
        // Initialize AT Protocol agent
        const agent = new AtpAgent({
            service: 'https://bsky.social'
        });
        await agent.login({
            identifier: HANDLE,
            password: PASSWORD
        });
        // Fetch likes from agent
        getAllLikes(agent, HANDLE);
    }
    catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
})();
//# sourceMappingURL=main.js.map