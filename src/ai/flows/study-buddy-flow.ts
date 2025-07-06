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
  verse: z.object({
    reference: z.string().describe('Canonical Bible verse with full reference.'),
    text: z.string().describe('The full text of the verse.'),
  }),
  explanation: z
    .string()
    .describe(
      'Doctrinally sound and emotionally intelligent summary in a Christlike tone.'
    ),
  application: z
    .string()
    .describe(
      'Real-world reflection or behavioral call-to-action modeled after Jesus’ teachings.'
    ),
  prayer: z
    .string()
    .optional()
    .describe('Short, simple prayer aligned to the theme of the response.'),
  cross_reference: z
    .array(
      z.object({
        reference: z.string().describe('The reference of a supporting verse.'),
        text: z.string().describe('The text of the supporting verse.'),
      })
    )
    .describe(
      'One or more supporting verses from elsewhere in Scripture, especially Christ’s own words.'
    ),
});
export type StudyBuddyOutput = z.infer<typeof StudyBuddyOutputSchema>;

export async function studyBuddy(input: StudyBuddyInput): Promise<StudyBuddyOutput> {
  return studyBuddyFlow(input);
}

const prompt = ai.definePrompt({
  name: 'studyBuddyPrompt',
  input: {schema: StudyBuddyInputSchema},
  output: {schema: StudyBuddyOutputSchema},
  prompt: `You are a Christ-centered Scripture Study Assistant.
Please respond to the user’s query in the following structured JSON format:
1.  **verse**: Provide an accurate quotation and reference for a relevant Bible verse.
2.  **explanation**: Give a clear, doctrinally sound summary of what this verse means, in an emotionally intelligent and Christlike tone.
3.  **application**: Offer a gentle, Christlike encouragement or a practical action the user can take (e.g., forgiveness, worship, prayer, reflection, humility).
4.  **prayer** (optional): Write a 1-2 sentence prayer that is intimate, Christ-focused, and aligned to the theme.
5.  **cross_reference**: List 1-2 supporting verses that harmonize with the main theme, preferably including Christ's own words.

The user is asking about this scripture: {{{scripture}}}.
Their specific question is: {{{question}}}

Base your response on their query.
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
