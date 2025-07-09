'use server';
/**
 * @fileOverview An AI agent that generates personalized prompts based on user journal entries.
 *
 * - generatePromptFromJournal - A function that generates a personalized prompt.
 * - GeneratePromptFromJournalInput - The input type for the generatePromptFromJournal function.
 * - GeneratePromptFromJournalOutput - The return type for the generatePromptFromJournal function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GeneratePromptFromJournalInputSchema = z.object({
  journalEntries: z.string().describe('The user journal entries.'),
  verse: z.string().describe('The scripture verse for generating the prompt.'),
});
export type GeneratePromptFromJournalInput = z.infer<typeof GeneratePromptFromJournalInputSchema>;

const GeneratePromptFromJournalOutputSchema = z.object({
  prompt: z.string().describe('A personalized prompt to stimulate thought and reflection on scripture.'),
});
export type GeneratePromptFromJournalOutput = z.infer<typeof GeneratePromptFromJournalOutputSchema>;

export async function generatePromptFromJournal(input: GeneratePromptFromJournalInput): Promise<GeneratePromptFromJournalOutput> {
  return generatePromptFromJournalFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generatePromptFromJournalPrompt',
  input: {schema: GeneratePromptFromJournalInputSchema},
  output: {schema: GeneratePromptFromJournalOutputSchema},
  prompt: `You are a spiritual guide that suggests personalized prompts to stimulate thought and reflection on scripture.

  Given the following scripture verse:
  {{verse}}

  And the following journal entries:
  {{journalEntries}}

  Generate a prompt that is tailored to the user's previous journal entries, so that they can gain deeper insights and strengthen their connection to the material.
  `,
});

const generatePromptFromJournalFlow = ai.defineFlow(
  {
    name: 'generatePromptFromJournalFlow',
    inputSchema: GeneratePromptFromJournalInputSchema,
    outputSchema: GeneratePromptFromJournalOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
