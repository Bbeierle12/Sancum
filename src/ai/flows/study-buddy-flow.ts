'use server';
/**
 * @fileOverview An AI agent that acts as a scripture study buddy.
 *
 * - studyBuddy - A function that provides answers to scripture questions.
 * - StudyBuddyInput - The input type for the studyBuddy function.
 * - StudyBuddyOutput - The return type for the studyBuddy function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const StudyBuddyInputSchema = z.object({
  scripture: z.string().describe('The scripture reference the user is asking about.'),
  question: z.string().describe('The user\'s question about the scripture.'),
});
export type StudyBuddyInput = z.infer<typeof StudyBuddyInputSchema>;

const StudyBuddyOutputSchema = z.object({
  answer: z.string().describe('A helpful and insightful answer to the user\'s question, based on the provided scripture.'),
});
export type StudyBuddyOutput = z.infer<typeof StudyBuddyOutputSchema>;

export async function studyBuddy(input: StudyBuddyInput): Promise<StudyBuddyOutput> {
  return studyBuddyFlow(input);
}

const prompt = ai.definePrompt({
  name: 'studyBuddyPrompt',
  input: {schema: StudyBuddyInputSchema},
  output: {schema: StudyBuddyOutputSchema},
  prompt: `You are an expert, friendly, and insightful scripture study companion. Your purpose is to help users deepen their understanding of the scriptures.

  A user has provided the following scripture reference and question.
  Scripture: {{{scripture}}}
  Question: {{{question}}}

  Please provide a thoughtful, contextually aware, and encouraging response that directly addresses their question. Draw upon the scripture itself, and if relevant, briefly mention related verses or principles to enrich their understanding. Keep your tone supportive and helpful.
  `,
});

const studyBuddyFlow = ai.defineFlow(
  {
    name: 'studyBuddyFlow',
    inputSchema: StudyBuddyInputSchema,
    outputSchema: StudyBuddyOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
