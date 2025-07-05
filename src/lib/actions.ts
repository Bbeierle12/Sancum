
'use server';

import { generatePromptFromJournal, GeneratePromptFromJournalOutput } from '@/ai/flows/generate-prompt-from-journal';
import { z } from 'zod';

const formSchema = z.object({
  journalEntries: z.string(),
  verse: z.string(),
});

type State = {
  prompt?: string;
  error?: string | null;
}

export async function getAIPrompt(prevState: State, formData: FormData): Promise<State> {
  const validatedFields = formSchema.safeParse({
    journalEntries: formData.get('journalEntries'),
    verse: formData.get('verse'),
  });

  if (!validatedFields.success) {
    return { error: 'Invalid form data. Please try again.' };
  }

  try {
    const result: GeneratePromptFromJournalOutput = await generatePromptFromJournal(validatedFields.data);
    return { prompt: result.prompt, error: null };
  } catch (error) {
    console.error('Error generating prompt:', error);
    return { error: 'Failed to generate a new prompt. Please try again later.' };
  }
}
