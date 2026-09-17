import { readFileSync,writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { defaultRoot } from './validate.mjs';
import { read,scoreCases } from './reference.mjs';
if(!process.argv[2])throw new Error('Usage: node packages/atlas-expansion/score.mjs predictions.json [result.json]');
const result=scoreCases(JSON.parse(readFileSync(resolve(process.argv[2]))),JSON.parse(readFileSync(resolve(defaultRoot,'worked_answers/cases.json'))),read(defaultRoot,'evidence_passages'));
if(process.argv[3])writeFileSync(resolve(process.argv[3]),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
