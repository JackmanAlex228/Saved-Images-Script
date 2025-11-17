import { promises as fs } from 'fs';
import * as yaml from 'js-yaml';
async function readYamlConfigFile(filePath) {
    const fileContents = await fs.readFile(filePath, 'utf8');
    return fileContents;
}
async function main() {
    const config = await readYamlConfigFile('config.yaml');
    ;
    const data = yaml.load(config);
    console.log(data.handle);
}
main();
