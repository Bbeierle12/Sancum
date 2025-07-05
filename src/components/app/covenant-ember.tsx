'use client';

import { useEffect, useActionState } from 'react';
import { useFormStatus } from 'react-dom';
import { Sparkles, LoaderCircle, AlertTriangle } from 'lucide-react';

import { getAIPrompt } from '@/lib/actions';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { useToast } from '@/hooks/use-toast';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending}>
      {pending ? (
        <>
          <LoaderCircle className="animate-spin" />
          Generating...
        </>
      ) : (
        <>
          <Sparkles />
          Generate Prompt
        </>
      )}
    </Button>
  );
}

type CovenantEmberProps = {
  verse: string;
  journalEntries: string;
};

const initialState = {
  prompt: "Click 'Generate Prompt' to get a personalized reflection starter based on your journal entries and the verse above.",
  error: null,
};

export function CovenantEmber({ verse, journalEntries }: CovenantEmberProps) {
  const [state, formAction] = useActionState(getAIPrompt, initialState);
  const { toast } = useToast();

  useEffect(() => {
    if (state.error) {
      toast({
        variant: 'destructive',
        title: 'Error',
        description: state.error,
      });
    }
  }, [state, toast]);

  return (
    <div>
      <Alert className="mb-4">
        {state.error ? <AlertTriangle className="h-4 w-4" /> : <Sparkles className="h-4 w-4" />}
        <AlertTitle className="font-headline">{state.error ? 'Error' : 'Covenant Ember'}</AlertTitle>
        <AlertDescription>{state.prompt}</AlertDescription>
      </Alert>

      <form action={formAction}>
        <input type="hidden" name="verse" value={verse} />
        <input type="hidden" name="journalEntries" value={journalEntries} />
        <SubmitButton />
      </form>
    </div>
  );
}
