import { GoogleGenAI } from '@google/genai';
import type { Interactions } from '@google/genai';

const ai = new GoogleGenAI({
    apiKey: process.env['GEMINI_API_KEY'],
});

const tools: Interactions.Tool[] = [
    {
        type: 'google_search',
    },
];

const generationConfig = {
    temperature: 1,
    max_output_tokens: 65536,
    top_p: 0.95,
};

async function main() {
    const interaction = await ai.interactions.create({
        model: 'models/gemini-2.5-flash',
        input: 'Hello',
        tools: tools,
        generation_config: generationConfig,
    });

    console.log(interaction.steps?.at(-1));
}

main();
