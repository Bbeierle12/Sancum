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

const UserContextSchema = z.object({
  themes_studied: z.array(z.string()).describe("A list of spiritual themes the user has studied previously."),
  emotional_struggles: z.array(z.string()).describe("A list of emotional struggles the user has mentioned."),
  spiritual_goals: z.array(z.string()).describe("A list of spiritual goals the user has set."),
}).optional();

const StudyBuddyInputSchema = z.object({
  scripture: z.string().describe('The scripture reference the user is asking about.'),
  question: z.string().describe('The user\'s question about the scripture.'),
  userContext: UserContextSchema,
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
  identified_themes: z.array(z.string()).describe('A list of spiritual themes identified in the user query and your response, which will be used to update the user\'s profile.'),
  identified_emotions: z.array(z.string()).describe('A list of emotions identified in the user query, which will be used to update the user\'s profile.'),
});
export type StudyBuddyOutput = z.infer<typeof StudyBuddyOutputSchema>;

export async function studyBuddy(input: StudyBuddyInput): Promise<StudyBuddyOutput> {
  return studyBuddyFlow(input);
}

const prompt = ai.definePrompt({
  name: 'studyBuddyPrompt',
  input: {schema: StudyBuddyInputSchema},
  output: {schema: StudyBuddyOutputSchema},
  prompt: `You are a Christ-centered Scripture Study Assistant. You behave like a wise, loving spiritual companion, remembering prior conversations and responding with empathy and grace.

{{#if userContext}}
You have memory of the user's past interactions. Here is their spiritual context:
{{#if userContext.themes_studied}}
- Previously Studied Themes: {{#each userContext.themes_studied}}{{{this}}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}
{{#if userContext.emotional_struggles}}
- Mentioned Emotional Struggles: {{#each userContext.emotional_struggles}}{{{this}}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}
{{#if userContext.spiritual_goals}}
- Stated Spiritual Goals: {{#each userContext.spiritual_goals}}{{{this}}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}

Use this context to inform your response. Start with a gentle, personalized check-in before addressing their current query. For example: "I remember you were struggling with fear. Here's a passage that might bring comfort today." or "Last week we explored patience—would you like to reflect on how that's been?"
{{/if}}

Please respond to the user’s query in the following structured JSON format:
1.  **verse**: Provide an accurate quotation and reference for a relevant Bible verse.
2.  **explanation**: Give a clear, doctrinally sound summary of what this verse means, in an emotionally intelligent and Christlike tone.
3.  **application**: Offer a gentle, Christlike encouragement or a practical action the user can take (e.g., forgiveness, worship, prayer, reflection, humility).
4.  **prayer** (optional): Write a 1-2 sentence prayer that is intimate, Christ-focused, and aligned to the theme.
5.  **cross_reference**: List 1-2 supporting verses that harmonize with the main theme, preferably including Christ's own words.
6.  **identified_themes**: Analyze the user's query and your response, and list any spiritual themes found (e.g., "patience", "forgiveness").
7.  **identified_emotions**: Analyze the user's query and list any emotions mentioned (e.g., "fear", "guilt").

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
