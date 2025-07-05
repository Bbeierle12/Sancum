'use client';

import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { BrainCircuit, LoaderCircle, Sparkles } from 'lucide-react';
import { getStudyBuddyResponse } from '@/lib/actions';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const initialState = {
  answer: '',
  error: null,
};

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending} className="w-full sm:w-auto">
      {pending ? (
        <>
          <LoaderCircle className="animate-spin" />
          Thinking...
        </>
      ) : (
        <>
          <BrainCircuit />
          Ask Study Buddy
        </>
      )}
    </Button>
  );
}

export default function StudyBuddyPage() {
  const [state, formAction] = useActionState(getStudyBuddyResponse, initialState);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Scripture Study Buddy</h1>
        <p className="text-lg text-muted-foreground">
          Ask questions and gain deeper insights into the scriptures.
        </p>
      </div>

      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="font-headline">Ask a Question</CardTitle>
          <CardDescription>
            Enter a scripture reference and your question to start a conversation with your AI study buddy.
          </CardDescription>
        </CardHeader>
        <form action={formAction}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="scripture">Scripture Reference</Label>
              <Input id="scripture" name="scripture" placeholder="e.g., John 3:16" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="question">Your Question</Label>
              <Textarea
                id="question"
                name="question"
                placeholder="e.g., What does it mean to be 'born again'?"
                className="min-h-[150px]"
                required
              />
            </div>
          </CardContent>
          <CardFooter>
            <SubmitButton />
          </CardFooter>
        </form>
      </Card>

      {(state.answer || state.error) && (
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="font-headline">Study Buddy's Response</CardTitle>
          </CardHeader>
          <CardContent>
            <Alert variant={state.error ? 'destructive' : 'default'}>
              {state.error ? null : <Sparkles className="h-4 w-4" />}
              <AlertTitle>{state.error ? 'Error' : 'Insight'}</AlertTitle>
              <AlertDescription className="prose prose-sm dark:prose-invert max-w-none">
                {state.error ? <p>{state.error}</p> : <p>{state.answer}</p>}
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
