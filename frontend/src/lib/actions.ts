
'use server';

import { generatePromptFromJournal, GeneratePromptFromJournalOutput } from '@/ai/flows/generate-prompt-from-journal';
import { studyBuddy, StudyBuddyOutput } from '@/ai/flows/study-buddy-flow';
import { z } from 'zod';
import { getVerse } from './bible-api';

const journalFormSchema = z.object({
  journalEntries: z.string(),
  verse: z.string(),
});

type JournalState = {
  prompt?: string;
  error?: string | null;
}

export async function getAIPrompt(prevState: JournalState, formData: FormData): Promise<JournalState> {
  const validatedFields = journalFormSchema.safeParse({
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

const studyBuddyFormSchema = z.object({
  scripture: z.string().optional(),
  question: z.string().min(1, 'Question is required.'),
});

type StudyBuddyState = {
  answer?: StudyBuddyOutput | null;
  error?: string | null;
}

export async function getStudyBuddyResponse(prevState: StudyBuddyState, formData: FormData): Promise<StudyBuddyState> {
  const validatedFields = studyBuddyFormSchema.safeParse({
    scripture: formData.get('scripture'),
    question: formData.get('question'),
  });

  if (!validatedFields.success) {
    const errors = validatedFields.error.flatten().fieldErrors;
    const errorString = [
      ...(errors.scripture || []),
      ...(errors.question || []),
    ].join(' ');
    return { error: `Invalid form data. ${errorString}`.trim() };
  }

  try {
    const scripture = validatedFields.data.scripture;
    let verseText = '';
    if (scripture) {
      const verse = await getVerse(scripture);
      if (verse) {
        verseText = verse.text;
      }
    }

    const input = {
      scripture: validatedFields.data.scripture,
      question: validatedFields.data.question,
      userContext: {}, 
    };
    const result: StudyBuddyOutput = await studyBuddy(input);
    
    return { answer: result, error: null };
  } catch (error) {
    console.error('Error getting study buddy response:', error);
    return { error: 'Failed to get a response from the study buddy. Please try again later.' };
  }
}
